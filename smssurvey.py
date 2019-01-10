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
	dnis = 
	currentsurveystatus = "RequestforSurvey"
	text = "You have been selected as a survey participant. Kindly respond by stating Yes if you want to take the survey or No if you want to opt out'
	# Send Request for Survey message
	sendSMS(dnis, text, cli)
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	query = "INSERT INTO customer_survey_master(ani, current_survey_status) values (%s,%s)"
	args = (dnis, currentsurveystatus)
	cur.execute(query,args)
	conn.commit()
	cur.close()
	conn.close()
	return str(response)

# Get ANI, SMS response and current survey status
@app.route('/startsurvey', methods=['GET','POST'])
def startsurvey():
	callerphonenumber = request.values.get('From')
	print (caller_phone_number)
	input_text = request.values.get('Body')
	current_status = ""
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	cur.execute("SELECT * FROM customer_survey_master where ani='"+callerphonenumber"'")
	for r in curr:
		current_status = r[1]
	cur.close()
	cur = conn.cursor()
	conn.close()
	sendsurveyquestion(callerphonenumber, input_text, current_status)
	return ""
	
# Send questions based on survey status	
def sendsurveyquestion(phonenumber, smsresponse, currentstatus):
	if currentstatus == "RequestforSurvey":
		conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
		# Populate survey response table with response for Request for Survey
		cur = conn.cursor()
		query  = "INSERT INTO customer_survey_history(ani, question_key, customer_response) values (%s,%s,%s)"
		args = (phonenumber, currentstatus, smsresponse)
		cur.execute(query,args)
		conn.commit()
		cur.close()
		# Update Survey master status to Question 1
		cur = conn.cursor()
		query = "UPDATE customer_survey_master set current_survey_status = %s where ani = %s"
		args = ('Question 1', phonenumber)
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
		# Get the number of questions
		cur = conn.cursor()
		curr.execute("SELECT count(question_key) from  survey_question_master")
		for r in curr:
			questioncount = int(r[0])-1
		i=0
		for i in questioncount
		# Populate survey response table with response for Question
		
		
	
			    
# Send SMS function
def sendSMS(dnis, smsbody, cli):
	client = Client(account_sid, auth_token)
	client.messages.create(body=smsbody, 
			       from_=cli,
			       to=dnis
			      )
	return ""

	
	
	
	

	question1 = "What do you think about the service you experienced. Please respond by choosing one of the options - Very Good, Good, Satisfactory, Dissatisfied'
	question2 = "Will you recommend our service. Please respond by choosing one of the options - Definitely, Yes, No'
	
	
	
	
	
	apiai_language = 'en'
	
	#Sending and getting response from Dialogflow
	headers = {'authorization': 'Bearer ' + apiai_client_access_key, 
			   'content-type': 'application/json'
			  }
	payload = {'query': input_text , 
			   'lang': apiai_language, 
			   'sessionId': user_id
			  }
	response = requests.request("POST", url=apiai_url, data=json.dumps(payload), headers=headers, params=apiai_querystring)
	print (response.text)
	output = json.loads(response.text)
	output_text = output['result']['fulfillment']['speech']
	#output_text = output_text.decode('utf-8')
				
	# Send whatsapp with dialogflow response
	client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	client.messages.create(body=output_text, 
			       from_='whatsapp:+14155238886', 
			       to=caller_phone_number
			      )					  
	return str(response)
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
