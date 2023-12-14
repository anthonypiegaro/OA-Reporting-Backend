from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

class NoPassingCondition(Exception):
    """Custom exception thrown when no condition is given"""
    pass

# Create your models here.
class Assessment(models.Model):
    ASSESSMENT_TYPE_CHOICES = [
        ("quantitative", "Quantitative"),
        ("qualitative", "Qualitative")
    ]

    name = models.CharField(max_length=100)
    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} assessment"


class ReportTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    assessments = models.ManyToManyField(Assessment, related_name="report_templates")

    def __str__(self):
        return f"{self.name} report template"


class Report(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    creation_date = models.DateField(default=timezone.now)
    assessments = models.ManyToManyField(Assessment, related_name="reports")

    def __str__(self):
        return f"Report for {self.user.first_name + ' ' + self.user.last_name} made from {self.template.name}"


class QuantitativeAssessment(models.Model):
    PASSING_CONDITION_CHOICES = [
        ('eq', 'Equal to'),
        ('gt', 'Greater than'),
        ('gte', 'Greater than or equal to'),
        ('lt', 'Less than'),
        ('lte', 'Less than or equal to'),
    ]

    assessment = models.OneToOneField(Assessment, related_name="quantitative_details", on_delete=models.CASCADE)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2)
    passing_condition = models.CharField(max_length=35, choices=PASSING_CONDITION_CHOICES)

    def __str__(self):
        return f"Quantitative details for {self.assessment.name}"
    
    def clean(self):
        if self.assessment.assessment_type != 'quantitative':
            raise ValidationError("The linked assessment must be of type 'quantitative'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call self.clean()
        super(QuantitativeAssessment, self).save(*args, **kwargs)


class QuantitativeAssessmentScore(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    quantitative_assessment = models.ForeignKey(QuantitativeAssessment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    did_not_test = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name + ' ' + self.user.last_name}'s score for {self.assessment} for report {self.report.template.name}"

    def passed(self):
        if self.quantitative_assessment.passing_condition == "eq":
            return self.score == self.quantitative_assessment.passing_score
        elif self.quantitative_assessment.passing_condition == "gt":
            return self.score > self.quantitative_assessment.passing_score
        elif self.quantitative_assessment.passing_condition == "gte":
            return self.score >= self.quantitative_assessment.passing_score
        elif self.quantitative_assessment.passing_condition == "lt":
            return self.score < self.quantitative_assessment.passing_score
        elif self.quantitative_assessment.passing_condition == "lte":
            return self.score <= self.quantitative_assessment.passing_score
        else:
            raise NoPassingCondition("No passing condition was defined")


class QualitativeAssessmentChoices(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('assessment', 'choice'),)

    def __str__(self):
        return f"{self.choice} is a choice option for the {self.assessment.name} assessment"

    def clean(self):
        if self.assessment.assessment_type != 'qualitative':
            raise ValidationError("The linked assessment must be of type 'qualitative'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call self.clean()
        super(QualitativeAssessmentChoices, self).save(*args, **kwargs)


class QualitativeAssessment(models.Model):
    assessment = models.OneToOneField(Assessment, related_name="qualitative_details", on_delete=models.CASCADE)
    passing_score = models.ForeignKey(QualitativeAssessmentChoices, on_delete=models.CASCADE)

    def __str__(self):
        return f"Qualitative assessment details for {self.assessment.name}"
    
    def clean(self):
        if self.assessment.assessment_type != 'qualitative':
            raise ValidationError("The linked assessment must be of type 'qualitative'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call self.clean()
        super(QualitativeAssessment, self).save(*args, **kwargs)


class QualitativeAssessmentScore(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    qualitative_assessment = models.ForeignKey(QualitativeAssessment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    score = models.ForeignKey(QualitativeAssessmentChoices, on_delete=models.CASCADE)
    did_not_test = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name + ' ' + self.user.last_name}'s score for {self.assessment.name} for report {self.report.template.name}"

    def passed(self):
        return self.score == self.qualitative_assessment.passing_score


class Drill(models.Model):
    assessments = models.ManyToManyField(Assessment, related_name="drills")
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=200, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.name} is recommended drill"


class TemplateAssessmentRelationship(models.Model):
    template = models.ForeignKey(ReportTemplate, verbose_name="template", on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, verbose_name="assessment", on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return f"Template: {self.template.name} | Assessment: {self.assessment.name} | Order: {self.order}"
