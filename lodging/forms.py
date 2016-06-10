from django import forms
from django.contrib import admin
from lodging.models import Lodging


class LodgingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LodgingForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.CheckboxSelectMultiple

    class Meta:
        model = Lodging

