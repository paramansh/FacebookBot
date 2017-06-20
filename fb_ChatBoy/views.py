# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
import requests
from pprint import pprint
# Create your views here.
# yomamabot/fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class fbc(generic.View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '12345':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            print(entry )
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
		    if 'text' in message['message']:
		   	 post_facebook_message(message['sender']['id'], message['message']['text'])
		    else:
			 post_facebook_message(message['sender']['id'], 'Text and Emojis Only')
        return HttpResponse()


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAbG7rZA4wkEBADfFkWHkGt2pAXuokz8ZAZAfEJiRXkE1637R3o3SZAECJDWld3AsREJZBgERkvjU0if6SHKZAvgZCGi7EcoF2uvCjiDLFGikg21kYCAvNd1UDlnjHBCP23QhO1Q5iGQmejyNRxZAXomNzHDtlHmcgdfjVSsG3WaRz5aNwJsyKg2'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
