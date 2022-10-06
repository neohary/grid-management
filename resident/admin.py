from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Resident._meta.fields]
    search_fields = ['name','IDnumber','sex','phone']

class ResidentInline(admin.TabularInline):
    model = Resident

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in House._meta.fields]
    inlines = [ResidentInline]