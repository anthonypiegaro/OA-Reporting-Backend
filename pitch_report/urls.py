from django.urls import path
from .views import (
    PitchList
)

urlpatterns = [
    path("get-pitches/", PitchList.as_view(), name="get-pitches"),
]
