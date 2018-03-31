from django.shortcuts import render
from slackclient import SlackClient
import os
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from zappy.models import Tweet
import json
from django.http import HttpResponse

SLACK_VERIFICATION_TOKEN = 'Nv9vArkIO0rYvmPUchCSKwvu'
SLACK_BOOT_TOKEN = 'xoxb-338657963874-CsYtuicEYhuapNvLVCl9iV2E'
TWITTER_CONSUMER_KEY = 'DAJxuF8xaRVkx48CaZLIK65Zh'
TWITTER_CONSUMER_SECRET = '6h3bCLNPkusVCyF4WhRPBMfxQJoYEvaOuyd7Lj6AsIQG6Zbi6x'
TWITTER_ACCESS_TOKEN = '979516170255642626-mJcvmpmI0nxR1oZD2amfKIXAit9HV5j'
TWITTER_ACCESS_SECRET = 'AwzXXO91l1oEWcP4hHrmRMML9F1o7jLYR0iXik2jXY95G'

slack_client = SlackClient(SLACK_BOOT_TOKEN)
auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)


class Events(APIView):
    # twitter_stream = None
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        
        # if not Events.twitter_stream:
        #     Events.twitter_stream = Stream(api.auth,tweetListener())
        #     Events.twitter_stream.userstream()
        #     Events.twitter_stream.filter(track=sys.argv[1:])
        
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
            bot_text = 'Hi <@{}> Zappy get new Tweets'.format(user)             
            if 'go' in text.lower():
                        
                slack_client.api_call(method='chat.postMessage',        
                                channel=channel,                  
                                text=bot_text)                    
                
                tweets = tweepy.Cursor(api.home_timeline).items()
                for tweet in tweets:
                    newTweet = Tweet.objects(tweet_id = tweet.id)
                    if not newTweet:
                        newTweet = Tweet(tweet_id = tweet.id,tweet_text=tweet.text,tweet_time = tweet.created_at,tweet_user = tweet.author.screen_name,tweet_location = tweet.author.location)
                        newTweet.save()
                    else:
                        break
               
                return Response(status=status.HTTP_200_OK)        

        return Response(status=status.HTTP_200_OK)
    
    def get(self,request,*args,**kwargs):       
       return render(request,'base.html',{})


def getTweets(request):
    tweets_res = []
    tweets = Tweet.objects()
    for tweet in tweets:
        tweets_res.append({"text":tweet.tweet_text,"time":str(tweet.tweet_time)})

    return HttpResponse(json.dumps(tweets_res))