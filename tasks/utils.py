# -*- coding: utf-8 -*-
import base64
import random

import requests
import urllib3
from Crypto.Cipher import AES
from requests import Session
from requests.adapters import HTTPAdapter

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
}


def get_session(retry_time=5, verify=False, proxies=None, headers=None) -> Session:
    if not verify:
        urllib3.disable_warnings()
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retry_time))
    s.mount('https://', HTTPAdapter(max_retries=retry_time))
    s.verify = verify
    if proxies:
        s.proxies.update(proxies)
    if not headers:
        headers = DEFAULT_HEADERS
    s.headers = headers

    return s


def encrypt(pwd, salt):
    charsets = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    rnd_16 = ''.join(random.choice(charsets) for _ in range(16))
    rnd_64 = ''.join(random.choice(charsets) for _ in range(64))
    return aes_encrypt(rnd_64 + pwd, salt, rnd_16)


def aes_encrypt(s: str, key: str, iv='\0' * 16, coding='utf-8') -> str:
    key_b = key.encode(coding)
    iv_b = iv.encode(coding)
    raw_b = s.encode(coding)

    cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
    padded = pad(raw_b, AES.block_size)
    encrypted = cipher.encrypt(padded)
    encoded = base64.b64encode(encrypted)
    return encoded.decode(coding)


def pad(s: bytes, block_size: int) -> bytes:
    l = len(s)
    pad_num = block_size - (l % block_size)
    if pad_num == 0:
        pad_num = block_size
    pad_b = bytes([pad_num])
    return s + pad_b * pad_num


def need_captcha(session: requests.Session, account) -> bool:
    NEED_CAPTCHA_URL = "http://authserver.njit.edu.cn" + "/authserver/needCaptcha.html"
    params = {
        'username': account,
        'pwdEncrypt2': 'pwdEncryptSalt'
        # '_': get_timestamp_mil,
    }
    res = session.get(NEED_CAPTCHA_URL, params=params)
    return True


def get_captcha(s: requests.Session) -> bytes:
    url = "http://authserver.njit.edu.cn" + "/authserver/captcha.html"
    params = {
        'ts': random.randint(1, 999)
    }
    return s.get(url, params=params).content
