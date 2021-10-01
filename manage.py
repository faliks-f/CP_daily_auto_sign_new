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
        for student in students:
            s = get_login_session(student["account"], student["password"])
            if 'iPlanetDirectoryPro' not in s.cookies:
                message += student["name"] + " fail\n"
            else:
                if sign(s):
                    message += student["name"] + " success\n"
                else:
                    message += student["name"] + " fail\n"
            print(message)
        if mail is not None:
            subject = time.strftime("%Y-%m-%d %H:%M", time.localtime()) + "打卡结果"
            mail.send(subject, message)


def sign_thread(threadName):
    schedule.every().day.at("07:10").do(job)
    schedule.every().day.at("12:10").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    sign_thread("sign")
