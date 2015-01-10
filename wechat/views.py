from django.shortcuts import render
from django.http import HttpResponse
import hashlib
# Create your views here.
def ifsverify(request):
	if request.method == 'GET':
		signature = request.GET.get('signature','')
		timestamp = request.GET.get('timestamp','')
		nonce = request.GET.get('nonce','')
		echostr=request.GET.get('echostr','')
		token="jasonwang"
		hslst = [token,timestamp,nonce]
		hslst.sort()
		hstr = "%s%s%s"%tuple(hslst)
		hstr = hashlib.sha1(hstr).hexdigest()
		print hstr,signature
		if hstr==signature:
			return HttpResponse(echostr)
			#return True
		else:
			#return HttpResponse(None)
			return False
def index(request):
	return HttpResponse('hello wechat')
def manageindex(request):
	return HttpResponse('manageindex')