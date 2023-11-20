import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Assessment,
    Report,
    ReportTemplate,
    QualitativeAssessmentChoices,
    QualitativeAssessmentScore,
    QuantitativeAssessmentScore,
)
from .permissions import CustomPermission
from .serializers import (
    AssessmentSerializer,
    AssessmentWithChoicesSerializer,
    ReportTemplateSerializer, 
    ReportTemplateListSerializer
)

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [CustomPermission, permissions.IsAuthenticated]

    @action(detail=True, methods=["GET"])
    def assessments(self, request, pk=None):
        template = self.get_object()
        assessments = template.assessments.all()
        serializer = AssessmentWithChoicesSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def report_dates(self, request, pk=None):
        template = self.get_object()
        user = request.user
        report_dates = Report.objects.filter(template=template, user=user).values("creation_date").distinct().order_by("-creation_date")
        return Response(report_dates, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def report_dates_user(self, request, pk=None, user_pk=None):
        template = self.get_object()
        user = get_user_model().objects.get(pk=user_pk)
        report_dates = Report.objects.filter(template=template, user=user).values("creation_date").distinct().order_by("-creation_date")
        return Response(report_dates, status=status.HTTP_200_OK)


class ReportTemplateListVeiwset(viewsets.ReadOnlyModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateListSerializer
    permission_classes = [CustomPermission, permissions.IsAuthenticated]


class HandleReportForm(views.APIView):
    permission_classes = [CustomPermission, permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        # permissions.IsAuthenticated handles checking if user is authenticated
        user = get_user_model().objects.get(pk=data["userId"])

        # check if template_id has a real template
        try:
            template_id = data["templateId"]
            template = ReportTemplate.objects.get(pk=template_id)
        except KeyError:
            return Response({"error": "templateId not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except ReportTemplate.DoesNotExist:
            return Response({"error": "Report Template does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if date is valid
        try:
            date_str = data["date"]
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except KeyError:
            return Response({"error": "Date not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid date format. Excpected YYYY-MM_DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        # validate the assessment scores
        try:
            assessments = data["assessments"]
        except KeyError:
            return Response({"error": "assessments not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                report = Report.objects.create(user=user, template=template, creation_date=date_obj)

                for assessment, assessment_data in assessments.items():
                    assessment_obj = Assessment.objects.get(pk=assessment_data["id"])
                    report.assessments.add(assessment_obj)

                    if assessment_data["type"] == "qualitative":
                        choice = assessment_data["value"]
                        choice_obj = assessment_obj.choices.get(choice=choice)
                        QualitativeAssessmentScore.objects.create(
                            assessment=assessment_obj,
                            qualitative_assessment=assessment_obj.qualitative_details,
                            user=user,
                            report=report,
                            score=choice_obj
                        )
                    elif assessment_data["type"] == "quantitative":
                        score = Decimal(assessment_data["value"])
                        QuantitativeAssessmentScore.objects.create(
                            assessment=assessment_obj,
                            quantitative_assessment=assessment_obj.quantitative_details,
                            user=user,
                            report=report,
                            score=score
                        )
                    else:
                        raise ValueError("Assessment type")
        except Assessment.DoesNotExist:
            return Response({"error": "Assessment does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except QualitativeAssessmentChoices.DoesNotExist:
            return Response({"error": "Choice does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidOperation as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Report created"}, status=status.HTTP_200_OK)

class UserReport(views.APIView):
    permission_classes = [CustomPermission, permissions.IsAuthenticated]

    def get(self, request, template_pk=None, date=None):
        user = request.user
        template = ReportTemplate.objects.get(pk=template_pk)
        creation_date = date

        report = Report.objects.filter(
            user=user,
            template=template,
            creation_date=creation_date
        ).first()

        assessments = report.assessments.all()

        data = []

        for assessment in assessments:
            name = assessment.name
            type = assessment.assessment_type
            description = assessment.description
            unit = assessment.unit
            
            if type == "quantitative":
                passing_score = assessment.quantitative_details.passing_score
                quantitative_obj = QuantitativeAssessmentScore.objects.get(
                    user=user,
                    assessment=assessment,
                    quantitative_assessment=assessment.quantitative_details,
                    report=report
                )
                score = quantitative_obj.score
                passed = quantitative_obj.passed()
                did_not_test = quantitative_obj.did_not_test
            else:
                passing_score = assessment.qualitative_details.passing_score.choice
                qualitative_obj = QualitativeAssessmentScore.objects.get(
                    assessment=assessment,
                    qualitative_assessment=assessment.qualitative_details,
                    user=user,
                    report=report
                )
                score = qualitative_obj.score.choice
                passed = qualitative_obj.passed()
                did_not_test = quantitative_obj.did_not_test
            drills = []
            drill_objs = assessment.drills.all()
            for drill in drill_objs:
                drill_name = drill.name
                drill_url = drill.url
                drills.append({"name": drill_name, "drill_url": drill_url})

            assessment_data = {
                "name": name,
                "type": type,
                "description": description,
                "unit": unit,
                "passing_score": passing_score,
                "score": score,
                "passed": passed,
                "did_not_test": did_not_test,
                "drills": drills
            }

            data.append(assessment_data)
        return Response(data, status=status.HTTP_200_OK)

class UserReportTrainer(views.APIView):
    permission_classes = [CustomPermission, permissions.IsAuthenticated]

    def get(self, request, template_pk=None, date=None, user_pk=None):
        user = get_user_model().objects.get(pk=user_pk)
        template = ReportTemplate.objects.get(pk=template_pk)
        creation_date = date

        report = Report.objects.filter(
            user=user,
            template=template,
            creation_date=creation_date
        ).first()

        print(report)

        assessments = report.assessments.all()

        data = []

        for assessment in assessments:
            name = assessment.name
            type = assessment.assessment_type
            description = assessment.description
            unit = assessment.unit
            
            if type == "quantitative":
                passing_score = assessment.quantitative_details.passing_score
                quantitative_obj = QuantitativeAssessmentScore.objects.get(
                    user=user,
                    assessment=assessment,
                    quantitative_assessment=assessment.quantitative_details,
                    report=report
                )
                score = quantitative_obj.score
                passed = quantitative_obj.passed()
            else:
                passing_score = assessment.qualitative_details.passing_score.choice
                qualitative_obj = QualitativeAssessmentScore.objects.get(
                    assessment=assessment,
                    qualitative_assessment=assessment.qualitative_details,
                    user=user,
                    report=report
                )
                score = qualitative_obj.score.choice
                passed = qualitative_obj.passed()
            drills = []
            drill_objs = assessment.drills.all()
            for drill in drill_objs:
                drill_name = drill.name
                drill_url = drill.url
                drills.append({"name": drill_name, "drill_url": drill_url})

            assessment_data = {
                "name": name,
                "type": type,
                "description": description,
                "unit": unit,
                "passing_score": passing_score,
                "score": score,
                "passed": passed,
                "drills": drills
            }

            data.append(assessment_data)
        return Response(data, status=status.HTTP_200_OK)