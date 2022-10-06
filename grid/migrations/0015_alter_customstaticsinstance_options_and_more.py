# Generated by Django 4.1 on 2022-09-24 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0014_groupprofile_avaliable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customstaticsinstance',
            options={'permissions': [('can_see_sinstance', '查看统计实例的权限'), ('can_c/d_sinstance', '创建/删除统计实例的权限'), ('can_edit_sinstance', '修改统计实例的权限')], 'verbose_name': '自定义统计实例', 'verbose_name_plural': '自定义统计实例'},
        ),
        migrations.AlterModelOptions(
            name='customstaticstemplate',
            options={'permissions': [('can_see_stemplate', '查看统计模板的权限'), ('can_c/d_stemplate', '创建/删除统计模板的权限')], 'verbose_name': '自定义统计模板', 'verbose_name_plural': '自定义统计模板'},
        ),
        migrations.AlterModelOptions(
            name='microgrid',
            options={'permissions': [('can_see_mgrid', '查看微网格信息的权限'), ('can_c/d_mgrid', '创建/删除微网格的权限'), ('can_edit_mgrid', '修改微网格信息的权限')], 'verbose_name': '微网格', 'verbose_name_plural': '微网格'},
        ),
        migrations.AlterModelOptions(
            name='village',
            options={'permissions': [('can_see_village', '查看村庄信息的权限'), ('can_c/d_village', '创建/删除村庄的权限'), ('can_edit_village', '修改村庄信息的权限')], 'verbose_name': '村庄', 'verbose_name_plural': '村庄'},
        ),
    ]