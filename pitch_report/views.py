import json
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    PitchSerializer
)
from .models import (
    Pitch
)


class PitchList(APIView):
    def get(self, request):
        pitches = Pitch.objects.all()
        serializer = PitchSerializer(pitches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FullPitchReportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        athlete = request.data["athlete"]
        date = request.data["date"]
        notes = request.data["notes"]
        file = request.data["file"]
        pitches = request.data["pitches"]

        data = {
            "athlete": athlete,
            "date": date,
            "notes": notes,
            "file": file,
            "pitches": pitches
        }

        pitch_data = json.loads(pitches)
        print(pitch_data)
        print(type(pitch_data))
        return Response("Received", status=status.HTTP_201_CREATED)
