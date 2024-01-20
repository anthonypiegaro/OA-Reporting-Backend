from rest_framework import status
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