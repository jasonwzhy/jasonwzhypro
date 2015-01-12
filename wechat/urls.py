from django.conf.urls import patterns, include, url
from wechat import views
urlpatterns = patterns('',
	url(r'^$',views.index),
	url(r'^manage/$',views.manageindex),
	url(r'^manage/createmenu/',views.wc_create_menu),
	url(r'^estationinfo/$',views.esinfoindex),
)