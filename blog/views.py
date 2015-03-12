from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from blog.models import Article
import os
import json
# Create your views here.

def handle_uploaded_file(f):
	print "in handle_uploaded_file"
	fpath = os.getcwd()+'/blog/upload/name.jpg'
	print fpath
	with open(fpath,'wb+') as destination:
		print f
		for chunk in f.chunks():
			destination.write(chunk)

def index(request):
	blogs = Article.objects.all()

	return render_to_response("blog/blogpost.html",{"blogs":blogs},RequestContext(request))
def blogitem(request):
	pass

###  Manage ####
def manage(request):
	
	return render_to_response("blog/manage.html",RequestContext(request));

def upload(request):
	print request.method
	if request.method == 'POST':
		print request.FILES['upload_file']
		
		handle_uploaded_file(request.FILES['upload_file'])
		ret = {
			"success":"true",
			"file_path":"/blog/upload/name.jpg"
		}
		print "upload success"
		return HttpResponse(json.dumps(ret));
	print 'error'
	return HttpResponse("error")
