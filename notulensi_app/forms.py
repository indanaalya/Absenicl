from django import forms
from django.forms import ModelForm, fields, widgets
from .models import Asisten,Absensi,Rapat

class addasisten(ModelForm):
    class Meta:
        model = Asisten
        fields = ("nama", "nim")