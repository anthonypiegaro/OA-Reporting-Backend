from django.contrib import admin
from .models import (
    Pitch,
    PitchAttribute,
    PitchAttributeChoice,
    PitchArsenalReport,
    PitchAttributeScore,
    PitchMetrics,
    PitchArsenalPitchNote
)

admin.site.register(Pitch)
admin.site.register(PitchAttribute)
admin.site.register(PitchAttributeChoice)
admin.site.register(PitchArsenalReport)
admin.site.register(PitchAttributeScore)
admin.site.register(PitchMetrics)
admin.site.register(PitchArsenalPitchNote)
