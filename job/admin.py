from django.contrib import admin
from .models import *


admin.site.register(Category)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
    
admin.site.register(Applicant,ApplicantAdmin)


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Listing,ListingAdmin)

class FavoriteJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
admin.site.register(FavoriteJob,FavoriteJobAdmin)

