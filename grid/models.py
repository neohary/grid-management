from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib import admin
from django.db.models import Q

import resident

# Create your models here.
class Village(models.Model):
    name = models.CharField(max_length=20,help_text="村名")
    houses = models.IntegerField(blank=True,default=0,help_text="总户数")
    mgrids = models.IntegerField(blank=True,default=0,help_text="总网格数")
    population = models.IntegerField(blank=True,default=0,help_text="人口")
    #maplocation 跟用户绑定后，用户打开地图的默认位置
    locationX = models.DecimalField(max_digits=20,decimal_places=6,blank=True,null=True,help_text="百度地图坐标X")
    locationY = models.DecimalField(max_digits=20,decimal_places=6,blank=True,null=True,help_text="百度地图坐标Y")
    deleted = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return "{}".format(self.name)

    def delete(self):
        self.deleted = True
        self.save()
    
    class Meta:
        verbose_name = "村庄"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_village','查看村庄信息的权限'),
            ('can_c/d_village','创建/删除村庄的权限'),
            ('can_edit_village','修改村庄信息的权限'),
            ('village_mark_village','村庄信息的村管理员标记'),
            ('mgrid_mark_village','村庄信息的网格管理员标记'),
        ]
    
    def get_managers(self):
        users = User.objects.filter(Q(groups__name="村管理员") | Q(groups__name="网格管理员")).filter(profile__village=self)
        return users
    
    def get_users(self):
        users = User.objects.filter(profile__village=self)
        return users

class MicroGrid(models.Model):
    village = models.ForeignKey(Village,on_delete=models.SET_NULL,blank=True,null=True,help_text="所属村庄")
    name = models.CharField(max_length=30,blank=True,null=True,help_text="网格名称")
    sort = models.IntegerField(blank=True,null=True,help_text="村内排序")
    color = models.CharField(max_length=8,blank=True,null=True,help_text="颜色") #color 颜色HEX数据
    houses = models.IntegerField(blank=True,default=0,help_text="网格内户数")
    population = models.IntegerField(blank=True,default=0,help_text="网格内人口")
    deleted = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return "{0} {1}".format(self.village,self.name)
    
    def delete(self):
        self.deleted = True
        self.save()
    
    class Meta:
        verbose_name = "微网格"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_mgrid','查看微网格信息的权限'),
            ('can_c/d_mgrid','创建/删除微网格的权限'),
            ('can_edit_mgrid','修改微网格信息的权限'),
            ('mgrid_mark_mgrid','微网格权限的微网格管理员标记'),
            ('village_mark_mgrid','微网格权限的村管理员标记'),
        ]

class Profile(models.Model): #扩展用户模型
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    village = models.ForeignKey(Village,on_delete=models.SET_NULL,blank=True,null=True,help_text="用户所属的村庄")
    mgrid = models.ForeignKey(MicroGrid,on_delete=models.SET_NULL,blank=True,null=True,help_text="用户所属的网格")
    phone = models.BigIntegerField(blank=True,null=True,help_text="用户的手机号，用于登录和重置密码",unique=True)
    r_name = models.CharField(max_length=20,blank=True,null=True,help_text="真实姓名")

    @property
    def getMapLocation(self):
        if self.village:
            location = []
            location.append(self.village.locationX)
            location.append(self.village.locationY)
        else:
            location = False
        return location
    
    @property
    def name(self):
        if self.r_name:
            return self.r_name
        else:
            return self.user.username
    
    class Meta:
        verbose_name = "扩展的用户信息"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_user','查看用户信息的权限'),
            ('can_c/d_user','创建/删除用户的权限'),
            ('can_edit_user','修改用户信息的权限'),
            ('mgrid_mark_user','用户权限的微网格管理员标记'),
            ('village_mark_user','用户权限的村管理员标记'),
        ]

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        group = Group.objects.get(name='未授权')
        instance.groups.add(group)
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()


