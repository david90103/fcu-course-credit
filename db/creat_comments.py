import sqlite3
conn = sqlite3.connect('comments.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS comments")

sql='''CREATE TABLE comments (
teacher TEXT,
description TEXT)'''

c.execute(sql)

conn.commit()
conn.close()
