from django.template import RequestContext
from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import LoginForm, RegisterForm
from user.models import User, Listing, Notification
from user.forms import UserCreationForm, JobForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
import re


# @login_required
def dashboard(request):
    listings = Listing.objects.all()
    return render(request, 'dashboard.html', {'listings': listings})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                'username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('dashboard')))

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('dashboard'))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'], name=data['name'],
                                                role=data['role'],)
            return HttpResponseRedirect(reverse('dashboard'))

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


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


def profile_detail(request, username):
    user = User.objects.filter(username=username).first()
    listings = Listing.objects.filter(creator=user).order_by('-date_posted')
    notifications = notification_count_view(request)
    # new_user = User.objects.create_user(email=data['email'], date_joined=data['date_joined'], role=data['role],)
    return render(request, 'profile.html', {'user': user, 'listings': listings, 'notifications': notifications})
