import requests
import sqlite3
from bs4 import BeautifulSoup
conn = sqlite3.connect('comments.db')
c = conn.cursor()
res = requests.get('https://babu7.github.io/2.html')
soup = BeautifulSoup(res.text, "html")

a = soup.select('tr')
for test in soup.select('tr'):
  k=1
  temp=''
  tempp=''
  aa=[]
  for i in test.select('td'):
    if(k!=1 and k!=8):
      aa.append(i.text.split('\r\n')[0])
      k+=1
    else:
      k+=1
  if len(aa)!=0:
    for p in range(2, 5):
      if '\'' in aa[p]:
        tempaa=aa[p].split('\'')
        aa[p]=tempaa[0]+tempaa[1]
      tempp = tempp + aa[p]
    temp = '\''+aa[6]+'\''+','+'\''+tempp+'\''
    c.execute("INSERT INTO comments (teacher,description) \
     VALUES ("+temp+" )")

conn.commit()
conn.close()
