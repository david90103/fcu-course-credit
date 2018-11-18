import sqlite3


def getClassList(unitName):
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    result = c.execute("select distinct sub_name, sub_credit, scj_scr_mso, unit, year from course \
                where unit == '" + unitName + "' or unit == '英文綜合班' or unit == '核心必修綜合班'").fetchall()
    conn.close()
    return result


def findGeneral(className):
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    result = c.execute("select distinct sub_name from course where sub_name \
                like '%" + className + "%' and (unit == '通識核心' or unit == '外語文選修')").fetchall()
    conn.close()
    return result
