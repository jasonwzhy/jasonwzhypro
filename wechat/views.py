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
		print request.body,'\n'
		signature = request.GET.get('signature','')
		timestamp = request.GET.get('timestamp','')
		nonce = request.GET.get('nonce','')
		body_text = request.body
		
		wechat = WechatBasic(token=token)
		if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
			wechat.parse_data(body_text)
			message = wechat.get_message()
			print '\n',message.type,'\n'
			if isinstance(message, TextMessage):
				print 'in if !'
				response = wechat.response_text(content=u'文字信息')
				print response
		print response
		return HttpResponse(response)
def manageindex(request):
	return HttpResponse('manageindex')