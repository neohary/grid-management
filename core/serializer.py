from rest_framework import serializers
from django.contrib.auth.models import User,Group
from grid.models import Profile,GroupProfile
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from .models import UserApproval
from django.utils import timezone

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField('get_user_phone')
    village = serializers.SerializerMethodField('get_user_village')
    mgrid = serializers.SerializerMethodField('get_user_mgrid')
    groups = serializers.SerializerMethodField('get_groups')
    groups_display = serializers.SerializerMethodField('get_group_display')
    last_login_display = serializers.SerializerMethodField('get_last_login_display')
    name = serializers.SerializerMethodField('get_name')

    def get_name(self,User):
        try:
            return User.profile.name
        except:
            return User.username

    def get_user_phone(self,User):
        try:
            return User.profile.phone
        except:
            return ''
    
    def get_user_village(self,User):
        try:
            return [User.profile.village.name,User.profile.village.id]
        except:
            return ''
    
    def get_user_mgrid(self,User):
        try:
            return [str(User.profile.mgrid),User.profile.mgrid.id]
        except:
            return ''
    
    def get_group_display(self,User):
        try:
            result = []
            for group in User.groups.all():
                html = '<span class="badge bg-danger mx-1">{}</span>'.format(group.name)
                result.append(html)
            return result
        except:
            return ''
    
    def get_groups(self,User):
        result = []
        for group in User.groups.all():
            result.append([group.name,group.id])
        return result
    
    def get_last_login_display(self,User):
        datetime = timezone.localtime(User.last_login)
        return datetime.strftime('%Y-%m-%d %H:%M')

    class Meta:
        model = UserModel
        fields = ['id','last_login_display','name','username','phone','email','village','mgrid','groups','groups_display','is_active']

class GroupSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField('get_color')
    description = serializers.SerializerMethodField('get_description')
    avaliable = serializers.SerializerMethodField('get_avaliable')

    def get_color(self,Group):
        try:
            return Group.groupprofile.color
        except:
            return '#E3E3E3'
    
    def get_description(self,Group):
        try:
            return Group.groupprofile.description
        except:
            return ''
    
    def get_avaliable(self,Group):
        try:
            return Group.groupprofile.avaliable
        except:
            return False

    class Meta:
        model = Group
        fields = ['id','name','color','description','avaliable']

class CreateUserSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self,validated_data):
        user = User.objects.filter(email=validated_data['email']).exists()
        if user:
            raise BadRequest('该邮箱已被注册')

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )

        user.profile.phone = validated_data['phone']
        try:
            user.profile.save()
        except:
            user.delete()
            raise BadRequest('该手机号已被注册')

        return user

    class Meta:
        model = UserModel
        fields = ['id','username','email','phone','password']

class UserApprovalSerializer(serializers.ModelSerializer):
    village_display = serializers.SerializerMethodField('get_village_display')
    mgrid_display = serializers.SerializerMethodField('get_mgrid_display')
    user_name = serializers.SerializerMethodField('get_user_name')
    create_time_display = serializers.SerializerMethodField('get_ctime_display')
    status_display = serializers.SerializerMethodField('get_status_display')

    class Meta:
        model = UserApproval
        fields = '__all__'
    
    def get_village_display(self,UserApproval):
        try:
            return UserApproval.village.name
        except:
            return ''
    
    def get_mgrid_display(self,UserApproval):
        try:
            return UserApproval.mgrid.name
        except:
            return ''
    
    def get_user_name(self,UserApproval):
        try:
            return UserApproval.user.username
        except:
            return ''
    
    def get_ctime_display(self,UserApproval):
        datetime = timezone.localtime(UserApproval.create_time)
        return datetime.strftime('%Y-%m-%d %H:%M')

    def get_status_display(self,UserApproval):
        try:
            result = UserApproval.get_status_display()
            return result
        except:
            return ''