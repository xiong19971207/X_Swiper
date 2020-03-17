from django.db import models, IntegrityError

from common import stat


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
        like_types = ['like', 'superlike']
        try:
            swiped_record = cls.objects.get(uid=uid, sid=sid)
            return swiped_record.stype in like_types
        except cls.DoesNotExist:
            return None

    @classmethod
    def swipe(cls, uid, sid, stype):
        if cls.stype not in ['like', 'superlike', 'dislike']:
            raise stat.StypeErr
        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise stat.ReswipeErr

    class Meta:
        db_table = 'swiped'
        unique_together = [['uid', 'sid']]


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
