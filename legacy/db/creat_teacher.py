import sqlite3
conn = sqlite3.connect('teacher.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS teacher")

sql='''CREATE TABLE teacher (
teacher TEXT,
department TEXT,
star TEXT)'''

c.execute(sql)

conn.commit()
conn.close()