class GroupProfile(models.Model): #扩展用户组模型
    group = models.OneToOneField(Group,on_delete=models.CASCADE)
    color = models.CharField(max_length=8,blank=True,null=True)
    description = models.TextField(max_length=200,blank=True,null=True)
    avaliable = models.BooleanField(default=True)

    def __str__(self):
        return '%s color=%s' % (self.group,self.color)

    class Meta:
        verbose_name = "扩展用户组信息"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_group','查看用户组的权限'),
            ('can_edit_group','修改用户组的权限'),
            ('mgrid_mark_group','用户组权限的微网格管理员标记'),
            ('village_mark_user','用户组权限的村管理员标记'),
        ]

@receiver(post_save,sender=Group)
def create_group_profile(sender,instance,created,**kwargs):
    if created:
        GroupProfile.objects.create(group=instance)

@receiver(post_save,sender=Group)
def save_group_profile(sender,instance,**kwargs):
    instance.groupprofile.save()

def example_datatypes():
    return {
        'r1':['整数','int'],
        'r2':['字符串','str'],
        'r3':["布尔",'bool'],
        'r4':["日期",'datetime'],
        'r5':["选项",'select','opt1','opt2','opt3','...']
        # JSON格式为：[列的名称，列的数据类型]
        #... 需要实现的数据类型：字符串，整数，布尔，日期
    }

class CustomStaticsTemplate(models.Model):
    title = models.CharField(max_length=30,blank=False,help_text="自定义统计标题")
    RANGE_CHOICES = (
        ('v','所属村庄'),
        ('g','所属微网格'),
        ('a','全局')
    )
    range = models.CharField(max_length=1,choices=RANGE_CHOICES,blank=False,help_text="统计范围")
    mgrid = models.ForeignKey(MicroGrid,on_delete=models.SET_NULL,blank=True,null=True,help_text="所属微网格（如果是微网格范围的统计）")
    village = models.ForeignKey(Village,on_delete=models.SET_NULL,blank=True,null=True,help_text="所属村庄（如果是村范围的统计）")
    OBJECT_CHOICES = (
        ('r','人员'),
        ('h','房屋'),
        ('g','微网格')
    )
    obj = models.CharField(max_length=1,choices=OBJECT_CHOICES,blank=False,default='r',help_text="统计对象")
    datatypes = models.JSONField(default=example_datatypes,help_text="统计数据的内容")
    create_date = models.DateField(auto_now_add=True,help_text="创建日期")
    creater = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    closed = models.BooleanField(default=False,blank=True,help_text="关闭")
    deleted = models.BooleanField(default=False,blank=True,help_text="删除")

    @admin.display(description='Range')
    def display_range(self):
        return self.get_range_display()

    @admin.display(description='Object')
    def display_object(self):
        return self.get_obj_display()
    
    def close(self):
        self.closed = True
        self.save()
    
    def delete(self):
        self.deleted = True
        self.save()
    
    def __str__(self):
        return "{}".format(self.title)
    
    class Meta:
        verbose_name = "自定义统计模板"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_stemplate','查看统计模板的权限'),
            ('can_cd_stemplate','创建/删除统计模板的权限'),
            ('village_mark_stemplate','统计模板权限的村管理员标记'),
            ('mgrid_mark_stemplate','统计模板权限的网格管理员标记'),
        ]


def example_data():
    return {
        'r1':111,
        'r2':"aaa",
        'r3':True,
        'r4':"YYYY/MM/DD HH:MM:SS"
    }

class CustomStaticsInstance(models.Model):
    template = models.ForeignKey(CustomStaticsTemplate,on_delete=models.CASCADE)
    resident = models.ForeignKey('resident.Resident',on_delete=models.CASCADE,null=True,blank=True,help_text="统计对象")
    house = models.ForeignKey('resident.House',on_delete=models.CASCADE,null=True,blank=True)
    mgrid = models.ForeignKey(MicroGrid,on_delete=models.CASCADE,null=True,blank=True)
    data = models.JSONField(default=example_data,help_text="统计数据的内容")
    update_time = models.DateTimeField(auto_now_add=True,blank=True)
    creater = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return "{}的统计实例".format(self.template)

    def delete(self):
        self.deleted = True
        self.save()
    
    class Meta:
        verbose_name = "自定义统计实例"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_sinstance','查看统计实例的权限'),
            ('can_c/d_sinstance','创建/删除统计实例的权限'),
            ('can_edit_sinstance','修改统计实例的权限'),
        ]