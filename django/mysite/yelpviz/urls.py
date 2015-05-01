from django.conf.urls import patterns, url

from yelpviz import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^bsearch$', views.bsearch, name='bsearch'),
    url(r'^csearch$', views.csearch, name='csearch'),
)
