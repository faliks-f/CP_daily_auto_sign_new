# -*- coding: utf-8 -*-
import json
import time

import schedule

from tasks.login import get_login_session
from tasks.send_email import Mail
from tasks.sign import sign


def job():
    with open("configure.json", encoding="utf-8") as f:
        configure = json.load(f)
        students = configure["students"]
        email_configure = configure["mail"]
        need_send = email_configure["need_send"]
        mail = None
        message = ""
        if need_send == "True":
            mail = Mail(email_configure["token"], email_configure["sender"], email_configure["receivers"])
        try:
            for student in students:
                s = get_login_session(student["account"], student["password"])
                if 'iPlanetDirectoryPro' not in s.cookies:
                    message += student["name"] + " fail! Login Error! Please check account and password!\n"
                else:
                    sign_result: int = sign(s)
                    if sign_result == 1:
                        message += student["name"] + " sign success.\n"
                    elif sign_result == 2:
                        message += student["name"] + " already signed.\n"
                    else:
                        message += student["name"] + " fail! Login Success! Check Error!\n"
        except Exception as e:
            print(e)
            message = ""
            for student in students:
                message = student["name"] + "fail! Configure Error!\n"
        print(message)
        try:
            if mail is not None:
                subject = time.strftime("%Y-%m-%d %H:%M", time.localtime()) + "打卡结果"
                mail.send(subject, message)
        except Exception as e:
            print("Email not send!")
            print(e)


def sign_thread(threadName):
    # changed to only one check in per day since 2022-03-25
    schedule.every().day.at("08:22").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    sign_thread("sign")
