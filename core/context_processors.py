from .models import customParameter,NavbarTab

def get_sitetitle(request):
    try:
        title = customParameter.objects.get(name='main_title').value
    except:
        return {'title':"TITLE MISSING!"}
    else:
        return {'title':title}


def get_headInfo(request):
    try:
        headInfo = customParameter.objects.get(name='head_info').value
    except:
        return {'headInfo':None}
    else:
        return {'headInfo':headInfo}
		
def get_footInfo(request):
    try:
        footInfo = customParameter.objects.get(name='foot_info').value
    except:
        return {'footInfo':"FOOTINFO MISSING!"}
    else:
        return {'footInfo':footInfo}

def get_version(request):
    try:
        version = customParameter.objects.get(name='version').value
    except:
        return {'version':"VERSION MISSING!"}
    else:
        return {'version':version}

def is_inviteRegOnly(request):
    try:
        inviteRegOnly = customParameter.objects.get(name='inviteRegOnly').value
    except:
        return {'inviteRegOnly':False}
    else:
        if inviteRegOnly == '1':
            return {'inviteRegOnly':True}
        else:
            return {'inviteRegOnly':False}
        

def is_underMaintaining(request):
    try:
        is_underMaintaining = customParameter.objects.get(name='is_underMaintaining').value
    except:
        return {'is_underMaintaining':False}
    else:
        if is_underMaintaining == '1':
            return {'is_underMaintaining':True}
        else:
            return {'is_underMaintaining':False}

def NavbarTabs(request):
    NavbarTabs_html = NavbarTab.objects.filter(scope__in=request.user.groups.all()).filter(avaliable=True)
    return {'NavbarTabs':NavbarTabs_html}

from core.models import UserApproval
from grid.models import CustomStaticsTemplate
from django.db.models import Q

def get_live_user_approval_count(request):
    #如果用户是村管理
    if request.user.is_authenticated:
        count = UserApproval.objects.filter(village=request.user.profile.village).exclude(status='x').count()
        return {'live_user_approval_count':count}
    else:
        return {'live_user_approval_count':None}

def get_live_static_count(request):
    if request.user.is_authenticated:
        try:
            count = CustomStaticsTemplate.objects.filter(Q(village=request.user.profile.village) | Q(range='a')).exclude(closed=True).exclude(deleted=True).count()
        except:
            count = None
        print(count)
        return {'live_static_count':count}
    else:
        return {'live_static_count':None}

def get_map_key(request):
    if request.user.is_authenticated:
        try:
            key = customParameter.objects.get(name='map_api_key').value
        except:
            return {'map_key':False}
        
        return {'map_key':key} #qilFhMCjAUFhh5OV4FlbrycrZc2I40LQ
    else:
        return {'map_key':False}

def get_map_style_id(request):
    if request.user.is_authenticated:
        try:
            key = customParameter.objects.get(name='map_style_id').value
        except:
            return {'map_style_id':None}
            
        return {'map_style_id':key} #cc7c2852115b42d620cd0dd058ab438e
    else:
        return {'map_style_id':None}