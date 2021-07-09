from django.shortcuts import render,HttpResponse, HttpResponseRedirect, reverse
from django.views.generic import View
import uuid

from job.forms import CreateListingForm
from job.models import Listing


class create_listing_view(View):
    
    def get(self, request):
        user = self.request.user
        print(user)
        template_name = 'create_listing.html'
        form = CreateListingForm()
        context = {'form': form}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateListingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            company = request.user
            new_listing = Listing.objects.create(
                title = data['title'],
                description = data['description'],
                creator = company
            )
            new_listing_id = new_listing.id
        return HttpResponseRedirect("/listing/%s/" % new_listing_id)

    # title = models.CharField(max_length=140)
    # description = models.TextField(max_length=500)
    # date_posted = models.DateTimeField(default=timezone.now)
    # creator = models.ForeignKey("user.User", on_delete=models.CASCADE)
    # applicants = models.ManyToManyField("user.User", symmetrical=False, related_name="applicants")

class listing_detail_view(View):
    def get(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']
        req_listing = Listing.objects.get(id=listing_id)
        print('listing', req_listing)
        template = 'listing.html'
        context = {'listing': req_listing}
        return render(request, template, context)