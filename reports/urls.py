from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportTemplateViewSet, 
    ReportTemplateListVeiwset,
    HandleReportForm,
    UserReport,
    UserReportTrainer,
)

router = DefaultRouter()
router.register(r'report-templates', ReportTemplateViewSet)
router.register(r'report-templates-min', ReportTemplateListVeiwset)

urlpatterns = [
    path('', include(router.urls)),
    path("build-report/", HandleReportForm.as_view()),
    path("report-templates/<int:pk>/report-dates/", ReportTemplateViewSet.as_view({'get': 'report_dates'}), name='report-template-report-dates'),
    path("user-report/<int:template_pk>/<str:date>/", UserReport.as_view(), name="user-report"),
    path("trainer-user-report/<int:user_pk>/<int:template_pk>/<str:date>/", UserReportTrainer.as_view(), name="trainer-user-report"),
]
