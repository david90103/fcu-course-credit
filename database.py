import sqlite3
import re


def clean(str):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', ", "",  str)


def getDeptList():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    r = c.execute(
        "select distinct long, dept from course join modifyName on course.unit == modifyName.short").fetchall()
    conn.close()
    result = {}
    for c in r:
        if not c[1] in result:
            result[c[1]] = []
        result[c[1]].append(c[0])
    return (result)


def getClassList(unitName):
    unitName = clean(unitName)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    unitName = c.execute("select short from modifyName where long = ?",
                         (unitName,)).fetchall()[0][0]
    result = c.execute("select distinct sub_name, sub_credit, scj_scr_mso, unit, year from course \
                where unit == ? or unit == '英文綜合班' or unit == '核心必修綜合班'", (unitName,)).fetchall()
    conn.close()
    return (result)


def getUnitCredits(unitName):
    unitName = clean(unitName)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    result = c.execute("select Department_Compulsory, Department_Electuve, Other_Department_Electuve, \
                    General_Compulsory, General_Elective from department where department.Department == ?",
                       (unitName,)).fetchall()[0]
    conn.close()
    return (result)


def nidGetCridits(courses):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    result = {"通識基礎": [], "院系必修": [], "本系專業選修": [], "非本系專業選修": [], "通識選修": []}
    for key, value in courses.items():
        for course in value:
            result[key].append(c.execute("select distinct sub_name, sub_credit from course where sub_name == ?",
                                         (course,)).fetchall()[0])
    return result


def findGeneral(className):
    className = clean(className)
    if className == '':
        return ()
    # generate target for like statement in sql
    formatName = '%'
    for c in list(className):
        formatName += c + '%'
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    result = c.execute("select distinct sub_name from course where sub_name \
                like '%" + formatName + "%' and (unit == '通識核心' or unit == '外語文選修')").fetchall()
    conn.close()
    return result


def searchTeacher(name):
    name = clean(name)
    if name == '':
        return ()
    # generate target for like statement in sql
    formatName = '%'
    for c in list(name):
        formatName += c + '%'
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    result = c.execute(
        "select distinct comments.teacher, description from comments left join teacher on teacher.teacher = comments.teacher where teacher.teacher like '%" + formatName + "%'").fetchall()
    conn.close()
    result_dict = {}
    for elem in result:
        if not elem[0] in result_dict:
            result_dict[elem[0]] = []
        result_dict[elem[0]].append(elem[1])
    return (result_dict)
