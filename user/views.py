from job.permissions import employee
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from user.models import *
from user.forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse


@login_required
def dashboard(request):
    published_jobs = Listing.objects.filter(
        is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        job_lists = []
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': next_page_number,
            'no_of_page': paginator.num_pages,
            'prev_page_number': prev_page_number
        }
        return JsonResponse(data)

    context = {

        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'total_completed_jobs': len(published_jobs.filter(is_closed=True)),
        'page_obj': page_obj
    }
    print('Success')
    return render(request, 'dashboard.html', context)


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


def employee_registration(request):
    form = EmployeeRegistration(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('login')
    return render(request, 'employee.html', {'form': form})

# (login_url=reverse_lazy('accounts:login'))


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
    return render(request, 'employer.html', {'form': form})


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
