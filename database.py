import sqlite3
import re


def clean(str):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', ", "",  str)


def getDeptList():
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    r = c.execute("select distinct unit, dept from course").fetchall()
    conn.close()
    result = {}
    for c in r:
        if not c[1] in result:
            result[c[1]] = []
        result[c[1]].append(c[0])
    return (result)


def getClassList(unitName):
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    result = c.execute("select distinct sub_name, sub_credit, scj_scr_mso, unit, year from course \
                where unit == '" + clean(unitName) + "' or unit == '英文綜合班' or unit == '核心必修綜合班'").fetchall()
    conn.close()
    return (result)


def findGeneral(className):
    print(className)
    if clean(className) == '':
        return ()
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    result = c.execute("select distinct sub_name from course where sub_name \
                like '%" + clean(className) + "%' and (unit == '通識核心' or unit == '外語文選修')").fetchall()
    conn.close()
    return result
