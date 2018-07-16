#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json
import os
import requests
import datetime
#import twilio.twiml
from flask import Flask
from flask import jsonify
from flask import url_for
from flask import request
from flask import make_response
from flask_ask import Ask, request, session, question, statement, audio, delegate, context
from twilio.rest import Client

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, "/")

#Helper function for Dialog Delegate
def get_dialog_state():
	return session['dialogState']

#Launch skill messages
@ask.launch
def launched():
	if session.user.accessToken == None:
		return statement('To start using the Yorkshire Water skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		accesstoken = session.user.accessToken
		userdetails = get_user_info(accesstoken)
		if userdetails is None:
			return question('Hello. Welcome to the Yorkshire Water skill on Amazon Alexa. You can check your account balance, submit your meter reading, get your next payment date, request for a water meter or submit a callback request for one of our customer service agents to call you.')
		else:
			return question('Hello '+userdetails['name'].split(' ')[0]+'! Welcome to the Yorkshire Water skill on Amazon Alexa. ou can check your account balance, submit your meter reading, get your next payment date, request for a water meter or submit a callback request for one of our customer service agents to call you.')
      
#Submit Meter Reading Intent
@ask.intent("Submitmeterreading")
def submitReading(MeterReading):
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		# delegate dialog to Alexa until all parameters are set
		dialog_state = get_dialog_state()
		print (dialog_state)
		if dialog_state != "COMPLETED":
			return delegate(speech=None)
		# get account reference from access token
		accesstoken = session.user.accessToken
		accountreference = getaccountreference(accesstoken)
		meterreading = MeterReading
		print(accesstoken, accountreference, meterreading)
		# Send SMS with meter reading
		client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		client.messages.create(from_='+14696467609', 
				       to='+917338856833',
				       body='Your meter reading ' + meterreading +  '. is successfully submitted for your account reference number ' + accountreference +  '. Thank you')
		#speak out response
		return statement('<speak> Your meter reading <say-as interpret-as="digits">' + meterreading + '</say-as> is successfully submitted for your account reference number <say-as interpret-as="digits">' + accountreference +  '</say-as>. Thank you. We have sent you an SMS with the details to your mobile number. </speak>')

#Get Account Balance
@ask.intent("Accountbalance")
def accountBalance():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		# get account reference from access token
		accesstoken = session.user.accessToken
		accountreference = getaccountreference(accesstoken)
		print(accesstoken, accountreference)
		client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		client.messages.create(from_='+14696467609', 
				       to='+917338856833',
				       body='Your account balance is 450 pounds for your account reference number ' + accountreference +  '. Thank you')
		return statement('<speak> Your account balance is <say-as interpret-as="cardinal">450</say-as> pounds for your account reference number <say-as interpret-as="cardinal"> ' + accountreference +  '</say-as>. Thank you. We have sent you an SMS with the details to your mobile number. </speak>')
 
 #Next Payment Date Intent
@ask.intent("Paymentduedate")
def paymentduedate():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		# get account reference from access token
		accesstoken = session.user.accessToken
		accountreference = getaccountreference(accesstoken)
		print(accesstoken, accountreference)
		client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		client.messages.create(from_='+14696467609', 
				       to='+917338856833',
				       body='Your payment due date for your account reference number ' + accountreference +  '.is the 28th of July 2018. Thank you.')
		return statement('<speak> Your payment due date for your account reference number <say-as interpret-as="cardinal"> ' + accountreference +  '</say-as> is <say-as interpret-as="date">20180728</say-as> </speak>')

#Water Meter request Intent
@ask.intent("Meterequest")
def paymentduedate():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		# get account reference from access token
		accesstoken = session.user.accessToken
		accountreference = getaccountreference(accesstoken)
		print(accesstoken, accountreference)
		client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		client.messages.create(from_='+14696467609', 
				       to='+917338856833',
				       body='Your request for a water meter related to account reference number ' + accountreference +  'has been successfully placed. We will contact you within 7 business days.')
		return statement('Your request for water meter has been successfully placed. We will contact you within 7 business days. We have sent you an SMS to your mobile number.')

#Callback request Intent
@ask.intent("Callbackrequest")
def callbackrequest(Scheduledate):
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		#delegate dialog to Alexa until all parameters are set
		dialog_state = get_dialog_state()
		print(dialog_state)
		if dialog_state != "COMPLETED":
			return delegate(speech=None)
		# get account reference from access token
		Callbackdate = Scheduledate
		accesstoken = session.user.accessToken
		accountreference = getaccountreference(accesstoken)
		print(accesstoken, accountreference)
		client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		client.messages.create(from_='+14696467609', 
				       to='+917338856833',
				       body='Your callback has been scheduled between 10 AM and 11 AM on the ' + Callbackdate +  '. Thank you.' )
		return statement('<speak> Your callback has been scheduled between 10 A M and 11 A M on <say-as interpret-as="date"> ' + Callbackdate + '</say-as>. Thank you </speak>')

#Stop Intent
@ask.intent('AMAZON.StopIntent')
def stop():
	return statement("Goodbye")

#Cancel Intent
@ask.intent('AMAZON.CancelIntent')
def cancel():
	return statement("Goodbye")

#End Session Intent
@ask.session_ended
def session_ended():
	return "{}", 200

#Helper function for balance, account number and due date
def getaccountreference(accesstoken):
	accountreference = '4563746572'
	return accountreference

#Helper function for user information
def get_user_info(accesstoken):
    #print access_token
    amazonProfileURL = 'https://api.amazon.com/user/profile?access_token='
    r = requests.get(url=amazonProfileURL+accesstoken)
    if r.status_code == 200:
        return r.json()
    else:
        return False 
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')

 
