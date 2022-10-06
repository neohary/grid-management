from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ResidentChangeLog)
class ResidentChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(HouseChangeLog)
class HouseChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(VillageChangeLog)
class VillageChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(MicroGridChangeLog)
class MicroGridChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(CustomStaticsTemplateChangeLog)
class CustomStaticsTemplateChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(CustomStaticsInstanceChangeLog)
class CustomStaticsInstanceChangeLogAdmin(admin.ModelAdmin):
    list_display =  ['object','behaviour','changeby','changetime']
    search_fields = ['object','behaviour','changeby','changetime']

@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserLoginLog._meta.fields]
    search_fields = [field.name for field in UserLoginLog._meta.fields]