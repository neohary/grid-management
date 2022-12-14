# Generated by Django 4.1 on 2022-08-15 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0007_alter_resident_idnumber'),
        ('grid', '0004_alter_microgrid_houses_alter_microgrid_population'),
    ]

    operations = [
        migrations.AddField(
            model_name='customstaticsinstance',
            name='resident',
            field=models.OneToOneField(default=1, help_text='统计对象', on_delete=django.db.models.deletion.CASCADE, to='resident.resident'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='microgrid',
            name='color',
            field=models.CharField(blank=True, help_text='颜色', max_length=8, null=True),
        ),
    ]
