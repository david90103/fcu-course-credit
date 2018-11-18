# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

header = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json; charset=UTF-8',
}

nid = ' '
password = ' '

logininfo = {
    '__EVENTTARGET': 'ctl00$Login1$LoginButton',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    'ctl00$Login1$RadioButtonList1': 'zh-tw',
    'ctl00$Login1$UserName': nid,
    'ctl00$Login1$Password': password,
    'ctl00$Login1$vcode': '',
    'ctl00$temp': ''
}

s = requests.session()

first = s.get('https://course.fcu.edu.tw/')
login_page = BeautifulSoup(first.text, "html.parser")

for element in login_page.findAll('input', {'value': True}):
    logininfo[str(element['name'])] = str(element['value'])

get_code = s.get("https://course.fcu.edu.tw/validateCode.aspx", headers=header)

with open("code.png", 'wb') as fp:
    fp.write(get_code.content)


content = input()
logininfo['ctl00$Login1$vcode'] = content
login = s.post("https://course.fcu.edu.tw/Login.aspx", data=logininfo, allow_redirects=False)
login = s.get(login.headers['Location'])

# done login

if '18343' in login.text:
    print ('yes')
else:
    print ('no')
