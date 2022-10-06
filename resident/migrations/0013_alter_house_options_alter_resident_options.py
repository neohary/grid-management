# Generated by Django 4.1 on 2022-09-24 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0012_alter_house_options_alter_resident_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='house',
            options={'permissions': [('can_see_house', '查看住户信息的权限'), ('can_c/d_house', '创建/删除住户信息的权限'), ('can_edit_house', '修改住户信息的权限')], 'verbose_name': '住户信息', 'verbose_name_plural': '住户信息'},
        ),
        migrations.AlterModelOptions(
            name='resident',
            options={'permissions': [('can_see_resident', '查看人员信息的权限'), ('can_c/d_resident', '创建/删除人员信息的权限'), ('can_edit_resident', '修改人员信息的权限')], 'verbose_name': '人员信息', 'verbose_name_plural': '人员信息'},
        ),
    ]