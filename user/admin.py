from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Listing, User


admin.site.register(User, UserAdmin)
admin.site.register(Listing)
