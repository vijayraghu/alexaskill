# -*- coding: utf-8 -*-
import os
import sys
import urllib
import requests
import json
from flask import Flask, request, Response, make_response, jsonify, url_for
# Twilio Helper Library
from twilio.rest import Client

# Declare global variables
apiai_client_access_key = os.environ["APIAPI_CLIENT_ACCESS_KEY"]
apiai_url = "https://api.api.ai/v1/query"
apiai_querystring = {"v": "20150910"}

app = Flask(__name__)

@app.route('/start', methods=['GET','POST'])
def start():
	caller_phone_number = request.values.get('From')
	print (caller_phone_number)
	user_id = request.values.get('From')
	input_text = request.values.get('Body')
	apiai_language = 'en'
	
	#Sending and getting response from Dialogflow
	headers = {'authorization': 'Bearer ' + apiai_client_access_key, 
			   'content-type': 'application/json'
			  }
	payload = {'query': input_text , 
			   'lang': apiai_language, 
			   'sessionId': user_id
			  }
	response = requests.request("POST", url=apiai_url, data=json.dumps(payload), headers=headers, params=apiai_querystring)
	print (response.text)
	output = json.loads(response.text)
	output_text = output['result']['fulfillment']['speech']
	#output_text = output_text.decode('utf-8')
				
	# Send whatsapp with dialogflow response
	client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	client.messages.create(body=output_text, 
			       from_='whatsapp:+14155238886', 
			       to=caller_phone_number
			      )					  
	return str(response)
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print ('Starting app on port %d' % port)
	app.run(debug=False, port=port, host='0.0.0.0')
