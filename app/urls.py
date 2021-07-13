from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import (handler404, handler500)
# from django.views.generic import TemplateView

# handler404 = user_views.handler404
# handler500 = user_views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job.urls')),
    path('', include('user.urls')),

]
