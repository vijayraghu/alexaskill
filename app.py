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
#from twilio.rest import TwilioRestClient
from flask_ask import Ask, request, session, question, statement, audio, delegate, context

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, "/")

#Helper function for Dialog Delegate
def get_dialog_state():
	return session['dialogState']

#Account Balance Intent
@ask.intent("Submitmeterreading")
def submitReading(AccountReference, MeterReading):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    CustAcc = AccountReference
    CustReading = MeterReading
    print (CustAcc, CustReading)
    #Submit = Submit(CustAcc, CustReading)
    #speech = 'Your meter reading ' + CustReading + ' is successfully submitted. Thank you '
    speech = '<speak> Your meter reading <say-as interpret-as="cardinal">' + CustReading + '</say-as> is successfully submitted. Thank you </speak>'
    speech = '<speak> Your meter reading <say-as interpret-as="cardinal">12345</say-as> is successfully submitted. Thank you </speak>'
    print (speech)
    return statement(speech).simple_card('Meter Reading', speech)

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
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
