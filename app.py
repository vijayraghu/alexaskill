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
#from __future__ import print_function

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, "/")

#Helper function for Dialog Delegate
def get_dialog_state():
	return session['dialogState']

#Account Balance Intent
@ask.intent("AccountBalIntent")
def getAccount(accountnumberslot, accounttypeslot):
# delegate dialog to Alexa until all parameters are set
    	dialog_state = get_dialog_state()
    	print (dialog_state)
    	if dialog_state != "COMPLETED":
        	return delegate(None)
    	accnum = accountnumberslot
    	accounttype = accounttypeslot
    	print (accnum, accounttype)
    	Balance = getBalance(accnum, accounttype)
	#Send SMS with acknowledgement number
	#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	#client.messages.create(from_='+14696467609', 
				#to='+917338856833', 
				#body='Your ' + accounttype + ' account balance is ' + Balance + ' dollars'
				#)
    	speech = 'Your ' + accounttype + ' account balance is ' + Balance \
        	+ ' dollars'
    	return statement(speech).simple_card('Account_balance', speech)

#Last purchase Intent
@ask.intent("Lastpurchase")
def getAccount(accountnumberslot, accounttypeslot):
	dialog_state = get_dialog_state()
	print (dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	accnum = accountnumberslot
	accounttype = accounttypeslot
	print (accnum, accounttype)
	lastpurchase = getLastpurchase(accnum, accounttype)
	Amount = lastpurchase[0][u'amount']
	Purchaseamount = str(Amount)
	date = lastpurchase[0][u'purchase_date']
	Purchasedate = str(date)
	speech = 'The last purchase you made was on ' + Purchasedate + ' for ' + Purchaseamount \
		+ ' dollars'
	return statement(speech).simple_card('Last purchase', speech)

#Last transfer Intent
@ask.intent("Lasttransfer")
def getAccount(accountnumberslot, accounttypeslot):
	dialog_state = get_dialog_state()
	print (dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	accnum = accountnumberslot
	accounttype = accounttypeslot
	print (accnum, accounttype)
	lasttransfer = getLasttransfer(accnum, accounttype)
	Amount = lasttransfer[0][u'amount']
	Transferamount = str(Amount)
	date = lasttransfer[0][u'transaction_date']
	Transferdate = str(date)
	speech = 'The last transfer you made was on ' + Transferdate + ' for ' + Transferamount \
		+ ' dollars'
	return statement(speech).simple_card('Last transfer', speech)

#Callback Service
@ask.intent("Callbackrequest")
def callbackrequest(Scheduledate, Scheduletime):
	dialog_state = get_dialog_state()
	print(dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(None)
	Callbackdate = Scheduledate
	Callbacktime = Scheduletime
	print(Callbackdate, Callbacktime)
	client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	client.calls.create(from_='+14696467609', to='+919840610434', url=url_for('.outbound', _external=True))
	speech = 'Your callback request has been successfully submitted. You would be recieving a call on your registered mobile shortly'
	return statement(speech).simple_card('Callback request', speech)

#Outbound call to endpoint for callback service
@app.route('/outbound', methods=['POST'])
def outbound():
	response = VoiceResponse()
	response.say('This call is in regards to your callback request. Please hold while we transfer your call to an agent', voice='alice')
	response.dial('+917338856833')
	response.redirect('/process_close')
	return str(response)

@app.route('/process_close', methods=['GET', 'POST'])
def process_close():
	print ('in process_close')	

#Help Intent
@ask.intent('AMAZON.HelpIntent')
def help():
	speech = 'Hello. You can ask me for account balance or details about your last purchase or last transfer or you can schedule a call back request.'
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

#Helper function for Balance
def getBalance(accnum, accounttype):
	with open('details.json') as json_file:
		details = json.load(json_file)
		apiKey = os.environ.get('NESSIE_API_KEY')
		print (apiKey, accnum)
		if accounttype == 'Savings':
			accountId = details[accnum]['savings']
		elif accounttype == 'Checking':
			accountId = details[accnum]['checking']
		else:
			accountId = details[accnum]['credit Card']
		url = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(accountId, apiKey)
		print (url)
		response = requests.get(url, headers={'content-type': 'application/json'})
		result = response.json()
		accountbalance = result[u'balance']
		Balance = str(accountbalance)
		return Balance

#Helper function for Last transfer
def getLasttransfer(accnum, accounttype):
	with open('details.json') as json_file:
		details = json.load(json_file)
		apiKey = os.environ.get('NESSIE_API_KEY')
		print (apiKey, accnum)
		accountId = details[accnum][accounttype]
		print (accountId)
		url = 'http://api.reimaginebanking.com/accounts/{}/transfers?type=payer&key={}'.format(accountId, apiKey)
		response = requests.get(url, headers={'content-type': 'application/json'})
		lasttransfer = response.json()
		return lasttransfer

#Helper function for Last Purchase
def getLastpurchase(accnum, accounttype):
	with open('details.json') as json_file:
		details = json.load(json_file)
		apiKey = os.environ.get('NESSIE_API_KEY')
		print (apiKey, accnum)
		accountId = details[accnum][accounttype]
		print (accountId)
		url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountId, apiKey)
		response = requests.get(url, headers={'content-type': 'application/json'})
		lastpurchase = response.json()
		return lastpurchase
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
