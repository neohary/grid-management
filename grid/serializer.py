from rest_framework import serializers
from .models import *
from resident.models import House,Resident

class VillageSerializer(serializers.ModelSerializer):
    mgrid_count = serializers.SerializerMethodField('get_mgrid_count')
    user_count = serializers.SerializerMethodField('get_user_count')
    houses_count = serializers.SerializerMethodField('get_houses_count')
    pop_count = serializers.SerializerMethodField('get_pop_count')

    def get_houses_count(self,Village):
        try:
            count = House.objects.filter(village=Village).exclude(deleted=True).count()
            return count
        except:
            return '-'
    
    def get_pop_count(self,Village):
        try:
            houses = House.objects.filter(village=Village).exclude(deleted=True)
            count = 0
            for house in houses:
                #print(house.pop)
                count += int(house.pop)
            return count
        except:
            return '-'
    
    def get_mgrid_count(self,Village):
        try:
            count = MicroGrid.objects.filter(village=Village).exclude(deleted=True).count()
            return count
        except:
            return '-'
    
    def get_user_count(self,Village):
        try:
            count = User.objects.filter(profile__village=Village).count()
            return count
        except:
            return '-'

    class Meta:
        model = Village
        fields = '__all__'

class MicroGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroGrid
        fields = ['id','village','name','sort','color']

class MicroGridDetailSerializer(serializers.ModelSerializer):
    village_name = serializers.SerializerMethodField('get_village_name')
    houses_count = serializers.SerializerMethodField('get_houses_count')
    pop_count = serializers.SerializerMethodField('get_pop_count')

    def get_village_name(self,MicroGrid):
        try:
            return MicroGrid.village.name
        except:
            return ''
    
    def get_houses_count(self,MicroGrid):
        try:
            count = House.objects.filter(mgrid=MicroGrid).exclude(deleted=True).count()
            return count
        except:
            return ''
    
    def get_pop_count(self,MicroGrid):
        try:
            houses = House.objects.filter(mgrid=MicroGrid).exclude(deleted=True)
            count = 0
            for house in houses:
                #print(house.pop)
                count += int(house.pop)
            return count
        except:
            return 'x'

    class Meta:
        model = MicroGrid
        fields = '__all__'

class CustomStaticsTemplateDetailSerializer(serializers.ModelSerializer):
    range_display = serializers.SerializerMethodField('get_range_display')
    object_display = serializers.SerializerMethodField('get_object_display')
    creater_display = serializers.SerializerMethodField('get_creater_display')

    def get_range_display(self,CustomStaticsTemplate):
        if CustomStaticsTemplate.range == 'v':
            return CustomStaticsTemplate.village.name
        elif CustomStaticsTemplate.range == 'g':
            return str(CustomStaticsTemplate.mgrid)
    
    def get_object_display(self,CustomStaticsTemplate):
        return CustomStaticsTemplate.display_object()
    
    def get_creater_display(self,CustomStaticsTemplate):
        return CustomStaticsTemplate.creater.username

    class Meta:
        model = CustomStaticsTemplate
        fields = '__all__'

from django.utils import timezone

class CustomStaticsInstanceSerializer(serializers.ModelSerializer):
    object_pk = serializers.SerializerMethodField('get_object_pk')
    creater_display = serializers.SerializerMethodField('get_creater_display')
    update_time_display = serializers.SerializerMethodField('get_update_time_display')

    def get_update_time_display(self,CustomStaticsInstance):
        datetime = timezone.localtime(CustomStaticsInstance.update_time)
        return datetime.strftime('%Y-%m-%d %H:%M')

    def get_object_pk(self,CustomStaticsInstance):
        template = CustomStaticsInstance.template
        #print(template.obj)
        if template.obj == 'r':
            return CustomStaticsInstance.resident.pk
        elif template.obj == 'h':
            return CustomStaticsInstance.house.pk
        elif template.obj == 'g':
            return CustomStaticsInstance.mgrid.pk

    def get_creater_display(self,CustomStaticsInstance):
        return CustomStaticsInstance.creater.username

    class Meta:
        model = CustomStaticsInstance
        fields = '__all__'