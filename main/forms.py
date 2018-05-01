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
        widgets = {
            'reported_reason' : forms.Textarea(attrs={
                'rows': '6',
                'cols': '80',
                'maxlength': '200',
            }),
        }

class ContactForm(forms.Form):
    contact_email = forms.EmailField(required=True, 
                    widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    message = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={'placeholder': 'Your message to us'}))
    send_copy = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "send_copy":
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'