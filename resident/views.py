from rest_framework import status,viewsets

from .models import *
from .serializer import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import ForeignKey,OneToOneField
from django.http import JsonResponse,QueryDict
from grid.serializer import *
from django.core import serializers as JSserializers

# Create your views here.
from index.models import ResidentChangeLog,HouseChangeLog

from notifications.signals import notify
from django.db import transaction

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def resident_changelog(object,context,behaviour,user):
    ResidentChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    changelogger("",True)

text = ""
fake_IDnumber = '371423199808042214'
fake_resident_name = 'JONE DOE'

def fake_request(request,str:str,fakevalue):
    if str in request.data:
            pass
    else:
        request.data[str] = fakevalue
        return request.data

def changelogger(context,clear):
    global text
    if clear:
        text = ""
    else:
        text += context + '\n'

def get_or_null(Model,key):
    try:
        result = Model.objects.get(pk=key)
    except :
        return None
    return result

def find(value,request,serializer,excludeStr:str,excludeFKv,*args):
    if request in serializer.data and serializer.data[request] != None:
        if bool(excludeStr and excludeFKv) and bool(request == excludeStr and serializer.data[request] == excludeFKv):
            pass
        else:
            object = serializer.Meta.model._meta.get_field(request)
            changelogger(
            "{}: {} -> {}".format(
                object.help_text,
                str(value)[:30],
                str(serializer.data[request])[:30]),
                False
                )
            if isinstance(object,ForeignKey) or isinstance(object,OneToOneField):
                value = get_or_null(args[0],serializer.data[request])
            else:
                value = serializer.data[request]
    else:
        value = value
    #print("{} : {}".format(request,value))
    return value

