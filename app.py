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

# Declaring Twilio credentials
account_sid = 'AC4f811e2ef41e640a2dedbb43e40ac77f'
auth_token = 'ba2d0e0eaf43f49c34427054b7c41778'
client = Client(account_sid, auth_token)

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, "/")

#Helper function for Dialog Delegate
def get_dialog_state():
	return session['dialogState']

#Get account balance
@ask.intent("accountbalance")
def Accountbalance():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.LinkAccount_card()
	else:
#delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
	  session.user.accessToken = accessToken
    balance, accnumber, duedate  = getbalance(accessToken)
    print (balance, accnumber, duedate)
    #session.attributes['intent_name'] = "addchannel"
    #session.attributes['channel_name'] = channelname
    #speech = '<speak>' + channelname +  'can be added to your account for just ' + channelprice +  '. Do you want to go ahead and add it to your account? </speak>'
	  message = client.messages \
                .create(
                     body="Your account balance is " + balance +  ". Your account number is " + accnumber + " and your bill due date is the " + duedate + ". We have sent you an SMS with the details to your mobile number.",
                     from_='+14696467609',
                     to='+9840610434'
                 )
	  print(message.sid)
    return statement('Your account balance is ' + balance +  '. Your account number is ' + accnumber + ' and your bill due date is the ' + duedate + '. We have sent you an SMS with the details to your mobile number.')
	#.simple_card('Channel', speech)

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
def getbalance(accessToken):
	  balance = 'Thirteen dollars and ninety nine cents'
	  accnumber = '34567654'
	  duedate = '06/20/2018'
	  return balance, accnumber, duedate
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')