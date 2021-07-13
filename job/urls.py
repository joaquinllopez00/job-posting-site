from django.urls import path
from job import views

app_name = "job"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_view, name='job-list'),
    path('job/create/', views.create_listing_view, name='create_listing'),
    path('job/<int:id>/', views.single_job_view, name='job_detail'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('favorite-job/<int:id>/', views.job_fave_view, name='favorite-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-favorite/<int:id>/', views.delete_favorite_view, name='delete-favorite'),


]
