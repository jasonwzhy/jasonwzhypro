from django.conf.urls import patterns, include, url
from wechat import views
urlpatterns = patterns('',
	url(r'^$',views.index),
)