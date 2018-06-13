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
		return statement('To start using the Optus skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		accesstoken = session.user.accessToken
		userdetails = get_user_info(accesstoken)
		if userdetails is None:
			return question('Hello. Welcome to the Optus skill on Amazon Alexa. You can check your account balance, your data usage and get answers to questions on relocation request, learn what to do if your phone has no signal or how to enable internet on your phone. What do you want to do today')
		else:
			return question('Hello '+userdetails['name'].split(' ')[0]+'! Welcome to the Optus skill on Amazon Alexa. You can check your account balance, your data usage and get answers to questions on relocation request, learn what to do if your phone has no signal or how to enable internet on your phone. What do you want to do today')

#Get account balance
@ask.intent("accountbalance")
def Accountbalance():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		accesstoken = session.user.accessToken
		print(accesstoken)
		balance, accnumber, duedate  = getbalance(accesstoken)
		print(balance, accnumber, duedate)
		#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		#client.messages.create(from_='+14696467609', 
				       #to='+61421183854',
				       #body='Your balance is ' + balance +  '. Your account number is ' + accnumber + ' and bill is due on ' + duedate)
		return statement('<speak> Your account balance is ' + balance +  '. Your account number is <say-as interpret-as="digits">  ' + accnumber + '</say-as> and your bill due date is ' + duedate + '. We have sent you an SMS with the details to your mobile number. </speak>')
	#.simple_card('Channel', speech)
  
#Get data usage status
@ask.intent("datausage")
def DataUsage():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
		accesstoken = session.user.accessToken
		print(accesstoken)
		consumedpercent, datacap, remainingdata, effectivedate  = getusage(accesstoken)
		print(consumedpercent, datacap, remainingdata, effectivedate)
		#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		#client.messages.create(from_='+14696467609', 
				       #to='+61421183854',
				       #body='You have used ' + consumedpercent +  ' of your monthly limit of ' + datacap + ' data and have ' + remainingdata + ' left until ' + effectivedate)
		return statement('You have used ' + consumedpercent +  ' of your monthly limit of ' + datacap + ' data and have ' + remainingdata + ' left until ' + effectivedate +  '. You can get more details about your data breakdown in Myoptus app or login to your account at www.optus.com.au')
	#.simple_card('Channel', speech)
  
#Submit relocate request
@ask.intent("relocaterequest")
def RelocateRequest():
	if session.user.accessToken == None:
		return statement('To start using this skill, please use the companion app to authenticate on Amazon') \
			.link_account_card()
	else:
#delegate dialog to Alexa until all parameters are set
		dialog_state = get_dialog_state()
		print(dialog_state)
		if dialog_state != "COMPLETED":
			return delegate(speech=None)
		accesstoken = session.user.accessToken
		print(accesstoken)
		session.attributes['intent_name'] = "relocaterequest"
		return question('<speak> You can now apply for a relocation request online or chat with our customer service or else call us at <say-as interpret-as="telephone"> 1300555241 </say-as> <break time="1500ms"/> Would you like to chat with our live chat team now? </speak>').reprompt('I did not get that. Would you like to initiate a chat now?')
	#.simple_card('Channel', speech)
  
#Customer FAQ
@ask.intent("faq")
def Faqtopic(faqtopic):
#delegate dialog to Alexa until all parameters are set
	dialog_state = get_dialog_state()
	print(dialog_state)
	if dialog_state != "COMPLETED":
		return delegate(speech=None)
	slotvalue = faqtopic
	print(slotvalue)
	list_1 = ['top up my phone', 'topup my phone', 'topup', 'top up', 'recharge', 'recharge my phone']
	list_2 = ['no signal', 'signal issues', 'low signal']
	list_3 = ['setup my phone for the internet', 'set up my phone for the internet', 'setup my phone to the internet', 'set up my phone for the internet']
	if slotvalue in list_1:
		return statement('There are various options for recharging your Prepaid Mobile or Mobile Broadband service. The My Optus app is the easiest way to top up or recharge. You can also store your credit card details to make your next recharge even easier. The My Optus app is available on Android and Apple smartphones. Recharge over the phone with a credit card by calling 555 from your Prepaid Mobile. Dont worry if you have run out of credit as calls to 555 are free. AutoRecharge is the simplest way to stay on top of your Prepaid plan. Just choose up the amount you want to recharge and the frequency of how often you would like the recharge to be applied. We will take care of the rest.')
	elif slotvalue in list_2:
		return statement('To check for a problem with the Optus Mobile Network & service in your area, see our coverage maps at www.optus.com.au/about/network/service-status.  Once you have selected the Outage tab and entered an address or location at the top of the map,  you will be presented with all the towers in the searched area. Red coloured tower or towers indicate there is a problem or outage, Orange coloured tower indicate we are performing maintenance or upgrades and Green coloured tower indicate that everything is running okay.')
	elif slotvalue in list_3:
		return statement('To set up, configure or troubleshoot your new device, check out our animated guides. They are all located at www.devicehelp.optus.com.au for selected devices and are are simple to follow online.')
	else:
		return statement('Kindly try our FAQ page at www.optus.com.au for answers to your queries')

#Yes Intent
@ask.intent('AMAZON.YesIntent')
def yes_intent():
	intent_name = session.attributes['intent_name']
	print(intent_name)
	if intent_name == "relocaterequest":
		#client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		#client.messages.create(from_='+14696467609', 
				       #to='+61421183854',
				       #body='Please click on this link http://yesopt.us/chat2us to initiate a livechat with our live chat team.')
		return statement('We have sent a SMS with the link to initiate a live chat to your mobile number. Please click on that link to chat with us')
	else:
		return statement('You can ask Alexa about your Optus account balance, data usage or for information about Optus services')

#No Intent
@ask.intent('AMAZON.NoIntent')
def no_intent():
	return statement('<speak> Please visit www.offer.optus.com.au/relocation# to submit your relocation request online or call us at <say-as interpret-as="telephone"> 1300555241 </say-as> to speak to our customer service team. </speak>')

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
def getbalance(accesstoken):
	balance = 'Thirteen dollars'
	accnumber = '34567654'
	duedate = '06/20/2018'
	return (balance, accnumber, duedate)

#Helper function for consumedpercent, datacap, remainingdata, effectivedate
def getusage(accesstoken):
	consumedpercent = '43%'
	datacap = '6 GB'
	remainingdata = '3.42 GB'
	effectivedate = '06/28/2018'
	return (consumedpercent, datacap, remainingdata, effectivedate)

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
