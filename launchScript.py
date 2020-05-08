#Creates Users and Contacted Databases
import sqlite3
import numpy
import os
#Use this next line as the only connection later on
#db = sqlite3.connect('record.sqlite3') 

def load_zipcodes(file='zipcodes.txt',path='data',datatype=str):
	data = numpy.genfromtxt(os.path.join(path,file),delimiter=',',dtype=datatype)
	conn = sqlite3.connect('record.sqlite3')
	c = conn.cursor()
	for row in data:
		c.execute('INSERT INTO zipcodes (zipcode, latitude, longitude) VALUES (?,?,?)', (row[0], float(row[1]), float(row[2])))
	conn.commit()
	c.close()
	conn.close()
def run():
	users_qry = open('users.sql', 'r').read()
	contacted_qry = open('contacted.sql', 'r').read()
	zipcodes_qry = open('zipcodes.sql', 'r').read()

	conn = sqlite3.connect('record.sqlite3')
	c = conn.cursor()
	c.execute(zipcodes_qry)
	conn.commit()
	c.close()
	conn.close()

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
	load_zipcodes()

