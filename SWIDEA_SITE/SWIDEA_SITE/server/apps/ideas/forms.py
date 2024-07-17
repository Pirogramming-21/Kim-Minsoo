from django import forms
from .models import Idea
from apps.devtools.models import DevTool

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['name', 'image', 'description', 'interest', 'expected_tools']

    def save(self, commit=True):
        idea = super().save(commit=False)
        expected_tool = self.cleaned_data.get('expected_tools')
        devtool, created = DevTool.objects.get_or_create(name=expected_tool)
        idea.devtool = devtool
        if commit:
            idea.save()
        return idea