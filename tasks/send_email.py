# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class Mail:
    def __init__(self, token, sender, receivers):
        self.mail_host = "smtp.qq.com"
        self.mail_token = token
        self.sender = sender
        self.receivers = receivers

    def send(self, subject, content):

        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header(self.sender, 'utf-8')
        message['To'] = Header("None", 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtp_object = smtplib.SMTP_SSL(self.mail_host, 465)
            smtp_object.login(self.sender, self.mail_token)
            smtp_object.sendmail(self.sender, self.receivers, message.as_string())
            smtp_object.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')
