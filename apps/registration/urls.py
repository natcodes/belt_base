from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
url(r'^$', views.index),   # This line has changed!
url(r'^login$', views.login),
#url after the '/', views.py, def login() method
url(r'^registration$', views.registration),
url(r'^success$', views.success),
url(r'^create$', views.create),
url(r'^quotes/addfav/(?P<id>\d+)$', views.addfav),
# /the addfav method within quotes, pertaining to the id, views file add fav method in views. 
url(r'^quotes/unfav/(?P<id>\d+)$', views.unfav),
url(r'^pages/(?P<id>\d+)$', views.pages)
]