class ResidentViewSet(viewsets.ViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        if request.user.is_superuser:
            queryset = Resident.objects.all()
            serializer = ResidentSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        resident = get_object_or_404(Resident,pk=pk)
        if request.user.has_perm('resident.can_see_resident'):
            if resident.deleted == False:
                serializer = ResidentDetailSerializer(resident)
            else:
                return Response({'detail':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def create(self,request):
        if request.user.has_perm('resident.can_c/d_resident'):
            serializer = ResidentDetailSerializer(data=request.data)
            if serializer.is_valid():
                resident = Resident.objects.filter(IDnumber=request.data['IDnumber']).exclude(deleted=True).exists()
                if(resident):
                    return Response({'error':"??????????????????????????????????????????"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                obj = Resident.objects.get(pk=serializer.data['id'])
                resident_changelog(
                    obj,
                    '{} ????????? {}'.format(request.user,obj),
                    'c',
                    request.user
                    )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {}".format(request.user,obj))
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self,request,pk):
        if request.user.has_perm('resident.can_c/d_resident'):
            resident = Resident.objects.get(pk=pk)
            if resident.deleted == False:
                resident.delete()
                resident_changelog(
                    resident,
                    '{} ????????? {}'.format(request.user,resident),
                    'd',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {}".format(request.user,resident))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self,request,pk):
        if request.user.has_perm('resident.can_edit_resident'):
            resident = get_object_or_404(Resident,pk=pk)
            global fake_IDnumber
            global fake_resident_name
            fake_request(request,'IDnumber',fake_IDnumber)
            fake_request(request,'name',fake_resident_name)
            serializer = ResidentDetailSerializer(data=request.data)

            if serializer.is_valid():
                fk_list = [None,None,None,None,None,None,None,None,House]
                i = 0
                for field in Resident._meta.fields:
                    if field.name == 'IDnumber':
                        setattr(resident,field.name,find(eval('resident.{}'.format(field.name)),field.name,serializer,'IDnumber',fake_IDnumber))
                    elif field.name == 'name':
                        setattr(resident,field.name,find(eval('resident.{}'.format(field.name)),field.name,serializer,'name',fake_resident_name))
                    else:
                        #print("i:{}, field:{}".format(i,field.name))
                        if i < len(fk_list):
                            setattr(resident,field.name,find(eval('resident.{}'.format(field.name)),field.name,serializer,'','',fk_list[i]))
                        else:
                            setattr(resident,field.name,find(eval('resident.{}'.format(field.name)),field.name,serializer,'',''))
                    i += 1
                resident.save()
                #print(text)
                resident_changelog(
                    resident,
                    text,
                    'u',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {} ?????????".format(request.user,resident))
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
    
    #@transaction.atomic
    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            resident = Resident.objects.all().exclude(deleted=True)
        elif request.user.has_perms(['resident.village_mark_resident','resident.can_see_resident']):
            village = request.user.profile.village
            resident = Resident.objects.filter(b_house__village=village).exclude(deleted=True)
        elif request.user.has_perms(['resident.mgrid_mark_resident','resident.can_see_resident']):
            mgrid = request.user.profile.mgrid
            resident = Resident.objects.filter(b_house__mgrid=mgrid).exclude(deleted=True)
        s_resident = ResidentDetailSerializer(resident,many=True)
        return Response({"residents":s_resident.data},status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def get_no_house(self,request):
        if request.user.has_perm('resident.can_see_resident'):
            resident = Resident.objects.filter(b_house__isnull=True).exclude(deleted=True)
            s_res = ResidentDetailSerializer(resident,many=True)
            return Response({"residents":s_res.data},status=status.HTTP_200_OK)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

def house_changelog(object,context,behaviour,user):
    HouseChangeLog.objects.create(
        object = object,
        context = context,
        behaviour = behaviour,
        changeby = user
    )
    changelogger("",True)

class HouseViewSet(viewsets.ViewSet):
    queryset = House.objects.all()
    serializer_class = HouseDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        if request.user.is_superuser:
            queryset = House.objects.all().exclude(deleted=True)
            serializer = HouseSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        if request.user.has_perm('resident.can_see_house'):
            house = get_object_or_404(House,pk=pk)
            if house.deleted == False:
                serializer = HouseDetailSerializer(house)
            else:
                return Response({'detail':'NOT FOUND.'},status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def create(self,request):
        #print(request.data)
        if request.user.has_perm('resident.can_c/d_house'):
            if(request.data['mgridID'] == 'auto'):
                maxhouse = House.objects.filter(village__id=request.data['village']).filter(mgrid__id=request.data['mgrid']).exclude(deleted=True).order_by('-mgridID').first()
                if maxhouse:
                    request.data['mgridID'] = maxhouse.mgridID + 1
                elif maxhouse == None:
                    request.data['mgridID'] = 1
            elif(request.data['mgridID']):
                matchhouse = House.objects.filter(village__id=request.data['village']).filter(mgrid__id=request.data['mgrid']).filter(mgridID=request.data['mgridID']).exclude(deleted=True).exists()
                if(matchhouse):
                    request.data['mgridID'] += 1

            serializer = HouseDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                obj = House.objects.get(pk=serializer.data['id'])
                house_changelog(
                    obj,
                    '{} ????????? {}'.format(request.user,obj),
                    'c',
                    request.user
                    )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {}".format(request.user,obj))
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self,request,pk):
        if request.user.has_perm('resident.can_c/d_house'):
            house = House.objects.get(pk=pk)
            if house.deleted == False:
                house.delete()
                residents = Resident.objects.filter(b_house=house)
                if residents:
                    for resident in residents:
                        resident.delete()

                house_changelog(
                    house,
                    '{} ????????? {}'.format(request.user,house),
                    'd',
                    request.user
                )
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {}".format(request.user,house))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self,request,pk):
        if request.user.has_perm('resident.can_edit_house'):
            house = get_object_or_404(House,pk=pk)
            if(request.data['mgridID'] == 'auto'):
                maxhouse = House.objects.filter(village__id=request.data['village']).filter(mgrid__id=request.data['mgrid']).order_by('-mgridID').first()
                if maxhouse == house:
                    request.data['mgridID'] = maxhouse.mgridID
                elif maxhouse == None:
                    request.data['mgridID'] = 1
                else:
                    request.data['mgridID'] = maxhouse.mgridID + 1
                
            serializer = HouseDetailSerializer(data=request.data)

            if serializer.is_valid():
                fk_list = [None,MicroGrid,Resident,None,None,Village]
                i = 0
                for field in House._meta.fields:
                    if i < len(fk_list):
                        setattr(house,field.name,find(eval('house.{}'.format(field.name)),field.name,serializer,'','',fk_list[i]))
                    else:
                        setattr(house,field.name,find(eval('house.{}'.format(field.name)),field.name,serializer,'',''))
                    i += 1
                house.save()
                house_changelog(
                    house,
                    text,
                    'u',
                    request.user
                )
                result = HouseDetailSerializer(house,many=False)
                notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ??????????????? {} ?????????".format(request.user,house))
                return Response(result.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False,methods=['get'])
    def get_by_permission(self,request):
        if request.user.is_superuser:
            houses = House.objects.all().exclude(deleted=True)
        elif request.user.has_perms(['resident.can_see_house','resident.village_mark_house']):
            village = request.user.profile.village
            houses = House.objects.filter(village=village).exclude(deleted=True)
        elif request.user.has_perms(['resident.can_see_house','resident.mgrid_mark_house']):
            mgrid = request.user.profile.mgrid
            houses = House.objects.filter(mgrid=mgrid).exclude(deleted=True)
        s_houses = HouseDetailSerializer(houses,many=True)
        return Response({"houses":s_houses.data},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['get'])
    def get_residents(self,request,pk):
        if request.user.has_perm('resident.can_see_house'):
            house = get_object_or_404(House,pk=pk)
            if house:
                residents = Resident.objects.filter(b_house=house).exclude(deleted=True)
                s_res = ResidentDetailSerializer(residents,many=True)
                return Response({'residents':s_res.data},status=status.HTTP_200_OK)
            else:
                return Response({'error':"NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['post'])
    @transaction.atomic
    def set_holder(self,request,pk):
        if request.user.has_perms(['resident.can_edit_house','resident.can_edit_resident']):
            house = get_object_or_404(House,pk=pk)
            holder = get_object_or_404(Resident,pk=request.data['holder'])
            if holder.deleted == False:
                if holder.b_house == house:
                    house.holder = holder
                    house_changelog(
                        house,
                        "???????????????",
                        'u',
                        request.user
                    )
                    house.save()
                    notify.send(sender=request.user,recipient=request.user.profile.village.get_managers(),verb="{} ????????? {} ??? {} ?????????".format(request.user,holder.name,house))
                    return Response({'success':"??????????????????"},status=status.HTTP_200_OK)
                else:
                    return Response({'error':"?????????????????????????????????"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':"????????????????????????"},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'????????????'},status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
from django.core.exceptions import PermissionDenied

def translateSex(text):
    if text == '???':
        return 'm'
    else:
        return 'f'

def translateIsLocal(text):
    if text == '??????':
        return True
    else:
        return False

def get_or_nan(value):
    if not pd.isnull(value):
        return value
    else:
        return None

@transaction.atomic
def batch_add_residents_by_file(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UploadFileForm(request.POST,request.FILES)
            if form.is_valid():
                mgrid = get_object_or_404(MicroGrid,pk=request.POST['mgrid_pk'])
                df = pd.ExcelFile(request.FILES['file']).parse(request.POST['sheet_name'])
                houses = House.objects.filter(mgrid=mgrid).exclude(deleted=True)
                house = None
                i = 0
                messages = []
                resident_count = 0
                house_count = 0
                empty_house_count = 0
                for index,row in df.iterrows():
                    if not pd.isnull(row[0]):
                        if isinstance(row[0],int):
                            
                            try:
                                house = houses.filter(mgridID=row[0]).exclude(deleted=True).get()
                            except House.DoesNotExist:
                                messages.append("[??????] ???????????????{} ??? {} ??????????????????????????????????????????????????????????????????????????????".format(mgrid.name,row[0]))
                                return render(request,'resident/upload_result.html',{'messages':messages})
                            
                            #house = row[0]#FAKE
                            #messages.append("[FAKE] ???????????????house?????? {} ???".format(house))#FAKE
                            house_count += 1

                            obj = Resident.objects.filter(name=row[2]).filter(sex=translateSex(row[4])).exclude(deleted=True).exists()
                            if obj:
                                obj = Resident.objects.filter(name=row[2]).filter(sex=translateSex(row[4])).exclude(deleted=True).first()
                                obj.b_house = house
                                obj.isholder = True
                                obj.save()
                                house.holder = obj
                                house.save()
                                messages.append('[??????] {} ??????????????????????????????????????? {} ????????????????????????'.format(row[2],house.mgridID))
                                #messages.append('[??????] {} ??????????????????????????????????????? {} ????????????????????????'.format(row[2],house))#FAKE
                                resident_count += 1
                            else:
                                if pd.isnull(row[2]) & bool(row[8] == "??????"):
                                    messages.append('[??????] ??? {} ?????????????????????????????????'.format(row[0],house))
                                    empty_house_count += 1
                                else:
                                    
                                    obj = Resident.objects.create(
                                        name=get_or_nan(row[2]),
                                        r_age=get_or_nan(row[3]),
                                        sex=translateSex(get_or_nan(row[4])),
                                        phone=get_or_nan(row[5]),
                                        isLocalResident=translateIsLocal(get_or_nan(row[6])),
                                        outLocation=get_or_nan(row[7]),
                                        note=get_or_nan(row[8]),
                                        b_house=house,
                                        isholder=True
                                    )
                                    house.holder = obj
                                    house.save()
                                    
                                    resident_count += 1
                                    '''
                                    resident = Resident(
                                        name=row[2],
                                        r_age=row[3],
                                        sex=translateSex(row[4]),
                                        phone=row[5],
                                        isLocalResident=translateIsLocal(row[6]),
                                        outLocation=row[7],
                                        note=row[8],
                                        isholder=True
                                    )#FAKE
                                    '''
                                    messages.append('[??????] ?????? {} ?????? {} ????????????????????????'.format(row[2],house.mgridID))
                                    #messages.append('[??????] ?????? {} ?????? {} ????????????????????????'.format(resident,house))#FAKE
                        else:
                            if row[0] == '??????':
                                messages.append('[??????] ????????????')
                                notify.send(sender=request.user,recipient=mgrid.village.get_managers(),verb="{} ?????????????????????????????? {}".format(request.user,mgrid.name))

                                return render(request,'resident/upload_result.html',
                                    {'messages':messages,'resident_count':resident_count,'house_count':house_count,'empty_house_count':empty_house_count})
                            messages.append('[??????] ????????? {} ???'.format(i))
                    else:
                        obj = Resident.objects.filter(name=row[2]).filter(sex=translateSex(row[4])).exclude(deleted=True).exists()
                        if obj:
                            obj = Resident.objects.filter(name=row[2]).filter(sex=translateSex(row[4])).exclude(deleted=True).first()
                            obj.b_house = house
                            obj.isholder = False
                            obj.save()
                            messages.append('[??????] {} ??????????????????????????????????????? {} ???'.format(row[2],house.mgridID))
                            resident_count += 1
                        else:
                            
                            Resident.objects.create(
                                name=get_or_nan(row[2]),
                                r_age=get_or_nan(row[3]),
                                sex=translateSex(get_or_nan(row[4])),
                                phone=get_or_nan(row[5]),
                                isLocalResident=translateIsLocal(get_or_nan(row[6])),
                                outLocation=get_or_nan(row[7]),
                                note=get_or_nan(row[8]),
                                b_house=house,
                                isholder=False
                            )
                            
                            resident_count += 1
                            '''
                            resident = Resident(
                                name=row[2],
                                r_age=row[3],
                                sex=translateSex(row[4]),
                                phone=row[5],
                                isLocalResident=translateIsLocal(row[6]),
                                outLocation=row[7],
                                note=row[8],
                                isholder=False
                            )#FAKE
                            '''
                            messages.append('[??????] ?????? {} ?????? {} ???'.format(row[2],house.mgridID))
                            #messages.append('[??????] ?????? {} ?????? {} ???'.format(resident,house)) #FAKE
                    i += 1
                notify.send(sender=request.user,recipient=mgrid.village.get_managers(),verb="{} ?????????????????????????????? {}".format(request.user,mgrid.name))
                return render(request,'resident/upload_result.html',
                                    {'messages':messages,'resident_count':resident_count,'house_count':house_count,'empty_house_count':empty_house_count})
        else:
            form = UploadFileForm()
        
        return render(request,'resident/upload_file.html',{'form':form})
    else:
        raise PermissionDenied()
