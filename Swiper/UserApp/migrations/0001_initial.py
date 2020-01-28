# Generated by Django 2.2.6 on 2020-01-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=15, unique=True, verbose_name='手机')),
                ('nickname', models.CharField(max_length=64, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=6, verbose_name='性别')),
                ('birthday', models.DateField(default='1990-01-01', max_length=32, verbose_name='生日')),
                ('location', models.CharField(max_length=256, verbose_name='常住地')),
                ('avatar', models.CharField(max_length=256, verbose_name='形象')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
