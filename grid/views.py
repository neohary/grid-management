from django.shortcuts import render
from rest_framework import status,viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import ForeignKey,OneToOneField

from .models import *
from .serializer import *
from resident.serializer import HouseDetailSerializer,ResidentDetailSerializer
from index.models import VillageChangeLog,MicroGridChangeLog,CustomStaticsInstanceChangeLog,CustomStaticsTemplateChangeLog
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
import resident
from resident.views import find
from grid import serializer

from notifications.signals import notify
from django.db.models import Q
# Create your views here.
def village_changelog(object,context,behaviour,user):
    VillageChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    resident.views.changelogger("",True)

def microgrid_changelog(object,context,behaviour,user):
    MicroGridChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    resident.views.changelogger("",True)

def customstaticsinstance_changelog(object,context,behaviour,user):
    CustomStaticsInstanceChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    resident.views.changelogger("",True)

def customstaticstemplate_changelog(object,context,behaviour,user):
    CustomStaticsTemplateChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    resident.views.changelogger("",True)

###village
fake_village_name = "FAKE_VILLAGE"
class VillageViewSet(viewsets.ViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        queryset = Village.objects.all().exclude(deleted=True)
        serializer = VillageSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('grid.can_see_village'):
            village = get_object_or_404(Village,pk=pk)
            if village.deleted == False:
                serializer = VillageSerializer(village)
            else:
                return Response({'message':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)
            
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        if request.user.has_perm('grid.can_c/d_village'):
            serializer = VillageSerializer(data=request.data)
            village = Village.objects.filter(name=request.data['name']).exists()
            if not village:
                if serializer.is_valid():
                    serializer.save()
                    obj = Village.objects.get(pk=serializer.data['id'])
                    village_changelog(
                        obj,
                        '{} 创建了 {}'.format(request.user,obj),
                        'c',
                        request.user
                    )
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'已存在同名村庄'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        if request.user.has_perm('grid.can_c/d_village'):
            village = Village.objects.get(pk=pk)
            if village.deleted == False:
                village.delete()
                users = village.get_users()
                for user in users:
                    user.profile.village = None
                    user.profile.mgrid = None
                    user.profile.save()
                    user.groups.clear()
                    group = Group.objects.filter(name="未授权").get()
                    user.groups.add(group)
                    notify.send(sender=request.user,recipient=user,verb="{} 删除了 {}，所以你的权限已被重置，请联系管理员".format(request.user,village))
                village_changelog(
                    village,
                    '{} 删除了 {}'.format(request.user,village),
                    'd',
                    request.user
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk):
        village = get_object_or_404(Village,pk=pk)
        if request.user.has_perm('grid.can_edit_village'):
            global fake_village_name
            if 'name' in request.data:
                pass
            else:
                request.data['name'] = fake_village_name

            serializer = VillageSerializer(data=request.data)

            if serializer.is_valid():
                i = 0
                for field in Village._meta.fields:
                    setattr(village,field.name,find(eval('village.{}'.format(field.name)),field.name,serializer,'name',fake_village_name))
                    i += 1
                village.save()
                village_changelog(
                    village,
                    resident.views.text,
                    'u',
                    request.user
                )
                notify.send(sender=request.user,recipient=village.get_managers(),verb="{} 修改了村庄信息".format(request.user))
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            villages = Village.objects.all().exclude(deleted=True)
        elif request.user.has_perms(['grid.can_see_village','grid.village_mark_village']):
            t_village = request.user.profile.village
            villages = Village.objects.filter(pk=t_village.pk).exclude(deleted=True)
        elif request.user.has_perms(['grid.can_see_village','grid.mgrid_mark_village']):
            t_village = request.user.profile.mgrid.village
            villages = Village.objects.filter(pk=t_village.pk).exclude(deleted=True)
        
        s_villages = VillageSerializer(villages,many=True)
        return Response({"villages":s_villages.data},status=status.HTTP_200_OK)

    @action(detail=True,methods=['get'])
    def get_mgrids(self,request,pk):
        if request.user.has_perm('grid.can_see_village'):
            t_village = get_object_or_404(Village,pk=pk)
            if t_village.deleted == False:
                mgrids = MicroGrid.objects.filter(village=t_village).exclude(deleted=True)
                serializer = MicroGridDetailSerializer(mgrids,many=True)
                return Response({"mgrids":serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"message":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['get'])
    def get_residents(self,request,pk):
        if request.user.has_perm('grid.can_see_village'):
            village = get_object_or_404(Village,pk=pk)
            if village == request.user.profile.village or request.user.is_superuser:
                if village.deleted == False:
                    houses = House.objects.filter(village=village).exclude(deleted=True)
                    resident_list = None
                    for house in houses:
                        residents = Resident.objects.filter(b_house=house).exclude(deleted=True)
                        if resident_list == None:
                            resident_list = residents
                        else:
                            resident_list = resident_list | residents
                    serializer = ResidentDetailSerializer(resident_list,many=True)
                    return Response({"residents":serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['get'])
    def get_houses(self,request,pk):
        if request.user.has_perm('grid.can_see_village'):
            village = get_object_or_404(Village,pk=pk)
            if village == request.user.profile.village or request.user.is_superuser:
                if village.deleted == False:
                    houses = House.objects.filter(village=village).exclude(deleted=True)
                    serializer = HouseDetailSerializer(houses,many=True)
                    return Response({"houses":serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)

###microgrid
class MicroGridViewSet(viewsets.ViewSet):
    queryset = MicroGrid.objects.all()
    serializer_class = MicroGridDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        if request.user.is_superuser:
            queryset = MicroGrid.objects.all().exclude(deleted=True)
            serializer = MicroGridDetailSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('grid.can_see_mgrid'):
            obj = get_object_or_404(MicroGrid,pk=pk)
            if request.user.profile.village == obj.village or request.user.is_superuser:
                if obj.deleted == False:
                    serializer = MicroGridDetailSerializer(obj)
                else:
                    return Response({'message':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)
                return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        if request.user.has_perm('grid.can_c/d_mgrid'):
            serializer = MicroGridDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                obj = MicroGrid.objects.get(pk=serializer.data['id'])
                microgrid_changelog(
                    obj,
                    '{} 创建了 {}'.format(request.user,obj),
                    'c',
                    request.user
                )
                return Response(serializer.data)
                notify.send(sender=request.user,recipient=obj.village.get_managers(),verb="{} 创建了 {}".format(request.user,obj))
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        if request.user.has_perm('grid.can_c/d_mgrid'):
            obj = MicroGrid.objects.get(pk=pk)
            if request.user.profile.village == obj.village or request.user.is_superuser:
                if obj.deleted == False:
                    obj.delete()
                    houses = House.objects.filter(mgrid=obj).exclude(deleted=True)
                    for house in houses:
                        residents = Resident.objects.filter(b_house=house).exclude(deleted=True)
                        for res in residents:
                            res.delete()
                        house.delete()

                    users = User.objects.filter(profile__mgrid=obj)
                    grid = MicroGrid.objects.filter(village=obj.village).exclude(deleted=True).latest()
                    for user in users:
                        if grid:
                            user.profile.mgrid = grid
                        else:
                            user.profile.mgrid = None
                        user.profile.save()
                        notify.send(sender=request.user,recipient=user,verb="{} 删除了 {}，你的所属微网格已被重新分配，如果发现异常请联系管理员".format(request.user,obj))

                    microgrid_changelog(
                        obj,
                        '{} 删除了 {}'.format(request.user,obj),
                        'd',
                        request.user
                    )
                    notify.send(sender=request.user,recipient=obj.village.get_managers(),verb="{} 删除了 {}".format(request.user,obj))
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        if request.user.has_perm('grid.can_edit_mgrid'):
            obj = get_object_or_404(MicroGrid,pk=pk)
            if request.user.profile.village == obj.village or request.user.is_superuser:
                serializer = MicroGridDetailSerializer(data=request.data)

                if serializer.is_valid():
                    fk_list = [Village]
                    i = 0
                    for field in MicroGrid._meta.fields:
                        if i < len(fk_list):
                            setattr(obj,field.name,find(eval('obj.{}'.format(field.name)),field.name,serializer,'','',fk_list[i]))
                        else:
                            setattr(obj,field.name,find(eval('obj.{}'.format(field.name)),field.name,serializer,'',''))
                        i += 1
                    obj.save()
                    microgrid_changelog(
                        obj,
                        resident.views.text,
                        'u',
                        request.user
                    )
                    return Response(serializer.data,status=status.HTTP_200_OK)
                    notify.send(sender=request.user,recipient=obj.village.get_managers(),verb="{} 修改了 {} 的信息".format(request.user,obj))
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            mgrids = MicroGrid.objects.all().exclude(deleted=True)
        elif request.user.has_perms(['grid.can_see_mgrid','grid.village_mark_mgrid']):
            t_village = request.user.profile.village
            mgrids = MicroGrid.objects.filter(village=t_village).exclude(deleted=True)
        elif request.user.has_perms(['grid.can_see_mgrid','grid.mgrid_mark_mgrid']):
            mgrids = MicroGrid.objects.filter(pk=request.user.profile.mgrid.pk)
        
        s_mgrids = MicroGridDetailSerializer(mgrids,many=True)
        return Response({"mgrids":s_mgrids.data},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['get'])
    def get_houses(self,request,pk):
        if request.user.has_perm('grid.can_see_mgrid'):
            mgrid = get_object_or_404(MicroGrid,pk=pk)
            if request.user.profile.village == mgrid.village or request.user.is_superuser:
                if mgrid.deleted == False:
                    houses = House.objects.filter(mgrid=mgrid).exclude(deleted=True)

                    s_houses = HouseDetailSerializer(houses,many=True)
                    return Response({"houses":s_houses.data},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True,methods=['get'])
    def get_residents(self,request,pk):
        if request.user.has_perm('grid.can_see_mgrid'):
            mgrid = get_object_or_404(MicroGrid,pk=pk)
            if request.user.profile.village == mgrid.village or request.user.is_superuser:
                if mgrid.deleted == False:
                    houses = House.objects.filter(mgrid=mgrid).exclude(deleted=True)
                    resident_list = None
                    for house in houses:
                        residents = Resident.objects.filter(b_house=house).exclude(deleted=True)
                        if resident_list == None:
                            resident_list = residents
                        else:
                            resident_list = resident_list | residents
                    serializer = ResidentDetailSerializer(resident_list,many=True)
                    return Response({"residents":serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
###microgrid end
###customstaticsinstance
class sTemplateViewSet(viewsets.ViewSet):
    serializer_class = CustomStaticsTemplateDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        if request.is_superuser:
            queryset = CustomStaticsTemplate.objects.all().exclude(deleted=True)
            serializer = CustomStaticsTemplateDetailSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('grid.can_see_stemplate'):
            obj = get_object_or_404(CustomStaticsTemplate,pk=pk)
            if obj.village == request.user.profile.village or obj.range == 'a':
                if obj.deleted == False:
                    serializer = CustomStaticsTemplateDetailSerializer(obj)
                else:
                    return Response({'detail':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)
                return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        if request.user.has_perm('grid.can_cd_stemplate'):
            request.data['creater'] = request.user.pk
            if request.data['range'] != 'all':
                print(request.data['range'])
                request.data['village'] = get_object_or_404(Village,pk=request.data['range'])
                request.data['range'] = 'v'
            elif request.data['range'] == 'all':
                request.data['range'] = 'a'
            
            serializer = CustomStaticsTemplateDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                obj = CustomStaticsTemplate.objects.get(pk=serializer.data['id'])
                customstaticstemplate_changelog(
                    obj,
                    '{} 创建了统计： {}'.format(request.user,obj),
                    'c',
                    request.user
                )
                return Response(serializer.data)
                notify.send(sender=request.user,recipient=obj.village.get_users(),verb="{} 创建了统计 {}".format(request.user,obj))
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        if request.user.has_perm('grid.can_cd_stemplate'):
            obj = CustomStaticsTemplate.objects.get(pk=pk)
            if obj.deleted == False:
                obj.delete()
                customstaticstemplate_changelog(
                    obj,
                    '{} 删除了统计： {}'.format(request.user,obj),
                    'd',
                    request.user
                )
                notify.send(sender=request.user,recipient=obj.village.get_users(),verb="{} 删除了统计 {}".format(request.user,obj))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            sTemplate = CustomStaticsTemplate.objects.all().exclude(deleted=True)
        elif request.user.has_perms(['grid.village_mark_stemplate','grid.can_see_stemplate']):
            t_village = request.user.profile.village
            sTemplate = CustomStaticsTemplate.objects.filter(Q(village=t_village) | Q(range='a') ).exclude(deleted=True)
        elif request.user.has_perms(['grid.mgrid_mark_stemplate','grid.can_see_stemplate']):
            t_village = request.user.profile.village
            #t_mgrid = request.user.profile.mgrid
            sTemplate = CustomStaticsTemplate.objects.filter(Q(village=t_village) | Q(range='a')).exclude(deleted=True)
        
        s_sTemplate = CustomStaticsTemplateDetailSerializer(sTemplate,many=True)
        return Response({"sTemplate":s_sTemplate.data},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['get'])
    def get_instances(self,request,pk):
        if request.user.has_perm('grid.can_see_stemplate'):
            sTemplate = get_object_or_404(CustomStaticsTemplate,pk=pk)
            if(sTemplate.deleted == False):
                instances = CustomStaticsInstance.objects.filter(template=sTemplate).exclude(deleted=True)
                s_instances = CustomStaticsInstanceSerializer(instances,many=True)
                return Response({'instances':s_instances.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"request not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['delete'])
    def close(self,request,pk):
        if request.user.has_perm('grid.can_cd_stemplate'):
            sTemplate = get_object_or_404(CustomStaticsTemplate,pk=pk)
            if(sTemplate.deleted == False and sTemplate.closed == False):
                sTemplate.close()
                notify.send(sender=request.user,recipient=sTemplate.village.get_users(),verb="{} 关闭了统计 {}".format(request.user,sTemplate))
                return Response({"detail":"closed"},status=status.HTTP_200_OK)
            else:
                return Response({"error":"request not found or already closed"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
###
###CustomStaticsTemplate

class sInstanceViewSet(viewsets.ViewSet):
    serializer_class = CustomStaticsInstanceSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        if request.user.is_superuser:
            queryset = CustomStaticsInstance.objects.all().exclude(deleted=True)
            serializer = CustomStaticsInstanceSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('grid.can_see_sinstance'):
            obj = get_object_or_404(CustomStaticsInstance,pk=pk)
            if obj.deleted == False:
                serializer = CustomStaticsInstanceSerializer(obj)
            else:
                return Response({'detail':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        #检测object pk和template pk的唯一性，如果重复则调用update
        if request.user.has_perm('grid.can_c/d_sinstance'):
            request.data['creater'] = request.user.pk
            serializer = CustomStaticsInstanceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                obj = CustomStaticsInstance.objects.get(pk=serializer.data['id'])
                customstaticsinstance_changelog(
                    obj,
                    '{} 创建了 {}'.format(request.user,obj),
                    'c',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 填写了统计 {}".format(request.user,obj.template))
                notify.send(sender=request.user,recipient=request.user,verb="你填写了统计 {}".format(obj.template))
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        if request.user.has_perm('grid.can_c/d_sinstance'):
            obj = CustomStaticsInstance.objects.get(pk=pk)
            if obj.deleted == False:
                obj.delete()
                customstaticsinstance_changelog(
                    obj,
                    '{} 删除了 {}'.format(request.user,obj),
                    'd',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 撤回了统计 {}".format(request.user,obj.template))
                notify.send(sender=request.user,recipient=request.user,verb="你撤回了统计 {}".format(obj.template))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        if request.user.has_perm('grid.can_edit_sinstance'):
            obj = get_object_or_404(CustomStaticsInstance,pk=pk)
            serializer = CustomStaticsInstanceSerializer(data=request.data)

            if serializer.is_valid():
                fk_list = [None,CustomStaticsTemplate,Resident,House,MicroGrid,None,None,User]
                i = 0
                for field in CustomStaticsInstance._meta.fields:
                    if i < len(fk_list):
                        setattr(obj,field.name,find(eval('obj.{}'.format(field.name)),field.name,serializer,'','',fk_list[i]))
                    else:
                        setattr(obj,field.name,find(eval('obj.{}'.format(field.name)),field.name,serializer,'',''))
                    i += 1
                obj.save()
                customstaticsinstance_changelog(
                    obj,
                    resident.views.text,
                    'u',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} 更新了统计 {}".format(request.user,obj.template))
                notify.send(sender=request.user,recipient=request.user,verb="你更新了统计 {}".format(obj.template))
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'权限不足'},status=status.HTTP_400_BAD_REQUEST)