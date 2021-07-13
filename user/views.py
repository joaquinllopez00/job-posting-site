from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from job.permissions import employee
from django.contrib import messages, auth
from user.models import *
from user.forms import *
from .forms import *


def login_view(request):
    """
    User ability to logIn

    """
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))

    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    """
    User ability to logout
    """
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('user:login')


def employee_registration(request):
    """
    Handle Employee Registration

    """
    form = EmployeeRegistration(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('user:login')

    return render(request,'user/employee.html',{'form':form})




@login_required
def profile_detail(request, username):
    user = User.objects.filter(username=username).first()
    listings = Listing.objects.filter(user=user)
    listings = listings.order_by('post_date').reverse()
    notifications = notification_count_view(request)
    context = {'user': user, 'listings': listings,
               'notifications': notifications}
    return render(request, 'profile.html', context)


@login_required
@employee
def employee_edit_profile(request, id=id):
    user = get_object_or_404(User, id=id)
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("edit_profile.html", kwargs={
            'id': form.id
        }))
    return render(request, 'edit_profile.html', {'form': form})


def employer_registration(request):
    form = EmployerRegistration(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('login')
    return render(request, 'user/employer.html', {'form': form})


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


@login_required
def notification_view(request):
    listings = Notification.objects.filter(mentioned=request.user)
    notification_count = 0
    notif_list = []
    for listing in listings:
        if listing.mark_as_read == False:
            notification_count += 1
            notif_list.append(listing.mention_listing)
            listing.mark_as_read = True
            listing.save()
    return render(request, 'notifications.html', {'mentions': notif_list, 'count': notification_count})


def notification_count_view(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(mentioned=request.user)
        notification_count = 0
        for notification in notifications:
            if notification.mark_as_read == False:
                notification_count += 1
    else:
        notification_count = 0
    return notification_count


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('job:home')

