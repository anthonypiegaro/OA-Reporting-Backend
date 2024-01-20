from django.urls import path
from .views import (
    PitchList,
    FullPitchReportView
)

urlpatterns = [
    path("get-pitches/", PitchList.as_view(), name="get-pitches"),
    path("full-report/", FullPitchReportView.as_view(), name="full-report"),
]
