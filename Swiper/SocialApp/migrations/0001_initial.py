# Generated by Django 3.0.3 on 2020-03-11 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='好友ID')),
                ('uid2', models.IntegerField(verbose_name='好友ID')),
            ],
        ),
        migrations.CreateModel(
            name='Swiped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='滑动者的ID')),
                ('sid', models.IntegerField(verbose_name='被滑动者的ID')),
                ('stype', models.CharField(choices=[('like', '喜欢'), ('superlike', '非常喜欢'), ('dislike', '不喜欢')], max_length=10, verbose_name='被滑动的类型')),
                ('stime', models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')),
            ],
        ),
    ]
