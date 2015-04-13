from django.conf.urls import patterns, url

from yelpviz import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^testquery$', views.index, name='index'),
)
