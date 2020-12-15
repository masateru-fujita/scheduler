from django import forms
from .models import Schedule

class ScheduleCreateForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ("title","detail","date","start_time","end_time")