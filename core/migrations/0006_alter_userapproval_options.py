# Generated by Django 4.1 on 2022-09-24 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_userapproval_approval_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userapproval',
            options={'permissions': [('can_deal_approvals', '处理用户申请的权限')], 'verbose_name': '用户申请', 'verbose_name_plural': '用户申请'},
        ),
    ]
