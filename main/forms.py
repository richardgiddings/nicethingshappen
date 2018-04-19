from django import forms
from .models import NiceThing

class NiceThingForm(forms.ModelForm):
    class Meta:
        model = NiceThing
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'rows': '12',
                'cols': '80',
                'maxlength': '400',
            }),
        }

class ReportNiceThingForm(forms.ModelForm):
    class Meta:
        model = NiceThing
        fields = ['id', 'reported_reason']