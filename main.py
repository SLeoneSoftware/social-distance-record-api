from flask import Flask, jsonify, request, redirect, url_for, abort
from flask_restful import Resource
from distance import distance



app = Flask(__name__)

@app.route('/updatelocation/<id>/<latitude>/<longitude>')
def updatelocation(id, latitude, longitude):
	return 0

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)