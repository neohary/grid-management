from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from grid.models import MicroGrid,Village,CustomStaticsInstance
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,post_delete
from rest_framework.response import Response
from rest_framework import status

# Create your models here.
def IDValidator(value):
    #身份证号码验证
     Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
     Ti = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
     sum = 0
    #身份证第十八位可能是X，输入时将小写x转换为大写X
     value = value.upper()
     if len(value) != 18:
        return Response({'error':'请输入18位身份证号码,您只输入了%s位' % len(value)},status=status.HTTP_400_BAD_REQUEST) 
     for i in range(17):
        sum += int(value[i]) * Wi[i]
     if Ti[sum%11] != value[17]:
        return Response({'error':"请输入正确的身份证号码"},status=status.HTTP_400_BAD_REQUEST)

class Resident(models.Model):
    name = models.CharField(max_length=20,blank=False,null=False,help_text="姓名")
    IDnumber = models.CharField(max_length=18,validators=[IDValidator],blank=True,null=True,help_text="身份证")
    r_age = models.IntegerField(blank=True,null=True)
    SEX_CHOICES = (
        ('m','男'),
        ('f','女'),
        ('o','其他')
    )
    sex = models.CharField(max_length=1,choices=SEX_CHOICES,blank=True,help_text="性别")
    phone = models.BigIntegerField(blank=True,null=True,help_text="电话")
    isLocalResident = models.BooleanField(default=False,help_text="是否常住")
    outLocation = models.CharField(max_length=30,blank=True,null=True,help_text="在外地点")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    b_house = models.ForeignKey('House',on_delete=models.SET_NULL,null=True,blank=True,help_text="户")
    isholder = models.BooleanField(default=False,help_text="户主")
    deleted = models.BooleanField(default=False,help_text="删除")

    class Meta:
        verbose_name = "人员信息"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_resident','查看人员信息的权限'),
            ('can_c/d_resident','创建/删除人员信息的权限'),
            ('can_edit_resident','修改人员信息的权限'),
            ('village_mark_resident','人员信息的村管理员标记'),
            ('mgrid_mark_resident','人员信息的微网格管理员标记'),
        ]

    @property
    def age(self):
        if self.IDnumber:
            try:
                age = int(datetime.now().year) - int(self.IDnumber[6:10])
            except:
                age = ''
        else:
            age = self.r_age
            
        return age
    
    @property
    def village(self):
        return self.b_house.village
    
    @property
    def mgrid(self):
        return self.b_house.mgrid

    def __str__(self):
        return "{0}".format(self.name)
    
    def delete(self):
        #self.IDnumber = 0
        statics = CustomStaticsInstance.objects.filter(resident=self).exclude(deleted=True)
        if statics:
            for s in statics:
                s.delete()
        self.deleted = True
        self.save()

'''@receiver(pre_save,sender=Resident)
def minus_house_population(sender,instance,**kwargs):
    try:
        house = instance.house
    except:
        house = None
        
    if house:
        house.population -= 1
        house.save()

@receiver(post_save,sender=Resident)
def add_house_population(sender,instance,**kwargs):
    try:
        house = instance.house
    except:
        house = None

    if house:
        house.population += 1
        house.save()'''
def default_geo_data():
    return {
        'p1':[0,0],'p2':[1,1]
    }

class House(models.Model):
    mgrid = models.ForeignKey(MicroGrid,on_delete=models.CASCADE,blank=False,null=False,help_text="所属网格")
    holder = models.OneToOneField(Resident,on_delete=models.SET_NULL,blank=True,null=True,help_text="户主")
    population = models.IntegerField(default=0,blank=True,null=True,help_text="人数")
    mgridID = models.IntegerField(blank=True,null=True,help_text="网格序号")
    village = models.ForeignKey(Village,on_delete=models.CASCADE,blank=False,null=False,help_text="所属村")
    #maplocation
    #geo = models.PolygonField()
    geo = models.JSONField(default=default_geo_data,help_text="房屋的地图数据")
    deleted = models.BooleanField(default=False,blank=True,help_text="删除")

    class Meta:
        verbose_name = "住户信息"
        verbose_name_plural = verbose_name
        permissions = [
            ('can_see_house','查看住户信息的权限'),
            ('can_c/d_house','创建/删除住户信息的权限'),
            ('can_edit_house','修改住户信息的权限'),
            ('village_mark_house','住户信息的村管理员标记'),
            ('mgrid_mark_house','住户信息的微网格管理员标记'),
        ]

    def __str__(self):
        return "{0} 第{1}户".format(self.mgrid,self.mgridID)
    
    @property
    def pop(self):
        count = Resident.objects.filter(b_house=self).exclude(deleted=True).count()
        return count
    
    def delete(self):
        statics = CustomStaticsInstance.objects.filter(house=self).exclude(deleted=True)
        if statics:
            for s in statics:
                s.delete()
        self.deleted = True
        self.save()