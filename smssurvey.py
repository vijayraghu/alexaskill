#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import urllib
import requests
import json
from flask import Flask, request, Response, make_response, jsonify, url_for
import pymysql
# Twilio Helper Library
from twilio.rest import Client

# Declare global variables
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
cli = os.environ["cli"]
surveyappurl = "<<url of survey application>>"
databasename = os.environ["databasename"]
databasehost = os.environ["databasehost"]
databaseusername = os.environ["databaseusername"]
databasepassword = os.environ["databasepassword"]

#Initialize Flask application
app = Flask(__name__)

#Receive POST request from Survey application
@app.route('/requestsurvey', methods=['GET','POST'])
def requestsurvey():
	phonenumber = request.values.get("phonenumber", None)
	questiontext = request.values.get("questiontext", None)
	surveyid = request.values.get("surveyid", None)
	userid = request.values.get("userid", None)
	# Update table and send SMS
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	query = "INSERT INTO customer_survey_master(ani, cli, question, surveyid, userid) values (%s,%s,%s,%s)"
	args = (phonenumber, cli, questiontext, surveyid, userid)
	cur.execute(query,args)
	conn.commit()
	cur.close()
	conn.close()
	# Send Request for Survey message
	sendSMS(phonenumber, questiontext, cli)
	return ""

# Get ANI, SMS response update to database
@app.route('/receiveresponse', methods=['GET','POST'])
def receiveresponse():
	phonenumber = request.values.get('From')
	senttonumber = request.values.get('To')
	smsresponse = request.values.get('Body')
	print (phonenumber, senttonumber, smsresponse)
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	query = "UPDATE customer_survey_master set response = %s where ani = %s and cli = %s"
	args = (smsresponse, phonenumber, senttonumber)
	cur.execute(query,args)
	conn.commit()
	cur.close()
	postresponse(phonenumber, senttonumber)
	return ""

# POST Response back to survey application
def postresponse(ani, dnis):
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	curr.execute("SELECT * from survey_question_master where ani="+ani" and dnis="+dnis"")
	for r in curr:
		ani = r[0]
		dnis = r[1]
		question = r[2]
		response = r[3]
		surveyid = r[4]
		userid = r[5]
	payload = {'ani': ani, 'dnis': dnis, 'question':question, 'surveyid':surveyid, 'userid':userid}
	requests.request("POST", url=surveyappurl, data=json.dumps(payload))
	return ""

# Send SMS function
def sendSMS(dnis, questiontext, cli):
	client = Client(account_sid, auth_token)
	client.messages.create(body=questiontext, 
			       from_=cli,
			       to=dnis
			      )
	return str(response)
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
