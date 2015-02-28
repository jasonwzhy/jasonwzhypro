from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from blog.models import Article
# Create your views here.

def index(request):
	blogs = Article.objects.all()

	return render_to_response("blog/blogpost.html",{"blogs":blogs},RequestContext(request))
def blogitem(request):
	

###  Manage ####
def manage(request):
	
	return render_to_response();

