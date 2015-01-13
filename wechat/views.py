# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

import hashlib
from xml.etree import ElementTree as etree

"""
wechat interface
"""
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
token = "jasonwang"
# Create your views here.
@csrf_exempt
def index(request):
	if request.method == 'GET':
		print request.GET
		signature = request.GET.get('signature','')
		timestamp = request.GET.get('timestamp','')
		nonce = request.GET.get('nonce','')
		echostr=request.GET.get('echostr','')
		
		hslst = [token,timestamp,nonce]
		hslst.sort()
		hstr = "%s%s%s"%tuple(hslst)
		hstr = hashlib.sha1(hstr).hexdigest()
		print hstr,signature
		if hstr==signature:
			return HttpResponse(echostr)
		else:
			return HttpResponse(None)
	elif request.method == 'POST':
		signature = request.GET.get('signature','')
		timestamp = request.GET.get('timestamp','')
		nonce = request.GET.get('nonce','')
		body_text = request.body
		print body_text
		wechat = WechatBasic(token=token)
		if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
			wechat.parse_data(body_text)
			message = wechat.get_message()
			if isinstance(message, TextMessage):
				response = wechat.response_text(content=u'文字信息')
			elif isinstance(message, VoiceMessage):
				response = wechat.response_text(content=u'语音信息')
			elif isinstance(message, ImageMessage):
				response = wechat.response_text(content=u'图片信息')
			elif isinstance(message, VideoMessage):
				response = wechat.response_text(content=u'视频信息')
			elif isinstance(message, LinkMessage):
				response = wechat.response_text(content=u'链接信息')
			elif isinstance(message, LocationMessage):
				response = wechat.response_text(content=u'地理位置信息')
			elif isinstance(message, EventMessage):  # 事件信息
				if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
					if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
						response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
					else:
						response = wechat.response_text(content=u'普通关注事件')
				elif message.type == 'unsubscribe':
					response = wechat.response_text(content=u'取消关注事件')
				elif message.type == 'scan':
					response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
				elif message.type == 'location':
					response = wechat.response_text(content=u'上报地理位置事件')
				elif message.type == 'click':
					if message.key == 'clicktesta':
						articles = [
							{
								'title':'testa1',
								'description':u'这是测试',
								'picurl':'http://a.hiphotos.baidu.com/image/w%3D310/sign=3f6b24fb84d6277fe912343918391f63/91529822720e0cf36fa0febb0946f21fbe09aa1f.jpg',
								'url':'www.baidu.com'
							},
							{
								'title':'testa1',
								'description':u'这是测试',
								'picurl':'http://a.hiphotos.baidu.com/image/w%3D310/sign=3f6b24fb84d6277fe912343918391f63/91529822720e0cf36fa0febb0946f21fbe09aa1f.jpg',
								'url':'www.baidu.com'
							}
						]
						response = wechat.response_news(articles)
					#response = wechat.response_text(content=u'自定义菜单点击事件')
				elif message.type == 'view':
					response = wechat.response_text(content=u'自定义菜单跳转链接事件')
		print response
		return HttpResponse(response)

def wc_create_menu(request):
	menu_dict = {
           'button':[
				{
					'name':u'客站资讯',
					'sub_button':[
                    	{
                    		'type':'view',
                            'name':u'客站介绍',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203349576&idx=1&sn=8ff27199f38b040273d9705802c52b44#rd'
                    	},
                    	{
                    		'type':'view',
                            'name':u'团队展示',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203349576&idx=1&sn=8ff27199f38b040273d9705802c52b44#rd'
                    	},
                    	{
                    		'type':'view',
                            'name':u'最新动态',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203429156&idx=1&sn=4104fe74654ac831400f8636f36f508a#rd'
                    	},
                    	{
                    		'type':'view',
                            'name':u'通知公告',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203429982&idx=1&sn=ba483cecf94e41786286c8ea22b991b4#rd'
                    	}
                    ]
				},
				{
					'name':u'服务中心',
					'sub_button':[
                        {
                            'type':'view',
                            'name':u'中心介绍',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203660894&idx=1&sn=80ead2fab876353a0444691b834b53c8#rd'
                        },
                        {
                            'type':'view',
                            'name':u'车次动态',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203660915&idx=1&sn=10b2a92885a30a9de89ea5bface55600#rd'
                        },
                        {
                            'type':'view',
                            'name':u'常用查询',
                            'url':'http://mp.weixin.qq.com/s?__biz=MzA3MjE5MDM3OQ==&mid=203661033&idx=1&sn=637b4e1997cca108fd7236c6ad402754#rd'
                        },
                        {
                            'type':'view',
                            'name':u'投诉建议',
                            'url':'http://115.28.107.224/EastStation/?m=home&c=Complaints'
                        }
                    ]
				},
				{
					'name':u'优惠互动',
					'sub_button':[
                        {
                            'type': 'view', 
                            'name': u'商户展示', 
                            'url': 'http://115.28.107.224/TeCollege/index.php?m=Wechat&a=index'
                        }, 
                        {
                            'type': 'view', 
                            'name': u'游戏互动', 
                            'url': 'http://115.28.107.224/TeCollege/index.php?m=ZhuanPan&a=ZhuanPan'
                        },
                        {
                        	'type': 'click',
                        	'name': 'clicktestA',
                        	'key':	'clicktesta'
                        },
                        {
                        	'type':'click',
                        	'name':'clicktestB',
                        	'key': 'clicktestb'
                        }
                    ]
				}
            ]}
	wechat = WechatBasic(appid='wx5d140785dfae330c', appsecret='7d665a6f144785c72d54ef280380e85e')
	print wechat.create_menu(menu_dict)
"""
 * * * * * * * * * * * * * * * * * * * * * * * * 
"""

"""
wechat manage
"""
def manageindex(request):
	return HttpResponse('manageindex')
"""
 * * * * * * * * * * * * * * * * * * * * * * * * 
"""

"""
wechat east station info
"""
def esinfoindex(request):
	return render_to_response("estation/stationinfo.html",RequestContext(request))

"""
 * * * * * * * * * * * * * * * * * * * * * * * * 
"""


"""
wechat 
"""
def esshops(request):
	pass
