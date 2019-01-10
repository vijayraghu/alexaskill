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
databasename = os.environ["databasename"]
databasehost = os.environ["databasehost"]
databaseusername = os.environ["databaseusername"]
databasepassword = os.environ["databasepassword"]

#Set key for session variables
SECRET_KEY = os.environ["SECRET_KEY"]
app.secret_key=SECRET_KEY

#Initialize Flask application
app = Flask(__name__)

#Receive POST request from Survey application
@app.route('/requestsurvey', methods=['GET','POST'])
def requestsurvey():
	phonenumber = 
	currentsurveystatus = "Question1"
	# Get the Question text and send SMS
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	curr.execute("SELECT * from survey_question_master where question_key='"+currentstatus"'")
	for r in curr:
		questiontext = r[1]
	# Send Request for Survey message
	sendSMS(phonenumber, questiontext, cli)
	query = "INSERT INTO customer_survey_master(ani, current_survey_status) values (%s,%s)"
	args = (phonenumber, currentsurveystatus)
	cur.execute(query,args)
	conn.commit()
	cur.close()
	conn.close()
	return str(response)

# Get ANI, SMS response and current survey status
@app.route('/startsurvey', methods=['GET','POST'])
def startsurvey():
	phonenumber = request.values.get('From')
	print (caller_phone_number)
	smsresponse = request.values.get('Body')
	currentsurveystatus = ""
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	cur.execute("SELECT * FROM customer_survey_master where ani='"+callerphonenumber"'")
	for r in curr:
		currentsurveystatus = r[1]
	cur.close()
	cur = conn.cursor()
	conn.close()
	sendsurveyquestion(phonenumber, smsresponse, currentsurveystatus)
	return ""
	
# Send questions based on survey status	
def sendsurveyquestion(phonenumber, smsresponse, currentsurveystatus):
	if currentsurveystatus == "Question1" and smsresponse == "Yes":
		conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
		# Get the number of questions
		cur = conn.cursor()
		curr.execute("SELECT count(question_key) from  survey_question_master")
		for r in curr:
			questioncount = int(r[0])-1
		i=1
		for i in range(i, questioncount):
			# Populate survey response table with response for Request for Survey
			query  = "INSERT INTO customer_survey_history(ani, question_key, customer_response) values (%s,%s,%s)"
			args = (phonenumber, currentstatus, smsresponse)
			cur.execute(query,args)
			# Update Survey master status to the question
			i=i+1
			questionnumber = currentstatus[0:8]+str(i)
			query = "UPDATE customer_survey_master set current_survey_status = %s where ani = %s"
			args = (questionnumber, phonenumber)
			cur.execute(query,args)
			conn.commit()
			curr.close()
			# Get the next question text and call send SMS
			cur = conn.cursor()
			curr.execute("SELECT * from survey_question_master where question_key='"+currentstatus"'")
			for r in curr:
				questiontext = r[1]
			curr.close()
			conn.close()
			sendSMS(phonenumber, questiontext, cli)
			return ""
		else:
			conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
			# Populate survey response table with response for Request for Survey stating Response is No
			query  = "INSERT INTO customer_survey_history(ani, question_key, customer_response) values (%s,%s,%s)"
			args = (phonenumber, currentstatus, smsresponse)
			cur.execute(query,args)
			conn.commit()
			curr.close()
			conn.close()
			return ""
		
# Send SMS function
def sendSMS(dnis, smsbody, cli):
	client = Client(account_sid, auth_token)
	client.messages.create(body=smsbody, 
			       from_=cli,
			       to=dnis
			      )
	return str(response)
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
