from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeUser, EmployerUser


admin.site.register(EmployeeUser, UserAdmin)
admin.site.register(EmployerUser, UserAdmin)
