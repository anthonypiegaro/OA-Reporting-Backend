from rest_framework import serializers
from .models import (
    Assessment,
    ReportTemplate,
    QualitativeAssessmentChoices,
    QualitativeAssessmentScore,
    QuantitativeAssessmentScore,
    Report
)

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = "__all__"


class ReportTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ["id", "name"]


class QualitativeAssessmentChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualitativeAssessmentChoices
        fields = "__all__"


class QualitativeAssessmentJustChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualitativeAssessmentChoices
        fields = ["id", "choice"]


class QualitativeAssessmentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualitativeAssessmentScore
        fields = "__all__"


class QuantitativeAssessmentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantitativeAssessmentScore
        fields = "__all__"


class AssessmentSerializer(serializers.ModelSerializer):
    qualitative_choices = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'assessment_type', 'description', 'unit']


class AssessmentWithChoicesSerializer(serializers.ModelSerializer):
    qualitative_choices = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'assessment_type', 'unit', "qualitative_choices"]

    def get_qualitative_choices(self, obj):
        if obj.assessment_type == 'qualitative':
            choices = obj.choices.all()
            return QualitativeAssessmentJustChoicesSerializer(choices, many=True).data
        return None
