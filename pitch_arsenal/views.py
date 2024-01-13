import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Pitch,
    PitchArsenalReport,
    PitchMetrics,
    PitchAttribute,
    PitchAttributeChoice,
    PitchAttributeScore,
    PitchArsenalPitchNote
)
from .serializers import PitchFormSerializer

class AllPitchesView(APIView):
    def get(self, request):
        pitches = Pitch.objects.all()
        serializer = PitchFormSerializer(pitches, many=True)
        return Response(serializer.data)


class CreateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data["data"]

        try:
            athlete = get_user_model().objects.get(pk=data["athlete"]["id"])
        except KeyError:
            return Response({"error": "Athlete not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except get_user_model().DoesNotExist:
            return Response({"error": "Athlete does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            date_str = data["date"]
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except KeyError:
            return Response({"error": "Date not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid date format. Excpected YYYY-MM_DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        report = PitchArsenalReport.objects.create(
            user=athlete,
            date=date_obj
        )

        for pitchId, pitchData in data["report"].items():
            if pitchData["throws"]:
                pitch = Pitch.objects.get(pk=pitchId)

                PitchArsenalPitchNote.objects.create(
                    report=report,
                    pitch=pitch,
                    note=pitchData["notes"]
                )

                velocity= Decimal(pitchData["metrics"]["velocity"])
                spin_rate = int(pitchData["metrics"]["spinRate"])
                horizontal_break = Decimal(pitchData["metrics"]["horizontalBreak"])
                vertical_break = Decimal(pitchData["metrics"]["verticalBreak"])

                PitchMetrics.objects.create(
                    report=report,
                    pitch=pitch,
                    velocity=velocity,
                    spin=spin_rate,
                    horizontal_break=horizontal_break,
                    vertical_break=vertical_break
                )

                for id, score in pitchData["attributes"].items():
                    choice_obj = PitchAttributeChoice.objects.get(pk=score)

                    attr_score = PitchAttributeScore.objects.create(
                        report=report,
                        score=choice_obj
                    )
                
        return Response({"Report created"}, status=status.HTTP_201_CREATED)





                





