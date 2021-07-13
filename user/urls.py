from django.urls import path
from user import views

app_name = "user"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
