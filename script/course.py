# -*- coding: UTF-8 -*-

import requests
import getpass
from bs4 import BeautifulSoup

header = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json; charset=UTF-8',
}

nid = input('Student ID: ')
password = getpass.getpass('NID password: ')

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


content = input("Validation code (check your folder for code.png):")
logininfo['ctl00$Login1$vcode'] = content
login = s.post("https://course.fcu.edu.tw/Login.aspx", data=logininfo, allow_redirects=False)
# param baseURL: http://serviceXXX.sds.fcu.edu.tw/
baseURL = login.headers['Location'][0: login.headers['Location'].index('?')]
login = s.get(login.headers['Location'])
login_page = BeautifulSoup(login.text, "html.parser")

# done login

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

logininfo = {
    '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabSelected$gvWishList$ctl02$btnAdd',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '',
    '__VIEWSTATEGENERATOR': '',
    '__EVENTVALIDATION': ''
}

for element in login_page.findAll('input', {'value': True}):
    if (not 'tabSelected' in str(element['name'])) and (not 'btn' in str(element['name'])):
        logininfo[str(element['name'])] = str(element['value'])
        print(str(element['name']))

guid = login_page.find('form', id='aspnetForm').get('action')

login = s.post(baseURL + guid, data=logininfo, headers=header, allow_redirects=False)

# check if "File saved" in html
if len(login.text) < 10000:
    print("------\n\nFail\n")
elif 'File saved' in login.text:
    print ('------\n\nYes\n')
else:
    print ('------\n\nNo\n')
