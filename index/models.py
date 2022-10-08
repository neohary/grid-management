from resident.models import *
from grid.models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.signals import user_logged_in

# Create your models here.

CHANGE_TYPES = (
    ('c','创建'),
    ('u','编辑'),
    ('d','删除')
)

class ResidentChangeLog(models.Model):
    object = models.ForeignKey(Resident,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "人员变更日志"
        verbose_name_plural = verbose_name

class HouseChangeLog(models.Model):
    object = models.ForeignKey(House,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "住户变更日志"
        verbose_name_plural = verbose_name

class VillageChangeLog(models.Model):
    object = models.ForeignKey(Village,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "村庄变更日志"
        verbose_name_plural = verbose_name

class MicroGridChangeLog(models.Model):
    object = models.ForeignKey(MicroGrid,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "微网格变更日志"
        verbose_name_plural = verbose_name

class CustomStaticsTemplateChangeLog(models.Model):
    object = models.ForeignKey(CustomStaticsTemplate,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "自定义统计模板变更日志"
        verbose_name_plural = verbose_name

class CustomStaticsInstanceChangeLog(models.Model):
    object = models.ForeignKey(CustomStaticsInstance,on_delete=models.DO_NOTHING,null=True)
    context = models.CharField(max_length=500)
    behaviour = models.CharField(max_length=1,choices=CHANGE_TYPES)
    changeby = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    changetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
    
    class Meta:
        verbose_name = "自定义统计实例变更日志"
        verbose_name_plural = verbose_name

class UserLoginLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    login_time = models.DateTimeField(auto_now_add=True,verbose_name="登录时间")
    ip_address = models.CharField(max_length=20,verbose_name="IP地址")
    device_name = models.CharField(max_length=300,verbose_name="设备名称")

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "用户登录日志"
        verbose_name_plural = verbose_name


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_user_login(sender,user,request,**kwargs):
    #print(request.META['HTTP_USER_AGENT'])
    UserLoginLog.objects.create(user=user,
        ip_address=get_client_ip(request),
        device_name=request.META['HTTP_USER_AGENT'])

user_logged_in.connect(log_user_login)