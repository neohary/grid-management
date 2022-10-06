# Generated by Django 4.1 on 2022-09-27 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0016_alter_customstaticstemplate_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='locationX',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='百度地图坐标X', max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='village',
            name='locationY',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='百度地图坐标Y', max_digits=20, null=True),
        ),
    ]
