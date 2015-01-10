# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as etree

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
				response = wechat.response_text(content=u'自定义菜单点击事件')
			elif message.type == 'view':
				response = wechat.response_text(content=u'自定义菜单跳转链接事件')

		print response
		return HttpResponse(response)
def manageindex(request):
	return HttpResponse('manageindex')