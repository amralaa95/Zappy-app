from django.conf.urls import url
from zappy.views import Events,getTweets

urlpatterns = [ 
    url(r'^$', Events.as_view()),
    url(r'^gettweets$',getTweets)  
]