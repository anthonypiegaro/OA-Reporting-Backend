from django.urls import path
from .views import AllPitchesView, CreateReportView

urlpatterns = [
    path('all-pitches/', AllPitchesView.as_view(), name='all-pitches'),
    path("create-report/", CreateReportView.as_view(), name="create-report")
]