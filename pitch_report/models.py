from django.contrib.auth import get_user_model
from django.db import models

class Pitch(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    document_file = models.FileField(upload_to="pdfs/", blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name + ' ' + self.user.last_name} pitcher report on {self.date}."


class PitchReport(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    velocity = models.DecimalField(max_digits=4, decimal_places=1)
    spin = models.IntegerField()
    vertical_break = models.DecimalField(max_digits=4, decimal_places=1)
    horizontal_break = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ("report", "pitch")
    
    def __str__(self):
        return f"{self.user.first_name + ' ' + self.user.last_name} | Report on {self.report.date} | {self.pitch.name}"
