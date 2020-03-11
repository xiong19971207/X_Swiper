from django.db import models


class Swiped(models.Model):
    STYPE = (
        ('like', '喜欢'),
        ('superlike', '非常喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的ID')
    sid = models.IntegerField(verbose_name='被滑动者的ID')
    stype = models.CharField(verbose_name='被滑动的类型', choices=STYPE, max_length=10)
    stime = models.DateTimeField(verbose_name='滑动时间', auto_now_add=True)

    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, stype__in=('like', 'superlike')).exists()

    class Meta:
        db_table = 'swiped'


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''类方法'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.create(uid1=uid1, uid2=uid2)

    class Meta:
        db_table = 'friend'
        unique_together = [['uid1', 'uid2']]
