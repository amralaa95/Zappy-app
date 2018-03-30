from django.shortcuts import render
from slackclient import SlackClient
import os
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from threading import Thread

SLACK_VERIFICATION_TOKEN = 'Nv9vArkIO0rYvmPUchCSKwvu'
slack_client = SlackClient('xoxb-338657963874-Va7Jc6jB4fRtaLq6cLfRzySV')

class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)

        if 'event' in slack_message:                              
            event_message = slack_message.get('event')            
            
            if event_message.get('subtype') == 'bot_message':     
                return Response(status=status.HTTP_200_OK)        
            
            user = event_message.get('user')                      
            text = event_message.get('text')                      
            channel = event_message.get('channel')                
            bot_text = 'Hi <@{}> :wave:'.format(user)             
            if 'go' in text.lower():                              
                slack_client.api_call(method='chat.postMessage',        
                                channel=channel,                  
                                text=bot_text)                    

                return Response(status=status.HTTP_200_OK)        

        return Response(status=status.HTTP_200_OK)
    
    def get(self,request,*args,**kwargs):
        return render(request,'base.html',{'form':'forrrrm'})
