from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Pitch(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class PitchAttribute(models.Model):
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.pitch.name}: {self.attribute}"


class PitchAttributeChoice(models.Model):
    attribute = models.ForeignKey(PitchAttribute, on_delete=models.CASCADE)
    score = models.IntegerField()
    description = models.TextField()

    class Meta:
        unique_together = ("attribute", "score")
    
    def __str__(self):
        return f"{self.attribute.pitch.name} | {self.attribute.attribute[:10]}... | Score: {self.score}"


class PitchArsenalReport(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name + ' ' + self.user.last_name} pitch arsenal report on {self.date}."


class PitchAttributeScore(models.Model):
    report = models.ForeignKey(PitchArsenalReport, on_delete=models.CASCADE)
    score = models.ForeignKey(PitchAttributeChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.report.user.first_name + ' ' + self.report.user.last_name} | Report on {self.report.date} | {self.score.attribute.attribute[:10]} | Score: {self.score.score}"

class PitchMetrics(models.Model):
    report = models.ForeignKey(PitchArsenalReport, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    velocity = models.DecimalField(max_digits=4, decimal_places=1)
    spin = models.IntegerField()
    vertical_break = models.DecimalField(max_digits=4, decimal_places=1)
    horizontal_break = models.DecimalField(max_digits=4, decimal_places=1)
    
    class Meta:
        unique_together = ("report", "pitch")
    
    def __str__(self):
        return f"Pitch metrics for {self.report.user.first_name + ' ' + self.report.user.last_name} on {self.report.date}."


class PitchArsenalPitchNote(models.Model):
    report = models.ForeignKey(PitchArsenalReport, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pitch.name} note for {self.report.user.first_name + ' ' + self.report.user.last_name}'s report on {self.report.date}."