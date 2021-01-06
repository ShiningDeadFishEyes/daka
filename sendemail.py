# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def mail(context , receiver):
    if receiver == "" :
        return;
    server = 'smtp.qq.com'
    user = '1275918492'
    passwd = 'ygfmyvfzpcorgjed'

    sender = '1275918492@qq.com'
    receivers = [receiver]
    message = MIMEMultipart()
    message['From'] = Header("打卡日志", 'utf-8')
    message['To'] = Header("Shanyx-126 mail box", 'utf-8')
    subject = '打卡日志'
    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText(context, 'plain', 'utf-8'))



    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(server, 25)  # 25 为 SMTP 端口号
        smtpObj.login(user, passwd)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail send success")
    except smtplib.SMTPException:
        print('Error: failed to send email')
