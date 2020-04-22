from flask import Flask, jsonify, request, redirect, url_for, abort
from flask_restful import Resource
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
	return 0


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)