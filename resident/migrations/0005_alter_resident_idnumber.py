# Generated by Django 4.1 on 2022-08-14 13:49

from django.db import migrations, models
import resident.models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0004_alter_house_population'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='IDnumber',
            field=models.CharField(help_text='身份证', max_length=18, validators=[resident.models.IDValidator]),
        ),
    ]
