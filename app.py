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

#Appointment Booking Intent
@ask.intent("geniusbar_appointment")
def book_appointment(device_serial_number, phone_number, appointment_date, appointment_time, problem_statement, zip_code):
	# delegate dialog to Alexa until all parameters are set
	dialog_state = get_dialog_state()
	print (dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	print(device_serial_number, phone_number, appointment_date, appointment_time, problem_statement, zip_code)
	# Send SMS with acknowledgement number
	#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	#client.messages.create(body='Your request for appointment on the ' + appointment_date +  ' at ' + appointment_time + '. been successfully submitted. The service request number is 456756435. You will receive an email with further details shortly', 
			       #from_='whatsapp:+14155238886', 
			       #to='whatsapp:+919840610434'
			      #)
	#speak out response
	return statement('<speak> Your request for appointment on the ' + appointment_date + ' at ' + appointment_time + '. been successfully submitted. The service request number is <say-as interpret-as="cardinal">456756435</say-as>. We have sent you an SMS with the details to your mobile number.</speak>')

#Pre-order device
@ask.intent("pre_order_device")
def pre_order(preorder_product, delivery_location, phone_number, collection_mode):
	## delegate dialog to Alexa until all parameters are set
	dialog_state = get_dialog_state()
	print (dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	print(preorder_product, delivery_location, phone_number, collection_mode)
	# Send SMS with acknowledgement number
	#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	#client.messages.create(from_='+14696467609', 
			       #to='+917338856833',
			       #body='Your request for preorder of ' + preorder_product + ' has been successfully accepted. The reference number is 876546756. You will receive an email with further details shortly '
			      #)
	#speak out response
	return statement('<speak> Your request for preorder of ' + preorder_product + ' has been successfully accepted. The reference number is <say-as interpret-as="cardinal">876546756</say-as>.We have sent you an SMS with the details to your mobile number.</speak>')
 
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
