# Generated by Django 4.1 on 2022-09-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0012_alter_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
