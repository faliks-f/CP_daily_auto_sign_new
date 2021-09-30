# -*- coding: utf-8 -*-
url = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/configSet/noraml/getRouteConfig.do?v=06320772315700147"
url1 = "http://ehallapp.njit.edu.cn/publicapp/sys/emappagelog/config/lwNjitHealthInfoDailyClock.do"
url2 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/healthClock.html?av=3"
url3 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock.do"
url4 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getClockTimeByPersonType.do"
url5 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getMyDailyReportDatas.do"
url6 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwpub/api/getServerTime.do"
url7 = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do"


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
        data["FILL_TIME"] = time
        data["TODAY_TEMPERATURE"] = "001"
        data["TODAY_TEMPERATURE_DISPLAY"] = "36℃及以下"
        print(time.split(" ")[1].split(":")[0])
        if int(time.split(" ")[1].split(":")[0]) < 12:
            data["BY3"] = "001"
            data["BY3_DISPLAY"] = "晨间打卡"
        else:
            data["BY3"] = "002"
            data["BY3_DISPLAY"] = "晚间打卡"
        res = s.post(url=url7, params=data)
        if res.json()["datas"]["T_HEALTH_DAILY_INFO_SAVE"]:
            return True
    except Exception as e:
        print(e)
    return False
