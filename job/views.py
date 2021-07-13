from django.contrib.auth import decorators
from django.contrib import messages
from user.models import *
from job.forms import *
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from .permissions import *

decorators = [employee, employer, login_required]


# @login_required(login_url=reverse_lazy('account:login'))

@method_decorator(login_required, name='dispatch')
@method_decorator(employer, name="dispatch")
class create_listing_view(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        template_name = 'create_listing.html'
        form = CreateListingForm()
        context = {'form': form}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateListingForm(request.POST or None)
        user = get_object_or_404(User, id=request.user.id)
        categories = Category.objects.all()
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(
                    request, 'You have successfully posted your job! Please wait for review.')
                return redirect(reverse("create_listing.html", {'form': form,
                                                                'categories': categories}, kwargs={'id': instance.id}))
    # form = CreateListingForm()

    # if form.is_valid():
    #     data = form.cleaned_data
    #     company = request.user
    #     new_listing = Listing.objects.create(
    #         title=data['title'],
    #         description=data['description'],
    #         creator=company
    #     )
    #     new_listing_id = new_listing.id
    # return HttpResponseRedirect("/listing/%s/" % new_listing_id)


@method_decorator(login_required, name='dispatch')
class listing_detail_view(LoginRequiredMixin, DetailView):
    model = Listing
    template = 'listing.html'
    slug_field = "creator"

    def get(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']
        req_listing = Listing.objects.get(id=listing_id)
        print('listing', req_listing)
        template = 'job_detail.html'
        is_it_favorite = FavoriteJob.objects.filter(job=listing_id, user=request.user)
        return render(request, template, {'listing': req_listing, 'favorite': is_it_favorite})


@login_required
@employer
@employee
def job_list_view(request):
    job_list = Listing.objects.filter(
        is_published=True, is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing.html', {'page_obj': page_obj})


@login_required
@employer
@employee
def single_job_view(request, id):
    job = get_object_or_404(Listing, id=id)
    related_job_list = job.tags.similar_objects()
    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'job_detail.html', {'job': job,
                                               'page_obj': page_obj,
                                               'total': len(related_job_list)})


@login_required
@employer
@employee
def search_result_view(request):
    job_list = Listing.objects.order_by('-timestamp')
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing.html', {'page_obj': page_obj})


# @login_required(login_url=reverse_lazy('account:login'))
# @employee
@login_required
@employee
def apply_job_view(request, id):
    form = ApplyForm(request.POST or None)
    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)
    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("job_detail.html", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("job_detail.html", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already applied for the Job!')
        return redirect(reverse("job_detail.html", kwargs={
            'id': id
        }))


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
def dashboard_view(request):
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':
        jobs = Listing.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count
    if request.user.role == 'employee':
        savedjobs = FaveForm.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {
        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs': appliedjobs,
        'total_applicants': total_applicants
    }
    return render(request, 'dashboard', context)


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employer
def delete_job_view(request, id):
    job = get_object_or_404(Listing, id=id, user=request.user.id)
    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')
    return redirect('dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Listing, id=id, user=request.user.id)
    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong!')
    return redirect('dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employer
def all_applicants_view(request, id):
    all_applicants = Applicant.objects.filter(job=id)
    context = {

        'all_applicants': all_applicants
    }
    return render(request, 'profile.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(FaveForm, id=id, user=request.user.id)
    if job:
        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employer
def applicant_details_view(request, id):
    applicant = get_object_or_404(User, id=id)
    return render(request, 'profile.html', {'applicant': applicant})


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employee
def job_fave_view(request, id):
    form = FaveForm(request.POST or None)
    user = get_object_or_404(User, id=request.user.id)
    applicant = FavoriteJob.objects.filter(user=request.user.id, job=id)
    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("job_detail.html", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("job_detail.html", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("job_detail.html", kwargs={
            'id': id
        }))


# @login_required(login_url=reverse_lazy('account:login'))
@login_required
@employer
def job_edit_view(request, id=id):
    job = get_object_or_404(Listing, id=id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Your Job Post was successfully updated!')
        return redirect(reverse("job_detail.html", kwargs={
            'id': instance.id
        }))
    return render(request, 'job_edit.html', {'form': form,
                                             'categories': categories})

@login_required
@employee
def favorite(request, listing_id):
    is_it_favorite = FavoriteJob.objects.filter(job=listing_id, user=request.user)

    if not is_it_favorite:
        listing = Listing.objects.get(id=listing_id)
        FavoriteJob.objects.create(
            user=request.user,
            job=listing,
        )
        return HttpResponseRedirect(f'/listing/{listing_id}')
    
    else:
        is_it_favorite.delete()
        return HttpResponseRedirect(f'/listing/{listing_id}')