from django.db import models
from django.contrib.auth.models import User,Group
from grid.models import Village,MicroGrid
from django.utils import timezone

# Create your models here.
class customParameter(models.Model):
    name = models.CharField(max_length=255,unique=True,null=False,blank=False,help_text="自定义参数名称")
    value = models.TextField(max_length=1000,null=True,blank=True,help_text="参数值")

    class Meta:
        verbose_name = "自定义参数"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.name)

class NavbarTab(models.Model):
    name = models.CharField(max_length=255,help_text='显示的名字')
    order = models.IntegerField(null=True,blank=True)
    url = models.CharField(max_length=255,help_text='url.py里的name值')
    variable = models.CharField(max_length=255,null=True,blank=True,help_text='url参数')
    icon = models.CharField(max_length=255,help_text='图标路径')
    scope = models.ForeignKey(Group,on_delete=models.CASCADE,help_text='对什么权限的用户可见')
    avaliable = models.BooleanField(default=True,null=False,blank=False,help_text='是否启用')
    splitline = models.BooleanField(default=False,null=False,blank=False,help_text='是否在标签下显示分割线')
    context_processors = models.CharField(max_length=255,blank=True,null=True,help_text='计数器')

    class Meta:
        ordering = ['order']
        verbose_name = "侧边栏标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.name,self.url)
        
class UserApproval(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="s_user")
    village = models.ForeignKey(Village,on_delete=models.CASCADE,blank=False,null=False)
    mgrid = models.ForeignKey(MicroGrid,on_delete=models.CASCADE,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('o','待处理'),
        ('x','已结束')
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='o',blank=True)
    RESULT_CHOICES = (
        ('a','通过'),
        ('d','拒绝')
    )
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,blank=True,null=True)
    note = models.TextField(max_length=200,blank=True,null=True)
    approval_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="approval_by_user")
    close_time = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name = "用户申请"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_deal_approvals','处理用户申请的权限'),
            ('can_see_approvals','查看用户申请的权限'),
            ('can_c/d_approvals','创建/删除用户申请的权限'),
        ]

    def __str__(self):
        return '[{}]{}的申请'.format(self.get_status_display,self.user.username)
    
    def close(self):
        if self.status == 'o':
            self.close_time = timezone.now()
            self.status = 'x'
            self.save()
            return True
        else:
            return False