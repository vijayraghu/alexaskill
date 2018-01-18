#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json
import os
import requests
import datetime
import twilio.twiml
from flask import Flask
from flask import jsonify
from flask import url_for
from flask import request
from flask import make_response
from twilio.rest import TwilioRestClient
from flask_ask import Ask, request, session, question, statement, audio, delegate

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, "/")

#Helper function for Dialog Delegate
def get_dialog_state():
	return session['dialogState']

#Account Balance Intent
@ask.intent('Account_balance')
def getAccount(account_nameslot, account_typeslot):
# delegate dialog to Alexa until all parameters are set
    dialog_state = get_dialog_state()
    print dialog_state
    if dialog_state != COMPLETED_DIALOG_STATE:
        return delegate(speech=None)
    custname = account_nameslot
    accounttype = account_typeslot
    print custname, accounttype
    Balance = getBalance(custname, accounttype)
    speech = 'Your ' + accounttype + ' account balance is ' + Balance \
        + ' dollars'
    return statement(speech).simple_card('Account_balance', speech)

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
def getBalance(nickname, Accounttype):
    with open('details.json') as json_file:
        details = json.load(json_file)
        apiKey = os.environ.get('NESSIE_API_KEY')
        print apiKey
        if Accounttype == 'Savings':
            accountId = details[nickname]['Savings']
        elif Accounttype == 'Checking':
            accountId = details[nickname]['Checking']
        else:
            accountId = details[nickname]['Credit Card']
        url = \
            'http://api.reimaginebanking.com/accounts/{}?key={}'.format(accountId,
                apiKey)
        print url
        response = requests.get(url,
                                headers={'content-type': 'application/json'
                                })
        result = response.json()
        accountbalance = result[u'balance']
        Balance = str(accountbalance)
        return Balance
		
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print 'Starting app on port %d' % port
	app.run(debug=False, port=port, host='0.0.0.0')
