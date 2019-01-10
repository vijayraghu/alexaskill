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
	client = Client(account_sid, auth_token)
	client.messages.create(body=text, 
			       from_=cli,
			       to=dnis
			      )
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	query = "INSERT INTO customer_survey_master("ani, current_survey_status) values (%s,%s)"
	args = (dnis, currentsurveystatus)
	cur.execute(query,args)
	conn.commit()
	cur.close()
	conn.close()
	return str(response)

#Proceed with survey based on response from Customer
@app.route('/startsurvey', methods=['GET','POST'])
def startsurvey():
	callerphonenumber = request.values.get('From')
	print (caller_phone_number)
	input_text = request.values.get('Body')
	conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
	cur = conn.cursor()
	cur.execute("SELECT * FROM customer_survey_master where ani='"+callerphonenumber"'")
	current_status = ""
	for r in curr:
		current_status = r[0]
	cur.close()
	conn.close()
	if current_status == "RequestforSurvey":
		conn = pymysql.connect(host=databasehost, user=databaseusername, passwd=databasepassword, port=3306, db=databasename)
		cur = conn.cursor()
		cur.execute("SELECT * FROM customer_survey_master where ani='"+callerphonenumber"'")
		# Send Request for Survey message
		client = Client(account_sid, auth_token)
		client.messages.create(body=text, 
				       from_=cli, 
				       to=callerphonenumber
				      )
		if input_text == "Yes":
		
	
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
