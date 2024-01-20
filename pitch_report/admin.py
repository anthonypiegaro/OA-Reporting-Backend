from django.contrib import admin
from .models import (
    Pitch,
    FullPitchReport,
    PitchReport,
)

admin.site.register(Pitch)
admin.site.register(FullPitchReport)
admin.site.register(PitchReport)