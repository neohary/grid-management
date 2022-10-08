from rest_framework import serializers
from .models import *

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id','name','IDnumber','age']

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id','village','mgrid','mgridID','population']

class ResidentDetailSerializer(serializers.ModelSerializer):
    house_name = serializers.SerializerMethodField('get_house_name')
    age = serializers.SerializerMethodField('get_age')
    sex_display = serializers.SerializerMethodField('get_sex_display_ser')
    village = serializers.SerializerMethodField('get_village')
    mgrid = serializers.SerializerMethodField('get_mgrid')

    def get_house_name(self,Resident):
        try:
            return str(Resident.b_house)
        except:
            return ''

    def get_age(self,Resident):
        #print(Resident.IDnumber)
        try:
            return Resident.age
        except:
            return ''
    
    def get_sex_display_ser(self,Resident):
        try:
            return Resident.get_sex_display()
        except:
            return ''
    
    def get_village(self,Resident):
        try:
            village = Resident.b_house.village
        except:
            return [None,None]
        if village:
            return [village.name,village.pk]
    
    def get_mgrid(self,Resident):
        try:
            mgrid = Resident.b_house.mgrid
        except:
            return [None,None]
        if mgrid:
            return [mgrid.name,mgrid.pk]

    class Meta:
        model = Resident
        fields = "__all__"

class HouseDetailSerializer(serializers.ModelSerializer):
    house_name = serializers.SerializerMethodField('get_house_name')
    grid_name = serializers.SerializerMethodField('get_mgrid_name')
    holder_name = serializers.SerializerMethodField('get_holder_name')
    village_name = serializers.SerializerMethodField('get_village_name')
    have_geo = serializers.SerializerMethodField('have_geo')
    pop_count = serializers.SerializerMethodField('get_pop_count')
    mgrid_color = serializers.SerializerMethodField('get_mgrid_color')
    short_name = serializers.SerializerMethodField('get_sort_name')

    def get_sort_name(self,House):
        try:
            return "{} <br> {}户".format(House.mgrid.name,House.mgridID)
        except:
            return ''

    def get_mgrid_color(self,House):
        try:
            return House.mgrid.color
        except:
            return '#E3E3E3'

    def get_house_name(self,House):
        try:
            return str(House)
        except:
            return ''
    
    def get_mgrid_name(self,House):
        try:
            return House.mgrid.name
        except:
            return ''
    
    def get_holder_name(self,House):
        try:
            return House.holder.name
        except:
            return ''

    def get_village_name(self,House):
        try:
            return House.village.name
        except:
            return ''
    
    def have_geo(self,House):
        if House.geo:
            return True
        else:
            return False
    
    def get_pop_count(self,House):
        try:
            count = Resident.objects.filter(b_house=House).exclude(deleted=True).count()
            return count
        except:
            return ''

    class Meta:
        model = House
        fields = "__all__"