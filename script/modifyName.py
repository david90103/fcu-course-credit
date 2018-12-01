import sqlite3


conn = sqlite3.connect('database.db')
c = conn.cursor()
result = c.execute("select distinct Department from department").fetchall()
# c.execute("insert into modifyName (short, long) values (null, '132')")
for e in result:
    a = (e[0])
    c.execute("insert into modifyName (short, long) values (null, ?)", (a,))
    # print (len(e[0]))

conn.commit()
conn.close()
