from django.contrib import admin
from .models import Blogs, Comment

admin.site.header = "Legit Edu Consults"
admin.site.register(Blogs)
admin.site.register(Comment)
