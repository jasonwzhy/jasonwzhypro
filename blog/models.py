from django.db import models
from django.contrib.auth.models import User
class Article(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=128)
	createdate = models.DateTimeField()
	content = models.TextField()
# Create your models here.
