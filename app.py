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
from twilio.twiml.voice_response import VoiceResponse, Gather, Say, Dial

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
	#client.messages.create(from_='+14696467609', 
			       #to='+15108949478',
			       #body='Your request for appointment on the ' + appointment_date +  ' at ' + appointment_time + '. been successfully submitted. The service request number is 456756435.'
			      #)
	#speak out response
	return statement('<speak> Your request for an appointment on the ' + appointment_date + ' at ' + appointment_time + '. has been successfully submitted. The service request number is <say-as interpret-as="digits">456756435</say-as> <break time="1s"/> We have sent you an SMS with the details to your mobile number.</speak>')

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
			       #to='+15108949478',
			       #body='Your request for preorder of ' + preorder_product + ' has been successfully accepted. The reference number is 876546756.'
			      #)
	#speak out response
	return statement('<speak> Your request for preorder of ' + preorder_product + ' has been successfully accepted. The reference number is <say-as interpret-as="digits">876546756</say-as> <break time="1s"/> We have sent you an SMS with the details to your mobile number.</speak>')

#Callback Service
@ask.intent("Callbackrequest")
def callbackrequest(Scheduledate, Scheduletime):
	dialog_state = get_dialog_state()
	print(dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	Callbackdate = Scheduledate
	Callbacktime = Scheduletime
	print(Callbacktime, Callbackdate)
	#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	#client.calls.create(from_='+14696467609', to='+15108949478', url=url_for('.outbound', _external=True))
	speech = 'Your callback request has been successfully submitted. You would be recieving a call on your mobile shortly'
	return statement(speech).simple_card('Callback request', speech)

#Outbound call to endpoint for callback service
@app.route('/outbound', methods=['POST'])
def outbound():
	response = VoiceResponse()
	response.say('This call is in regards to your callback request. Please hold while we transfer your call to an agent', voice='alice')
	response.dial('+13026606019')
	response.redirect('/process_close')
	return str(response)

@app.route('/process_close', methods=['GET', 'POST'])
def process_close():
	print ('in process_close')
	
#Help Intent
@ask.intent('AMAZON.HelpIntent')
def help():
	speech = 'Hello. You can schedule an appointment at a genius bar store, place a pre-order request for an apple product or schedule a call back to speak to our customer service representative.'
	return question(speech).simple_card('Help', speech)

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
