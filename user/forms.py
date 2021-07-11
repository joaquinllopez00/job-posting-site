from django import forms
from user.models import User, Listing
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'bio', 'email', 'date_joined', 'is_active', 'role']


class JobForm(forms.ModelForm):
    listing = forms.CharField(widget=forms.Textarea, max_length=140)

    class Meta:
        model = Listing
        fields = "__all__"


class EmployeeRegistration(UserCreationForm):

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['name'].required = True
        self.fields['name'].label = "Full Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'name', 'email',
                  'password1', 'password2']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistration(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['name'].required = True
        self.fields['name'].label = "Company Name and Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name and Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['name',
                  'email', 'password1', 'password2', ]

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )

    class Meta:
        model = User
        fields = ["name"]
