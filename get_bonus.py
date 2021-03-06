# coding=utf-8
import random
import smtplib
import time
from email.mime.text import MIMEText

import requests
import json
from email.mime.multipart import MIMEMultipart

# cookie - can be found from browser with F12
userCookie = ''

msg_from = '370716264@qq.com'  # sender
passwd = ''  # qq mail box autherized code
to = ['370716264@qq.com']  # receiver

current_url = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'
checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'


def http_request(url):
    headers = {
        'Referer': 'https://www.smzdm.com/',
        'Host': 'zhiyou.smzdm.com',
        'Cookie': userCookie.encode('utf-8'),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = json.loads(res.text)
        return data
    else:
        raise Exception(res.text)


def report(content):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    msg['Subject'] = "smzdm bonue report"
    msg['From'] = msg_from

    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, to, msg.as_string())


def try_bonus():
    try:
        data = http_request(current_url)
        if not data['checkin']['has_checkin']:
            checkin = http_request(checkin_url)['data']
            print(checkin)

        data = http_request(current_url)
        info = '%s ：%s 你目前积分：%s，经验值：%s，金币：%s，碎银子：%s，威望：%s，等级：%s，已经签到：%s天' % (
                data['sys_date'], data['nickname'], data['point'], data['exp'], data['gold'], data['silver'],
                data['prestige'],
                data['level'], data['checkin']['daily_checkin_num'])
        return info
    except Exception as ex:
        print(ex)
        return "Fail to get bonus. " + str(ex)


time.sleep(random.randint(0, 60))
result = try_bonus()
print(result)
report(result)
