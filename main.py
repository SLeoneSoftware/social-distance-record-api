from flask import Flask, jsonify, request, redirect, url_for, abort
from flask_restful import Resource
import sqlite3
import distance



app = Flask(__name__)
con = sqlite3.connect('record.sqlite3')

@app.route('/updatelocation/<id>/<latitude>/<longitude>')
def updatelocation(uid, latitude, longitude):
	#Update Database
	cur = con.cursor()
	cur.execute('UPDATE users SET latitude = ?, longitude = ? WHERE id = ?', (latitude, longitude, uid))
	con.commit()
	#Search for users in contact
	cur.execute('SELECT zipcode from users WHERE id = ?', (uid,))
	zipcode, = cur.fetchone()
	cur.execute('SELECT latitude, longitude, id from users WHERE zipcode = ?', (zipcode))
	while True:
		row = cur.fetchone()
		if row == None:
			break
		lat_two,long_two, uid_two = row
		social_distance = distance.calculate(latitude, longitude,lat_two, long_two) / 3280.839895 #changing km to feet
		#account for +/- 3 feet in location
		if social_distance < 9:
			#add contact
			cur2 = con.cursor()
			time = ''
			date = ''
			cur2.execute('INSERT INTO contacted (user, contacteduser, datemark, timemark) VALUES (?, ?, ?)', (uid, uid_two, date, time))
			cur2.execute('INSERT INTO contacted (user, contacteduser, datemark, timemark) VALUES (?, ?, ?)', (uid_two, uid, date, time))
	con.commit()
	return 0


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)