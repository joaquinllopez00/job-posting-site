from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib.auth import authenticate, login


class LoginView(TemplateView):
    '''Login Form for testing BaseUser concept'''

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
