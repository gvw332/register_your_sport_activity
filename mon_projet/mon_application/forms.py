from django import forms
from .models import Activity
from .models import UserObjective


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['date', 'name', 'marche', 'jogging', 'velo', 'total', 'calories']

class UserObjectiveForm(forms.ModelForm):
    class Meta:
        model = UserObjective
        fields = ['objectif_marche', 'objectif_jogging', 'objectif_velo']