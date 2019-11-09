from django.contrib import admin
from .models import User
from .models import Issue
from .models import Update

# Register your models here.
admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Update)