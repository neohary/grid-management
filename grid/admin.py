from django.contrib import admin
from .models import *
from resident.models import House
from django.contrib.auth.admin import UserAdmin,GroupAdmin
# Register your models here.

class MicroGridInline(admin.TabularInline):
    model = MicroGrid

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['name','houses','mgrids','population','deleted']
    search_fields = ['name']
    inlines = [MicroGridInline]

class HouseInline(admin.TabularInline):
    model = House

@admin.register(MicroGrid)
class MicroGridAdmin(admin.ModelAdmin):
    list_display = ['village','sort','name','houses','population']
    inlines = [HouseInline]
    search_fields = ['village__name','name']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin,self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'GroupProfile'
    fk_name = 'group'

class CustomGroupAdmin(GroupAdmin):
    inlines = (GroupProfileInline, )

    def get_inline_instances(self,request,obj=None):
        if not obj:
            return list()
        return super(CustomGroupAdmin,self).get_inline_instances(request,obj)

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

@admin.register(CustomStaticsTemplate)
class sTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomStaticsTemplate._meta.fields]

@admin.register(CustomStaticsInstance)
class sinstanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomStaticsInstance._meta.fields]
