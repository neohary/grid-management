from rest_framework import serializers
from .models import *

class ResidentChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentChangeLog
        fields = '__all__'

class HouseChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseChangeLog
        fields = '__all__'

class VillageChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageChangeLog
        fields = '__all__'

class MicroGridChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroGridChangeLog
        fields = '__all__'

class CustomStaticsTemplateChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomStaticsTemplateChangeLog
        fields = '__all__'

class CustomStaticsInstanceChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomStaticsInstanceChangeLog
        fields = '__all__'