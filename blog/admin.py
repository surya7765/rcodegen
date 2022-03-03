from django.contrib import admin
from .models import Post

# Register your models here.

admin.site.site_header = "Random Question Generator Admin"
admin.site.site_title = "Random Question Generator Admin Area"
admin.site.index_title = "Welcome to the Random Question Generator admin area"


admin.site.register(Post)
