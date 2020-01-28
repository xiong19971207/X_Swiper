from django.db import models


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    phonenum = models.CharField(verbose_name='手机', max_length=15, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    gender = models.CharField(verbose_name='性别', max_length=6,choices=SEX)
    birthday = models.DateField(verbose_name='生日', max_length=32, default='1990-01-01')
    location = models.CharField(verbose_name='常住地', max_length=256)
    avatar = models.CharField(verbose_name='形象', max_length=256)

    class Meta:
        db_table = 'User'
