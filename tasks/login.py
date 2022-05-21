# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs4
from requests.compat import urljoin

from predict.predict import predict_captcha
from predict.utils import *
from tasks.utils import *

url = "http://authserver.njit.edu.cn/authserver/login?service=http%3A%2F%2Fehall.njit.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.njit.edu.cn%2Fnew%2Findex.html"


def retry(s: requests.Session, account: str, password: str) -> bool:
    require_captcha: bool = need_captcha(s, account)
    captcha = ""
    while not check_captcha(captcha):
        content = get_captcha(s)
        # check whether b'<html>' in content
        if b'<html>' in content:
            print("ERROR: get_captcha() failed")
            print("Response:", content)
            raise Exception("get_captcha() failed, content:", content)
        captcha = predict_captcha(content)
    res = s.get(url)
    data = {
        "lt": None,
        "dllt": None,
        "execution": None,
        "_eventId": None,
        "rmShown": None,
        'pwdDefaultEncryptSalt': None
    }
    res = bs4(res.content, 'html.parser')
    salt = res.find('input', id='pwdDefaultEncryptSalt')['value']
    login_url = res.find('form', id='casLoginForm')['action']
    login_url = urljoin(url, login_url)

    for i in res.find_all('input'):
        if 'name' in i.attrs and i['name'] in data:
            data[i['name']] = i['value']

    data['username'] = account
    data['password'] = encrypt(password, salt)

    data['rememberMe'] = 'on'
    if require_captcha:
        data['captchaResponse'] = captcha

    s.post(login_url, data=data)
    return len(s.cookies) != 2


def get_login_session(account: str, password: str, retry_times: int = 5) -> requests.Session:
    s: requests.Session = get_session()
    while retry_times and not retry(s, account, password):
        retry_times -= 1
    return s
