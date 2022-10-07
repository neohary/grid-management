from django.shortcuts import render
from rest_framework import status,viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializer import *
from django.contrib.auth.models import User,Group
from grid.models import Profile,GroupProfile
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate,logout
from .models import UserApproval

from notifications.signals import notify
from resident.views import find
from grid.models import *
# Create your views here.

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def list(self,request):
        if request.user.is_superuser:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        obj = get_object_or_404(User,pk=pk)
        if request.user == obj or request.user.has_perm('grid.can_see_user'):
            serializer = UserSerializer(obj)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            queryset = User.objects.all()
        elif request.user.has_perms(['grid.can_see_user','grid.village_mark_user']):
            t_village = request.user.profile.village
            queryset = User.objects.filter(profile__village=t_village)
        elif request.user.has_perms(['grid.can_see_user','grid.mgrid_mark_user']):
            t_mgrid = request.user.profile.mgrid
            queryset = User.objects.filter(profile__mgrid=t_mgrid)
        serializer = UserSerializer(queryset,many=True)
        return Response({'users':serializer.data},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['delete'])
    def kick(self,request,pk):
        if request.user.has_perm('grid.can_edit_user'):
            obj = get_object_or_404(User,pk=pk)
            if obj == request.user:
                return Response({'message':'你不能移除自己，如果需要移除自己，请联系管理员'},status=status.HTTP_400_BAD_REQUEST)
            obj.groups.clear()
            group = Group.objects.filter(name="未授权").get()
            obj.groups.add(group)
            obj.profile.village = None
            obj.profile.mgrid = None
            obj.profile.save()
            notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 移除了用户 {}".format(request.user,obj))
            notify.send(sender=request.user,recipient=obj,verb="{} 将你移出了 {}".format(request.user,request.user.profile.village))
            return Response({'message':'success'},status=status.HTTP_200_OK)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['post'])
    def set_group(self,request,pk):
        if request.user.has_perm('grid.can_edit_user'):
            obj = get_object_or_404(User,pk=pk)
            data = request.data['groups']
            if obj.groups.filter(name="村管理员").exists() or obj.is_superuser:
                temp = Group.objects.filter(name="村管理员").first()
                if temp.pk in data:
                    pass
                else:
                    if request.user.is_superuser:
                        pass
                    else:
                        return Response({'message':'无法修改管理员的权限'},status=status.HTTP_400_BAD_REQUEST)
            obj.groups.clear()
            base_g = Group.objects.filter(name="基础授权").get()
            obj.groups.add(base_g)
            for g in data:
                group = Group.objects.filter(pk=g).get()
                obj.groups.add(group)
            notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 更新了用户 {} 的权限".format(request.user,obj))
            notify.send(sender=request.user,recipient=obj,verb="{} 更新了你的权限".format(request.user))
            return Response({'message':'success'},status=status.HTTP_200_OK)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        if request.user.has_perm('grid.can_edit_user') or (request.user == user):
            serializer = self.serializer_class(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                profile_keys = ['village','mgrid','phone','r_name']
                for key in profile_keys:
                    if key in request.data:
                        if key == 'village':
                            village = Village.objects.get(pk=request.data[key])
                            setattr(user.profile,key,village)
                        elif key == 'mgrid':
                            mgrid = MicroGrid.objects.get(pk=request.data[key])
                            setattr(user.profile,key,mgrid)
                        else:
                            setattr(user.profile,key,request.data[key])
                        user.profile.save()

                if request.user != user:
                    notify.send(sender=request.user,recipient=user,verb="{} 修改了你的信息".format(request.user))
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = CreateUserSerializer

import re

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

class LoginView(APIView):
    def post(self,request):
        #print(request.data)
        username = request.data['username']
        passwd = request.data['password']
        
        if username.isnumeric() and len(username) == 11:
            user = User.objects.filter(profile__phone=username).first()
        elif check(username):
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if user == None:
            return Response({'message':"用户不存在"},status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(passwd):
            return Response({'message':"账号或密码错误"},status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.is_active:
                login(request,user)
                return Response({'message':"登录成功"},status=status.HTTP_200_OK)
            else:
                return Response({'message':"你的账户已被停用，请联系管理员"},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':"未知错误"},status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message':"登出成功"},status=status.HTTP_200_OK)
        else:
            return Response({'message':"您已登出"},status=status.HTTP_200_OK)

class GroupViewSet(viewsets.ViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        if request.user.is_superuser:
            queryset = Group.objects.all().exclude(groupprofile__avaliable=False)
            serializer = GroupSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        obj = get_object_or_404(Group,pk=pk)
        serializer = GroupSerializer(obj)
        return Response(serializer.data)
    
    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            queryset = Group.objects.all().exclude(groupprofile__avaliable=False)
        elif request.user.has_perm('grid.can_see_group'):
            queryset = Group.objects.all().exclude(name="全域管理员").exclude(name="全域查看").exclude(name="未授权").exclude(name="基础授权").exclude(groupprofile__avaliable=False)
        else:
            return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupSerializer(queryset,many=True)
        return Response(serializer.data)

class UserApprovalViewSet(viewsets.ViewSet):
    queryset = UserApproval.objects.all()
    serializer_class = UserApprovalSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        if request.user.is_superuser:
            queryset = UserApproval.objects.all()
            serializer = UserApprovalSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('core.can_see_approvals'):
            obj = get_object_or_404(UserApproval,pk=pk)
            serializer = UserApprovalSerializer(obj)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        request.data['user'] = request.user.pk
        if request.user.has_perm('core.can_c/d_approvals'):
            serializer = UserApprovalSerializer(data=request.data)
            if serializer.is_valid():
                obj = UserApproval.objects.filter(user=request.user).exclude(status='x').exists()
                if obj:
                    return Response({'message',"已有正在进行中的申请"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        obj = get_object_or_404(UserApproval,pk=pk)
        if request.user.has_perm('core.can_c/d_approvals') and (obj.user == request.user):
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':"权限不足"},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def get_living(self,request):
        if request.user.has_perm('core.can_see_approvals'):
            user = request.user
            queryset = UserApproval.objects.filter(village=user.profile.village).exclude(status='x')
            serializer = UserApprovalSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['post'])
    def approve(self,request,pk):
        if request.user.has_perm('core.can_deal_approvals'):
            obj = get_object_or_404(UserApproval,pk=pk)
            if obj.status == 'o':
                if request.data['result'] == 'a':
                    obj.result = 'a'
                    obj_user = obj.user
                    obj_user.profile.village = obj.village
                    if obj.mgrid:
                        obj_user.profile.mgrid = obj.mgrid
                    obj_user.profile.save()
                    group = Group.objects.get(name="未授权")
                    obj_user.groups.remove(group)
                    group = Group.objects.get(name="基础授权")
                    obj_user.groups.add(group)
                    #把用户添加到基础权限组里
                    notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 同意了 {} 的申请".format(request.user,obj_user))
                    notify.send(sender=request.user,recipient=obj_user,verb="{} 同意了你的申请".format(request.user))
                else:
                    obj.result = 'd'
                    #其他拒绝逻辑
                    notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 拒绝了 {} 的申请".format(request.user,obj_user))
                    notify.send(sender=request.user,recipient=obj_user,verb="{} 拒绝了你的申请".format(request.user))
                obj.approval_by = request.user
                obj.close()
                return Response({'message':'success'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'该审批已经结束'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['get'])
    def get_live_by_user(self,request):
        obj = UserApproval.objects.filter(user=request.user).exclude(status='x').first()
        
        if obj: #用户自己查看自己的申请
            if obj.user == request.user:
                serializer = UserApprovalSerializer(obj)
                return Response(serializer.data)
            return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False,methods=['get'])
    def get_live_by_village(self,request):
        if request.user.has_perm('core.can_see_approvals'):
            obj = UserApproval.objects.filter(village=request.user.profile.village).exclude(status='x')
            if obj:
                serializer = UserApprovalSerializer(obj,many=True)
                return Response(serializer.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)