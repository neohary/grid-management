# Generated by Django 4.1 on 2022-09-24 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0015_alter_customstaticsinstance_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customstaticstemplate',
            options={'permissions': [('can_see_stemplate', '查看统计模板的权限'), ('can_c/d_stemplate', '创建/删除统计模板的权限'), ('village_mark_stemplate', '统计模板权限的村管理员标记'), ('mgrid_mark_stemplate', '统计模板权限的网格管理员标记')], 'verbose_name': '自定义统计模板', 'verbose_name_plural': '自定义统计模板'},
        ),
        migrations.AlterModelOptions(
            name='groupprofile',
            options={'permissions': [('can_see_group', '查看用户组的权限'), ('can_edit_group', '修改用户组的权限'), ('mgrid_mark_group', '用户组权限的微网格管理员标记'), ('village_mark_user', '用户组权限的村管理员标记')], 'verbose_name': '扩展用户组信息', 'verbose_name_plural': '扩展用户组信息'},
        ),
        migrations.AlterModelOptions(
            name='microgrid',
            options={'permissions': [('can_see_mgrid', '查看微网格信息的权限'), ('can_c/d_mgrid', '创建/删除微网格的权限'), ('can_edit_mgrid', '修改微网格信息的权限'), ('mgrid_mark_mgrid', '微网格权限的微网格管理员标记'), ('village_mark_mgrid', '微网格权限的村管理员标记')], 'verbose_name': '微网格', 'verbose_name_plural': '微网格'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': [('can_see_user', '查看用户信息的权限'), ('can_c/d_user', '创建/删除用户的权限'), ('can_edit_user', '修改用户信息的权限'), ('mgrid_mark_user', '用户权限的微网格管理员标记'), ('village_mark_user', '用户权限的村管理员标记')], 'verbose_name': '扩展的用户信息', 'verbose_name_plural': '扩展的用户信息'},
        ),
        migrations.AlterModelOptions(
            name='village',
            options={'permissions': [('can_see_village', '查看村庄信息的权限'), ('can_c/d_village', '创建/删除村庄的权限'), ('can_edit_village', '修改村庄信息的权限'), ('village_mark_village', '村庄信息的村管理员标记'), ('mgrid_mark_village', '村庄信息的网格管理员标记')], 'verbose_name': '村庄', 'verbose_name_plural': '村庄'},
        ),
    ]
