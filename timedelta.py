#CyberRex様マジ感謝

import datetime

def utc2jst(basetime):
    jsttime = basetime + datetime.timedelta(hours=9)
    return jsttime

#ここから俺のやつ

def time2jt(time):
    utc = datetime.datetime.fromtimestamp(time)
    jst = utc2jst(utc)
    return jst
