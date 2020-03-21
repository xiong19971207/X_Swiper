import datetime

from SocialApp.models import Swiped, Friend
from UserApp.models import Profile, User
from common import stat
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
    Swiped.swipe(uid, sid, 'like')

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
    Swiped.swipe(uid, sid, 'superlike')

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


def dislike_someone(uid, sid):
    # 添加滑动记录
    Swiped.swipe(uid, sid, 'dislike')

    # 滑动过的人从优先推荐队列删除
    rds.lrem('FIRST_Q-%s' % uid, 1, sid)


def rewind_swipe(uid):
    # 取出当前时间
    now = datetime.datetime.now()
    print(now)
    Rewind_K = 'Rewind_times-%s-%s' % (now.date(), uid)

    # 当天反悔次数，取不到时默认为 0
    rewind_times = rds.get(Rewind_K, 0)

    # 检查当前反悔次数是否大于3次以上
    if rewind_times > 3:
        raise stat.RewindtimesErr

    # 取出最后一次的滑动记录
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')
    print(last_swipe)

    # 检查是否过了五分钟过期时间
    pass_time = now - last_swipe.stime
    print(pass_time.total_seconds())
    if pass_time.total_seconds() > 5 * 60:
        raise stat.RewindtimeoutErr

    # 如果是超级喜欢,需要将自己从对方优先推荐队列删除,然后解除好友关系
    if last_swipe.stype == 'superlike':
        rds.lrem('FIRST_Q-%s' % last_swipe.sid, 1, uid)
        Friend.break_friends(uid, last_swipe.sid)
    # 如果反悔之前是喜欢,需要撤销好友关系
    elif last_swipe.stype == 'like':
        Friend.break_friends(uid, last_swipe.sid)

    # 将滑动记录删除
    last_swipe.delete()

    # 更新反悔次数
    rds.set(Rewind_K, rewind_times + 1, 86400)

