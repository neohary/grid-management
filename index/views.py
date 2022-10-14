from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import *
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from core.models import *
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

class ResidentChangeLogViewSet(viewsets.ModelViewSet):
    queryset = ResidentChangeLog.objects.all().order_by('-changetime')
    serializer_class = ResidentChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class HouseChangeLogViewSet(viewsets.ModelViewSet):
    queryset = HouseChangeLog.objects.all().order_by('-changetime')
    serializer_class = HouseChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class VillageChangeLogViewSet(viewsets.ModelViewSet):
    queryset = VillageChangeLog.objects.all().order_by('-changetime')
    serializer_class = VillageChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class MicroGridChangeLogViewSet(viewsets.ModelViewSet):
    queryset = MicroGridChangeLog.objects.all().order_by('-changetime')
    serializer_class = MicroGridChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class CustomStaticsTemplateChangeLogViewSet(viewsets.ModelViewSet):
    queryset = CustomStaticsTemplateChangeLog.objects.all().order_by('-changetime')
    serializer_class = CustomStaticsTemplateChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class CustomStaticsInstanceChangeLogViewSet(viewsets.ModelViewSet):
    queryset = CustomStaticsInstanceChangeLog.objects.all().order_by('-changetime')
    serializer_class = CustomStaticsInstanceChangeLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

from django.contrib.auth.models import User,Group

def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="未授权").exists():
            return redirect('select-village-html')
        else:
            return render(request,'index/index.html')
    else:
        return redirect('user-login-html')

@login_required
def map(request):

    return render(request,'index/map.html')

@login_required
def residentList(request):

    return render(request,'resident/resident_list.html')

from resident.models import Resident,House

@login_required
def residentDetail(request,pk):
    obj = get_object_or_404(Resident,pk=pk)
    if obj.deleted == False:
        return render(request,'resident/resident_detail.html',{'pk':pk})
    else:
        raise Http404

@login_required
def houseList(request):

    return render(request,'resident/house_list.html')

@login_required
def houseDetail(request,pk):
    obj = get_object_or_404(House,pk=pk)
    if obj.deleted == False:
        return render(request,'resident/house_detail.html',{'pk':pk})
    else:
        raise Http404

@login_required
def mgridList(request):

    return render(request,'grid/mgrid_list.html')

from grid.models import MicroGrid,CustomStaticsTemplate

@login_required
def mgridDetail(request,pk):
    obj = get_object_or_404(MicroGrid,pk=pk)
    if obj.deleted == False:
        return render(request,'grid/mgrid_detail.html',{'pk':pk})
    else:
        raise Http404

@login_required
def cStaticCreate(request):

    return render(request,'grid/cStatic_create.html')

@login_required
def cStaticDetail(request,pk):
    obj = get_object_or_404(CustomStaticsTemplate,pk=pk)
    if obj.deleted == False:
        return render(request,'grid/cStatic_detail.html',{'pk':pk})
    else:
        raise Http404

@login_required
def cStaticList(request):
    
    return render(request,'grid/cStatic_list.html')

@login_required
def userList(request):

    return render(request,'user/user_list.html')

@login_required
def userDetail(request,pk):
    obj = get_object_or_404(User,pk=pk)

    return render(request,'user/user_detail.html',{'pk':pk})

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request,'user/user_login.html')

def userLogout(request):
    #已登录的用户才可访问
    return render(request,'user/user_logout.html')

def userRegister(request):
    #未登录的用户才可访问
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request,'user/user_register.html')

def userResetPassword(request):
    #未登录的用户才可访问
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request,'user/user_reset_password.html')

def userRegistSuccess(request):
    return render(request,'user/user_regist_success.html')

@login_required
def villageSelect(request):

    return render(request,'index/village_select.html')

@login_required
def villageSelectDetail(request,pk):
    obj = get_object_or_404(Village,pk=pk)
    if obj.deleted == False:
        return render(request,'index/village_select_confirm.html',{'pk':pk})
    else:
        raise Http404

@login_required
def villageSelectSuccess(request):

    return render(request,'index/village_select_success.html')

@login_required
def userApprovalList(request):

    return render(request,'grid/user_approval_list.html')

@login_required
def editUserGroup(request,pk):

    return render(request,'user/user_edit_group.html',{'pk':pk})

from notifications.signals import notify
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def NotifyTest(request):
    for i in range(20):
        notify.send(request.user,recipient=request.user,verb="This is a test")

    return redirect('notify-list-html')

class NoticeListView(LoginRequiredMixin,ListView):
    context_object_name = 'notices'
    template_name = 'inbox/notifications.html'
    paginate_by = 15
    
    def get_queryset(self):
        return self.request.user.notifications.all().exclude(deleted=True)
    
@login_required
def notify_mark_all_as_read(request):
    qs = request.user.notifications.unread()
    qs.mark_all_as_read()

    return redirect('notify-list-html')

@login_required
def notify_delete_all_read(request):
    if request.method == 'POST':
        qs = request.user.notifications.all().filter(unread=False)
        qs.mark_all_as_deleted()
        return redirect('notify-list-html')
    else:
        return JsonResponse({'message':'只接受POST方法'})

@login_required
def village_create_complete(request):
    return render(request,'grid/village_create_complete.html')

@login_required
def village_list(request):
    return render(request,'grid/village_list.html')

@login_required
def village_detail(request,pk):
    obj = get_object_or_404(Village,pk=pk)

    return render(request,'grid/village_detail.html',{'pk':pk})

def not_found_view(request):
    
    return render(request,'index/404.html')

from resident.models import Resident,House
import random

def resident_test(request):
    for i in range(1000):
        name = ''
        for j in range(3):
            name += random.choice('阙凡旋耿冰枫蒙娟妍冀秋翠范孤丹敖翠茵充清浅')
        age = random.randint(10,100)
        sex = random.choice('mf')
        phone = random.randint(10000000000,99999999999)
        r_bool = bool(random.getrandbits(1))
        houses = list(House.objects.all().exclude(deleted=True))
        house = random.choice(houses)
        outLocation = ''
        if not r_bool:
            for j in range(random.randint(2,6)):
                outLocation += random.choice('盯卵道孕哲省堂睁镇二往坝北颤庄秀圈堡易银观')
        else:
            outLocation = None
        note = 'TEST'
        Resident.objects.create(
            name=name,
            r_age=age,
            sex=sex,
            phone=phone,
            isLocalResident=r_bool,
            outLocation=outLocation,
            note=note,
            b_house=house
        )
    return render(request,'index/test_complete.html')