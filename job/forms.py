from django import forms
from .models import *


class CreateListingForm(forms.ModelForm):
    title = forms.CharField(max_length=140)
    description = forms.CharField(max_length=500, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['post_date'].label = " Job Post Date :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['tags'].label = "Tags :"
        self.fields['url'].label = "Website :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Des Moines, Iowa',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$1500 - $2200',
            }
        )
        self.fields['post_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',

            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: Python, JavaScript ',
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )
        

    class Meta:
        model = Listing

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "post_date",
            "company_name",
            "company_description",
            "tags",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(CreateListingForm, self).save(commit=False)
        if commit:
            User.save()
        return job


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']


class FaveForm(forms.ModelForm):
    class Meta:
        model = FavoriteJob
        fields = ['job']


class JobEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['post_date'].label = "Job Post Date :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Full Stack Software Engineer',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : ',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$40,000 - $80,000',
            }
        )
        self.fields['post_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )

    class Meta:
        model = Listing

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "post_date",
            "company_name",
            "company_description",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            User.save()
        return job
