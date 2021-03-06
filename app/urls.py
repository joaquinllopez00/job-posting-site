"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user_views
from job import views
from django.conf.urls import (handler404, handler500)


handler404 = user_views.handler404
handler500 = user_views.handler500

urlpatterns = [
    path('login/', user_views.login_view, name='loginview'),
    path('logout/', user_views.logout_view, name='logoutview'),
    path('register/employee/', user_views.employee_registration,
         name='employee-registration'),
    path('register/employer/', user_views.employer_registration,
         name='employer-registration'),
    path('profile/edit/<int:id>/',
         user_views.employee_edit_profile, name='edit-profile'),
    path('', user_views.dashboard, name='dashboard'),
    path('notifications/', user_views.notification_view, name="notifications"),
    path('create/', views.create_listing_view.as_view(),
         name='createlisting'),
    path('listing/<int:listing_id>/',
         views.listing_detail_view.as_view(), name='listingdetail'),
    path('favorite/<int:listing_id>/', views.favorite, name='favoriteListing'),
    path('profile/<str:username>/', user_views.profile_detail, name='userprofile'),
    path('admin/', admin.site.urls),
]
