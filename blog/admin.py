from django.contrib import admin
from blog.models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('author','title','createdate','content')
admin.site.register(Article,ArticleAdmin)