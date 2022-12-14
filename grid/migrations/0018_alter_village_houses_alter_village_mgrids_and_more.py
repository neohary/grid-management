# Generated by Django 4.1 on 2022-09-27 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0017_alter_village_locationx_alter_village_locationy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='houses',
            field=models.IntegerField(blank=True, default=0, help_text='总户数'),
        ),
        migrations.AlterField(
            model_name='village',
            name='mgrids',
            field=models.IntegerField(blank=True, default=0, help_text='总网格数'),
        ),
        migrations.AlterField(
            model_name='village',
            name='population',
            field=models.IntegerField(blank=True, default=0, help_text='人口'),
        ),
    ]
