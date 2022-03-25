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


def get_sign_wid_info(s, batch_code) -> (str, str, str):
    wid_url = "http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/getMyTodayReportWid.do"
    params = {"pageNumber": 1, "BATCH_CODE": batch_code}
    res = s.post(wid_url, params=params)
    wid = str(res.json()["datas"]["getMyTodayReportWid"]["rows"][0]["WID"])
    czrq = str(res.json()["datas"]["getMyTodayReportWid"]["rows"][0]["CZRQ"])
    need_chk_date = str(res.json()["datas"]["getMyTodayReportWid"]["rows"][0]["NEED_CHECKIN_DATE"])
    return wid, czrq, need_chk_date


def is_checked(last_time, now_time):
    last_date = last_time.split(" ")[0].split("-")
    now_date = now_time.split(" ")[0].split("-")
    if len(last_date) != 3 and len(now_date) != 3:
        return False
    if last_date[0] != now_date[0] or last_date[1] != now_date[1] or last_date[2] != now_date[2]:
        return False
    # changed to only one check in per day since 2022-03-25
    return True


# return int
# 1: success, 2: already checked, 3: error
def sign(s) -> int:
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
            return 2
        check_time = data["FILL_TIME"]
        data["CZR"] = None
        data["CZZXM"] = None
        data["CHECKED"] = "YES"
        data["FILL_TIME"] = time
        data["CREATED_AT"] = time
        # TAG BEGIN fields changed since 2022-03-23
        data["TODAY_TEMPERATURE"] = "007"
        data["TODAY_TEMPERATURE_DISPLAY"] = "是"
        # 新学期开学以来是否返校
        # BY4_DISPLAY	"是"
        # BY4	"1"
        data["BY4_DISPLAY"] = "是"
        data["BY4"] = "1"
        # 是否处于南京市外中高风险地区
        # BY5_DISPLAY	"否"
        # BY5	"0"
        data["BY5_DISPLAY"] = "否"
        data["BY5"] = "0"
        # 近14天是否有南京市外中高风险地区旅居史
        # BY6_DISPLAY	"否"
        # BY6	"0"
        data["BY6_DISPLAY"] = "否"
        data["BY6"] = "0"
        # 近14天是否与确诊病例、疑似病例或者无症状感染者有接触
        # BY7_DISPLAY	"否"
        # BY7	"0"
        data["BY7_DISPLAY"] = "否"
        data["BY7"] = "0"
        # 共同居住人员身体状况
        # BY8_DISPLAY	"无以上状况"
        # BY8	"011"
        data["BY8_DISPLAY"] = "无以上状况"
        data["BY8"] = "011"
        # 共同居住人员近14天是否有南京市外中高风险地区旅居史
        # BY9_DISPLAY	"否"
        # BY9	"0"
        data["BY9_DISPLAY"] = "否"
        data["BY9"] = "0"
        # 今日是否核酸检测
        # BY10_DISPLAY	"否"
        # BY10	"0"
        data["BY10_DISPLAY"] = "否"
        data["BY10"] = "0"
        # 本人及共同居住人员是否有近14天进口冷链食品(货物)接触史
        # BY11_DISPLAY	"否"
        # BY11	"0"
        data["BY11_DISPLAY"] = "否"
        data["BY11"] = "0"
        # 本人及其共同居住人员是否有近3个月境外旅居史
        # BY12_DISPLAY	"否"
        # BY12	"0"
        data["BY12_DISPLAY"] = "否"
        data["BY12"] = "0"
        # 本人及其共同居住人员是否有近14天省外旅居史
        # BY13_DISPLAY	"否"
        # BY13	"0"
        data["BY13_DISPLAY"] = "否"
        data["BY13"] = "0"
        # TAG END fields changed since 2022-03-23
        # only one check in per day since 2022-03-25
        data["BY3"] = "001"
        data["BY3_DISPLAY"] = "打卡"
        wid, czrq, need_chk_date = get_sign_wid_info(s, data["BY3"])
        data["WID"] = wid
        data["CZRQ"] = czrq
        data["NEED_CHECKIN_DATE"] = need_chk_date
        res = s.post(url=url7, params=data)
        if res.json()["datas"]["T_HEALTH_DAILY_INFO_SAVE"]:
            return 1
    except Exception as e:
        print(e)
    return 3
