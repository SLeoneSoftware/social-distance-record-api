from flask import Flask, jsonify, request, redirect, url_for, abort
from flask_restful import Resource
import sqlite3
import distance
from datetime import datetime
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



app = Flask(__name__)

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

@app.route('/adduser/<firstname>/<email>/<phone>/<latitude>/<longitude>')
def adduser(firstname, email, phone, latitude, longitude):
	con = sqlite3.connect('record.sqlite3')
	cur = con.cursor()
	#TODO: Add in Zipcode functionality later 
	zipcode = 11111
	#
	cur.execute('SELECT count(*) from users')
	count, = cur.fetchone()
	print(count)
	count += 10000000
	cur.execute('INSERT INTO users (id, firstname, email, phone, zipcode, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', (int(count), str(firstname), str(email), str(phone), zipcode, int(latitude), int(longitude)))
	con.commit()
	con.close()
	return '<div> Test: Success </div>'

@app.route('/updatelocation/<id>/<latitude>/<longitude>')
def updatelocation(uid, latitude, longitude):
	#Update Database
	con = sqlite3.connect('record.sqlite3')
	cur = con.cursor()
	cur.execute('UPDATE users SET latitude = ?, longitude = ? WHERE id = ?', (latitude, longitude, uid))
	con.commit()
	#Search for users in contact
	cur.execute('SELECT zipcode FROM users WHERE id = ?', (uid,))
	zipcode, = cur.fetchone()
	cur.execute('SELECT latitude, longitude, id FROM users WHERE zipcode = ?', (zipcode))
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
			timestamp = str(datetime.now())
			date = timestamp[0:10]
			time = timestamp[11:16]
			cur2.execute('INSERT INTO contacted (user, contacteduser, datemark, timemark) VALUES (?, ?, ?)', (uid, uid_two, date, time))
			cur2.execute('INSERT INTO contacted (user, contacteduser, datemark, timemark) VALUES (?, ?, ?)', (uid_two, uid, date, time))
	con.commit()
	con.close()
	return 0

@app.route('/testedpositive/<id>')
def testedpositive(uid):
	con = sqlite3.connect('record.sqlite3')
	cur = con.cursor()
	cur.execute('SELECT contacted.contacteduser, contacted.datemark, contacted.timemark, user.email FROM contacted JOIN user on contacted.contacteduser = user.id  WHERE contacted.user = uid')
	s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()
	from dotenv import load_dotenv
	load_dotenv()
	MY_ADDRESS = token = os.environ.get("MY_ADDRESS")
	PASSWORD = token = os.environ.get("PASSWORD")
	s.login(MY_ADDRESS, PASSWORD)
	message_template = read_template('message.txt')
	while True:
		row = cur.fetchone()
		if row == None:
			break
		msg = MIMEMultipart()
		message = message_template.substitute(PERSON_NAME=name)
		name, date, time, email = row
		msg['From']=MY_ADDRESS
		msg['To'] = email
		msg['Subject']="You contacted a COVID-19 positive patient on " + date + " at " + time + "."
		s.send_message(msg)
		del msg
	con.close()
	return 0

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)