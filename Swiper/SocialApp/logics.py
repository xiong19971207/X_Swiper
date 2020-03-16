import datetime

from SocialApp.models import Swiped, Friend
from UserApp.models import Profile, User
from libs.cache import rds


def rcmd_from_redis(uid):
    rds_list = rds.lrange('FIRST_Q-%s' % uid, 0, 9)
    rds_users = [user for user in User.objects.filter(id__in=rds_list)]
    return rds_users


def rcmd_from_db(uid, num):
    profile, _ = Profile.objects.get_or_create(id=uid)

    today = datetime.datetime.today()

    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 排除已经划过的人的ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)
    print(list(sid_list))

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]

    return users


def rcmd(uid):
    users_from_redis = rcmd_from_redis(uid)
    count = 10 - len(users_from_redis)
    users_from_db = rcmd_from_db(uid, count)

    return list(users_from_redis) + list(users_from_db)


def like_someone(uid, sid):

    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='like')

    # 滑动过的人从优先推荐队列删除
    rds.lrem('FIRST_Q-%s' % uid, 1, sid)

    # 查看对方有没有喜欢或超级喜欢我
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='superlike')

    # 滑动过的人从优先推荐队列删除
    rds.lrem('FIRST_Q-%s' % uid, 1, sid)

    # 查看对方有没有喜欢或超级喜欢我
    like_me = Swiped.is_liked(sid, uid)
    if like_me:
        Friend.make_friends(uid, sid)
        return True
    elif like_me == False:
        return False
    else:
        rds.rpush('FIRST_Q-%s' % sid, uid)
        return False
