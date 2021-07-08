from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import LoginForm, RegisterForm
from user.models import User
from user.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


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
    return HttpResponseRedirect(reverse('homepage'))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                'username'), password=data.get('password'), name=data.get('name'), bio=data.get('bio'), date_joined=data.get('date_joined'), email=data.get('email'), role=data.get('role'))
            login(request, new_user)
            return HttpResponseRedirect(reverse('dashboard'))

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    # user = listing.objects.filter(user=request.user)
    # following = listing.objects.filter(user__in=request.user.following.all())
    # notifications = views.notification_count_view(request)
    # feed = user | following
    # feed = feed.order_by('-time')
    # return render(request, 'dashboard.html', {'feed': feed, 'notifications': notifications})
    return render(request, 'dashboard.html')

