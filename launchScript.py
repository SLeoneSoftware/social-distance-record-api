#Creates Users and Contacted Databases
import sqlite3

db = sqlite3.connect('record.sqlite3') 

users_qry = open('users.sql', 'r').read()
contacted_qry = open('contacted.sql', 'r').read()

conn = sqlite3.connect('record.sqlite3')
c = conn.cursor()
c.execute(users_qry)
conn.commit()
c.close()
conn.close()

conn = sqlite3.connect('record.sqlite3')
c = conn.cursor()
c.execute(contacted_qry)
conn.commit()
c.close()
conn.close()
