from django import forms
from .models import NiceThing

class NiceThingForm(forms.ModelForm):
    class Meta:
        model = NiceThing
        fields = ['text']

class ReportNiceThingForm(forms.ModelForm):
    class Meta:
        model = NiceThing
        fields = ['id', 'reported_reason']