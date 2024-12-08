from django import forms
from .models import DevTool

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = '__all__'  
