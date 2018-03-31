import sys
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from zappy.models import Tweet

TWITTER_CONSUMER_KEY = 'DAJxuF8xaRVkx48CaZLIK65Zh'
TWITTER_CONSUMER_SECRET = '6h3bCLNPkusVCyF4WhRPBMfxQJoYEvaOuyd7Lj6AsIQG6Zbi6x'
TWITTER_ACCESS_TOKEN = '979516170255642626-mJcvmpmI0nxR1oZD2amfKIXAit9HV5j'
TWITTER_ACCESS_SECRET = 'AwzXXO91l1oEWcP4hHrmRMML9F1o7jLYR0iXik2jXY95G'
auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

class tweetListener(StreamListener):
    def on_connect(self):
        print "connect"
    def on_status(self,data):
        newTweet = Tweet(tweet_id = data.id,tweet_text=data.text,tweet_time = data.created_at,tweet_user = data.author.screen_name,tweet_location = data.author.location)
        newTweet.save()
        return 
    def on_error(self,error):
        print error
    # def on_delete(self, status_id, user_id):
    #     print status_id
    #     print user_id
        return

twitter_stream = Stream(api.auth,tweetListener())
twitter_stream.userstream()
twitter_stream.filter(track=sys.argv[1:])


