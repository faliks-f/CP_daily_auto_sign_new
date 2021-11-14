# -*- coding: utf-8 -*-

import random
import json

url = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/configSet/noraml/getRouteConfig.do?v=06320772315700147"
url1 = "http://ehallapp.njit.edu.cn/publicapp/sys/emappagelog/config/lwNjitHealthInfoDailyClock.do"
url2 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/healthClock.html?av=3"
url3 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock.do"
url4 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getClockTimeByPersonType.do"
url5 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getMyDailyReportDatas.do"
# url5 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getMyDailyReportDatas.do"
url6 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwpub/api/getServerTime.do"
url7 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do"


def get_wid(s, batch_code):
    wid_url = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getMyTodayReportWid.do"
    params = {"pageNumber": 1, "BATCH_CODE": batch_code}
    res = s.post(wid_url, params=params)
    wid = str(res.json()["datas"]["getMyTodayReportWid"]["rows"][0]["WID"])
    return wid


def is_checked(last_time, now_time):
    last_date = last_time.split(" ")[0].split("-")
    now_date = now_time.split(" ")[0].split("-")
    if len(last_date) != 3 and len(now_date) != 3:
        return False
    if last_date[0] != now_date[0] or last_date[1] != now_date[1] or last_date[2] != now_date[2]:
        return False
    last_hour = int(last_time.split(" ")[1].split(":")[0])
    now_hour = int(now_time.split(" ")[1].split(":")[0])
    if last_hour < 12 and now_hour < 12:
        return True
    if last_hour >= 12 and now_hour >= 12:
        return True
    return False


def sign(s):
    try:
        res = s.get(url=url)
        res = s.get(url=url1)
        res = s.get(url=url2)
        params = {"*json": 1}
        res = s.post(url=url3, params=params)
        res = s.post(url=url4)
        params = {"pageNumber": 1,
                  "pageSize": 1}
        res = s.post(url=url5, params=params)
        data = res.json()["datas"]["getMyDailyReportDatas"]["rows"][0]
        res = s.post(url=url6)
        time = res.json()["date"].replace("/", "-")
        if is_checked(data["FILL_TIME"], time):
            return True
        check_time = data["FILL_TIME"]
        data["CZR"] = None
        data["CZZXM"] = None
        data["CHECKED"] = "YES"
        data["FILL_TIME"] = time
        data["NEED_CHECKIN_DATA"] = time.split(" ")[0]
        data["CREATED_AT"] = time
        yestday = time.split(" ")[0].split("-")[-1]
        czrq = time.split(" ")[0].split("-")[0] + "-" + time.split(" ")[0].split("-")[1] + "-" + str(int(yestday) - 1) \
               + " 23:55:57"
        data["CZRQ"] = czrq
        data["TODAY_TEMPERATURE"] = "001"
        data["TODAY_TEMPERATURE_DISPLAY"] = "36℃及以下"
        if int(time.split(" ")[1].split(":")[0]) < 12:
            data["BY3"] = "001"
            data["BY3_DISPLAY"] = "晨间打卡"
        else:
            data["BY3"] = "002"
            data["BY3_DISPLAY"] = "晚间打卡"
        data["WID"] = get_wid(s, data["BY3"])
        res = s.post(url=url7, params=data)
        if res.json()["datas"]["T_HEALTH_DAILY_INFO_SAVE"]:
            return True
    except Exception as e:
        print(e)
    return False
