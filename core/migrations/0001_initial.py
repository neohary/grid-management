# Generated by Django 4.1 on 2022-08-28 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='customParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='自定义参数名称', max_length=255, unique=True)),
                ('value', models.TextField(blank=True, help_text='参数值', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NavbarTab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='显示的名字', max_length=255)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('url', models.CharField(help_text='url.py里的name值', max_length=255)),
                ('variable', models.CharField(blank=True, help_text='url参数', max_length=255, null=True)),
                ('icon', models.CharField(help_text='图标路径', max_length=255)),
                ('avaliable', models.BooleanField(default=True, help_text='是否启用')),
                ('splitline', models.BooleanField(default=False, help_text='是否在标签下显示分割线')),
                ('context_processors', models.CharField(blank=True, help_text='计数器', max_length=255, null=True)),
                ('scope', models.ForeignKey(help_text='对什么权限的用户可见', on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
