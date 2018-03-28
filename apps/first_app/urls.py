from django.conf.urls import url
from . import views          
  
urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.register),   
    url(r'^process_login$', views.login),
    url(r'^quotelist$', views.quotelist),
    url(r'^contribute$', views.contribute),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^user_quotes/(?P<quote_id>\d+)$', views.user_quotes),
    url(r'^add_quotelist/(?P<quote_id>\d+)$', views.add_quotelist)
]

