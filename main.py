from flask import Flask, jsonify, request, redirect, url_for, abort
from flask_restful import Resource
import sqlite3
import distance
from datetime import datetime
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

#Changing path due to hosting services used
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))



app = Flask(__name__)

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def get_zipcode(latitude, longitude):
	con = sqlite3.connect(os.path.join(THIS_FOLDER, 'record.sqlite3'))
	cur = con.cursor()
	zipcode_query_result = cur.execute('SELECT * from zipcodes')
	zipcodes = zipcode_query_result.fetchall()
	zipcodes.sort(key = lambda x: distance.calculate(float(latitude), float(longitude), float(x[1]), float(x[2])))
	zipcode = zipcodes[0][0]
	con.close()
	return zipcode

@app.route('/confirmemail/<uid>/<encrypted>', methods = ['PUT'])
def confirmemail(uid, encrypted):
	con = sqlite3.connect(os.path.join(THIS_FOLDER, 'record.sqlite3'))
	cur = con.cursor()
	cur.execute('SELECT encrypted from encryptions where id = ?', (uid,))
	row = cur.fetchone()
	logged_encrypted, = row
	if logged_encrypted == encrypted:
		cur.execute('UPDATE users SET confirmed = 1 where id = ?', (uid,))
		cur.execute('DELETE FROM encryptions WHERE id = ?', (uid,))
		con.commit()
		con.close()
		return '<div> Your account has been confirmed. Thank you! </div>'
	else:
		con.commit()
		con.close()
		return '<div> There was a problem with your account. This will be reviewed shortly. Please reply to your confirmation email if you think this is an error. </div>'


@app.route('/adduser/<firstname>/<email>/<latitude>/<longitude>', methods = ['POST'])
def adduser(firstname, email, latitude, longitude):
	con = sqlite3.connect(os.path.join(THIS_FOLDER, 'record.sqlite3'))
	cur = con.cursor()
	zipcode = get_zipcode(latitude, longitude)
	cur.execute('SELECT count(*) from users')
	count, = cur.fetchone()
	count += 10000000
	cur.execute('INSERT INTO users (id, firstname, email, zipcode, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)', (int(count), str(firstname), str(email), zipcode, latitude, longitude))
	#Send email confirmation
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	message_template = read_template('confirmation.txt')
	from dotenv import load_dotenv
	load_dotenv()
	MY_ADDRESS = token = os.environ.get("MY_ADDRESS")
	PASSWORD = token = os.environ.get("PASSWORD")
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To'] = email
	msg['Subject']="Social Distance Record Confirmation Email"
	import secrets
	encrypted = secrets.token_urlsafe(16)
	cur.execute('INSERT INTO encryptions (id, encrypted) VALUES (?, ?)', (int(count), encrypted ))
	link = 'SUPER_SECRET_LINK'
	message = message_template.substitute(PERSON_NAME=link)
	msg.attach(MIMEText(message, 'plain'))
	s.send_message(msg)
	del msg
	#End email confirmation section
	con.commit()
	con.close()
	json = {}
	json['id'] = count
	return jsonify(json)

@app.route('/updatelocation/<uid>/<latitude>/<longitude>', methods = ['PUT'])
def updatelocation(uid, latitude, longitude):
	#Update Database
	con = sqlite3.connect(os.path.join(THIS_FOLDER, 'record.sqlite3'))
	cur = con.cursor()
	zipcode = get_zipcode(latitude, longitude)
	cur.execute('UPDATE users SET zipcode = ?, latitude = ?, longitude = ? WHERE id = ?', (zipcode, latitude, longitude, uid))
	con.commit()
	#Search for users in contact
	#cur.execute('SELECT zipcode FROM users WHERE id = ?', (uid,))
	#zipcode, = cur.fetchone()
	cur.execute('SELECT latitude, longitude, id FROM users WHERE zipcode = ? AND id != ?', (zipcode,uid))
	while True:
		row = cur.fetchone()
		if row == None:
			break
		lat_two,long_two, uid_two = row
		social_distance = distance.calculate(float(latitude), float(longitude),float(lat_two), float(long_two)) / 3280.839895 #changing km to feet
		#account for +/- 3 feet in location
		if social_distance < 9:
			#add contact
			cur2 = con.cursor()
			'''
			Times have been replaced; logic is now done by database. This is left commented rather than deleted for slight editing reasons.
			timestamp = str(datetime.now())
			date = timestamp[0:10]
			time = timestamp[11:16]
			'''
			cur2.execute('INSERT INTO contacted (user, contacteduser) VALUES (?, ?)', (uid, uid_two))
			cur2.execute('INSERT INTO contacted (user, contacteduser) VALUES (?, ?)', (uid_two, uid))
	con.commit()
	con.close()
	json = {}
	json['result'] = 'success'
	return jsonify(json)

@app.route('/testedpositive/<uid>', methods = ['POST'])
def testedpositive(uid):
	con = sqlite3.connect(os.path.join(THIS_FOLDER, 'record.sqlite3'))
	cur = con.cursor()
	cur.execute('SELECT contacted.datemark, users.email, users.firstname, users.confirmed FROM contacted JOIN users on contacted.contacteduser = users.id  WHERE contacted.user = ? AND contacted.contacteduser != ? AND contacted.datemark >= DateTime("Now", "LocalTime", "-14 Day")', (uid,uid))
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
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
		date, email, name, confirmed = row
		if confirmed == 0:
			continue
		message = message_template.substitute(PERSON_NAME=name)
		msg['From']=MY_ADDRESS
		msg['To'] = email
		msg['Subject']="You contacted a COVID-19 positive patient on " + date + "."
		msg.attach(MIMEText(message, 'plain'))
		s.send_message(msg)
		del msg
	con.close()
	json = {}
	json['result'] = 'success'
	return jsonify(json)

if __name__ == '__main__':
	success = True
	#app.debug = True
	#app.run(host='0.0.0.0', port=3000)
