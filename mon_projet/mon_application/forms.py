from django import forms
from .models import Activity
from .models import UserObjective


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['date', 'name', 'marche', 'jogging', 'velo']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # Utilise le type datetime-local pour date et heure
                
            }),
        }
class UserObjectiveForm(forms.ModelForm):
    class Meta:
        model = UserObjective
        fields = ['objectif_marche', 'objectif_jogging', 'objectif_velo']