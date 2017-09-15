# encoding: utf-8
from __future__ import absolute_import

__author__ = 'yudan.chen'


from datetime import datetime, timedelta
import pytz
from dateutil import parser

LOCAL_TZ = pytz.timezone('Asia/Shanghai')
LOCAL_ZERO_DATETIME = datetime(1970, 1, 1, 8)
DEFAULT_DATIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime2epoch(dt):
    """
    :type dt: datetime
    """
    if dt.tzinfo is None:
        return (dt - LOCAL_ZERO_DATETIME).total_seconds()
    return (dt - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()


def epoch2datetime(epoch, tz=LOCAL_TZ):
    """
    :type epoch: float
    :type tz: tzinfo
    """
    return datetime.fromtimestamp(epoch)


def get_datetime_now_str():
    return datetime.now().strftime(DEFAULT_DATIME_FORMAT)


def get_list_timestamp_to_weekday(l_time):
    n = abs((int(l_time[-1]) - int(l_time[0]))) / 86400

    _begin = datetime.fromtimestamp(float(l_time[0])).weekday()
    _end = datetime.fromtimestamp(float(l_time[-1])).weekday()
    a = set([_begin, _end])
    for i in range(_begin, n + _begin):
        if i >= 7:
            i -= 7
        a.add(i)
    return list(a)


def get_timerange(l_time):
    res = []
    for l in l_time:
        next_day = int(l) + 86400
        if next_day > l_time[-1]:
            break
        res.append(next_day)

    return res + l_time


def parse_time(time_str):
    if not time_str:
        return None
    try:
        return parser.parse(time_str)
    except:
        return None


def get_date_format(time_str):
    return time_str.strftime('%Y-%m-%d')


# 取一周中的第一天
def get_day_in_week_monday():
    week_num = datetime.now().weekday()
    monday = datetime.now() + timedelta(days=-week_num)
    monday = str(monday)[0:10] + ' 00:00:00'
    return monday


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + timedelta(i), format) for i in range(0, days, step)]