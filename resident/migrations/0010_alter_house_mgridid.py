# Generated by Django 4.1 on 2022-08-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0009_house_geo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='mgridID',
            field=models.IntegerField(blank=True, help_text='网格序号', null=True),
        ),
    ]
