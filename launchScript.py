import sqlite3

db = sqlite3.connect('record.sqlite3') 

qry = open('users.sql', 'r').read()
conn = sqlite3.connect('record.sqlite3')
c = conn.cursor()
c.execute(qry)
conn.commit()
c.close()
conn.close()
