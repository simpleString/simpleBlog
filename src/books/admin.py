from django.contrib import admin
from .models import *


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Tag)
