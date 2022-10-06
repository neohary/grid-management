from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(customParameter)
class customParameterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in customParameter._meta.fields]

@admin.register(NavbarTab)
class NavbarTabAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NavbarTab._meta.fields]

@admin.register(UserApproval)
class UserApprovalTabAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApproval._meta.fields]