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

#Submit Meter Reading Intent
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
    speech = '<speak> Your meter reading <say-as interpret-as="digits">' + CustReading + '</say-as> is successfully submitted. Thank you </speak>'
    print (speech)
    return statement(speech).simple_card('Meter Reading', speech)
	
#Account Balance Intent
@ask.intent("Accountbalance")
def accountBalance(AccountReference):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    CustAcc = AccountReference
    print (CustAcc)
    speech = '<speak> Your account balance is <say-as interpret-as="cardinal">450</say-as> pounds. Thank you </speak>'
    print (speech)
    return statement(speech).simple_card('Account Balance', speech)
	
#Next Payment Date Intent
@ask.intent("Paymentduedate")
def paymentduedate(AccountReference):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    CustAcc = AccountReference
    print (CustAcc)
    speech = '<speak> Your payment due date is <say-as interpret-as="date">20180528</say-as> </speak>'
    print (speech)
    return statement(speech).simple_card('Payment Due Date', speech)
	
#Water Meter request Intent
@ask.intent("Watermeterrequest")
def paymentduedate(AccountReference):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    CustAcc = AccountReference
    print (CustAcc)
    speech = '<speak> Your request for water meter has been successfully placed. We will contact you within 7 days </speak>'
    print (speech)
    return statement(speech).simple_card('Water Meter request', speech)
	
#Callback request Intent
@ask.intent("Callbackrequest")
def callbaclrequest(AccountReference, Scheduledate):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    CustAcc = AccountReference
    Callbackdate = Scheduledate
    print (CustAcc, Callbackdate)
    speech = '<speak> Your callback has been scheduled between 10 A M and 11 A M on <say-as interpret-as="date">' + Callbackdate + '</say-as>. Thank you </speak>'
    print (speech)
    return statement(speech).simple_card('Callback request', speech)

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
