from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Assessment,
    ReportTemplate,
    Report,
    QualitativeAssessment,
    QuantitativeAssessment,
    QualitativeAssessmentScore,
    QuantitativeAssessmentScore,
    QualitativeAssessmentChoices,
    Drill
)

class CustomQuantitativeAssessmentAdmin(admin.ModelAdmin):
    ordering = ("assessment",)
    model = QuantitativeAssessment
    list_display = ("assessment", "passing_score", "passing_condition")
    list_filter = ("assessment", "passing_score", "passing_condition")
    # fieldsets = (
    #     (None, {'fields': ('email', "first_name", "last_name")}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', "first_name", "last_name", 'is_staff', 'password1', 'password2'),
    #     }),
    # )

class QualitativeAssessmentChoiceAdmin(admin.ModelAdmin):
    ordering = ("assessment",)
    model = QuantitativeAssessment
    list_display = ('assessment', 'choice')
    list_filter = ('assessment', 'choice')

class ReportTemplateAdmin(admin.ModelAdmin):
    ordering = ("name",)
    model = ReportTemplate
    list_display = ("name",)
    list_filter = ("name",)


# Register your models here.
admin.site.register(Assessment)
# admin.site.register(ReportTemplate, ReportTemplateAdmin)
admin.site.register(Report)
# admin.site.register(QuantitativeAssessment, CustomQuantitativeAssessmentAdmin)
# admin.site.register(QuantitativeAssessmentScore)
# admin.site.register(QualitativeAssessment)
# admin.site.register(QualitativeAssessmentChoices, QualitativeAssessmentChoiceAdmin)
# admin.site.register(QualitativeAssessmentScore)
admin.site.register(Drill)
