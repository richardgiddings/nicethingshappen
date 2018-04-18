from django import forms
from .models import NiceThing

class NiceThingForm(forms.ModelForm):
    class Meta:
        model = NiceThing
        fields = ['text']