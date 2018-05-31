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

#Add channel Intent
@ask.intent("addchannel")
def channeladd(channel):
	# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print (dialog_state)
    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    channelname = channel
    print (channelname)
    channelprice = getchannelprice(channelname)
    speech = '<speak>' + channelname +  'can be added to your account for just ' + channelprice +  '. Do you want to go ahead and add it to your account? </speak>'
    #speech = '<speak>' + channelname +  'can be added to your account for just <say-as interpret-as="digits">' + channelprice + '</say-as> is successfully submitted. Thank you </speak>'
    print (speech)
    return statement(speech).simple_card('Channel', speech)
    
#Yes Intent
@ask.intent('AMAZON.YesIntent')
def yes_intent():
	  channelname = 'cinemax channel'
	  return statement('Ok. ' + channelname + ' has been added to your account')
	
#No Intent
@ask.intent('AMAZON.YesIntent')
def no_intent():
	  return statement("Goodbye")

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

#Helper function for channelprice
def getchannelprice(channelname):
	  #channelname == 'cinemax channel':
	  channelprice == 'Thirteen dollars and ninety nine cents'
	  return channelprice
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
