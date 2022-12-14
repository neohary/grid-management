# Generated by Django 4.1 on 2022-09-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0011_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(blank=True, help_text='用户的手机号，用于登录和重置密码', null=True, unique=True),
        ),
    ]
