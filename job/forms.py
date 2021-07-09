from django import forms

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=140)
    description= forms.CharField(max_length=500, widget=forms.Textarea)