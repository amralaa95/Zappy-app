from django.conf.urls import url
from zappy.views import Events

urlpatterns = [ 
    url(r'^$', Events.as_view()),  
]