# Generated by Django 4.1 on 2022-09-22 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0013_groupprofile_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='avaliable',
            field=models.BooleanField(default=True),
        ),
    ]
