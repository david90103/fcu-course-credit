import sqlite3

c = sqlite3.connect('department.db')
c.execute('''PRAGMA foreign_keys = ON;''')

print ("Opened database successfully");

c.execute('''CREATE TABLE department(
  id   INTEGER,
  Department   TEXT,
  Department_Compulsory   INTEGER,
  Department_Elective     INTEGER,
  Other_Department_Elective     INTEGER,
  General_Compulsory     INTEGER,
  General_Elective     INTEGER
);''')

print("Table created successfully");


c.commit()
c.close()
