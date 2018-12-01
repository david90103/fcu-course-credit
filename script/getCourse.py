# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import sqlite3

baseUrl = 'https://coursesearch01.fcu.edu.tw/Service/Search.asmx/'
header = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json; charset=UTF-8',
}

conn = sqlite3.connect('course.db')
cur = conn.cursor()
options = [{"lang": "cht", "year": 107, "sms": 1}, {"lang": "cht", "year": 106, "sms": 2}]

for option in options:
    deptList = requests.post(baseUrl + 'GetDeptList', json={
                             "baseOptions": option, "degree": "1"}, headers=header)
    for dept in json.loads(deptList.json()['d']):
        print ('\n[POST] ' + dept['name'], end='')
        unitList = requests.post(
            baseUrl + 'GetUnitList', json={"baseOptions": option, "degree": "1", "deptId": dept['id']}, headers=header)
        for unit in json.loads(unitList.json()['d']):
            print ('.', end='')
            classList = requests.post(baseUrl + 'GetType1Result', json={"baseOptions": option, "typeOptions": {
                                      "degree": "1", "deptId": dept['id'], "unitId": unit['id'], "classId": "*"}}, headers=header)
            for c in json.loads(classList.json()['d'])['items']:
                y = int(re.search(r'[^\d]+(\d+)P?', c['sub_id3']).group(1)[0])
                cur.execute('insert into course values (?, ?, ?, ?, ?, ?, ?, ?)',
                            (int(c['scr_selcode']), c['sub_id3'], c['sub_name'], int(c['scr_credit']), c['scj_scr_mso'], dept['name'], unit['name'], y))

conn.commit()
conn.close()
