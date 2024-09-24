from rest_framework import serializers
from .models import Activity, UserObjective

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'date', 'name', 'marche', 'jogging', 'velo', 'total', 'calories']

class UserObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObjective
        fields = ['id', 'user', 'objectif_marche', 'objectif_jogging', 'objectif_velo']
