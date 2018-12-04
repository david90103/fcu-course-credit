import sqlite3
conn = sqlite3.connect('course.db')
c = conn.cursor()
c.execute('''create table course(
teacher TEXT,
course TEXT,
department TEXT,
star TEXT,
a TEXT,
b TEXT,
c TEXT
);''')
conn.commit()
conn.close()
