from django import forms

from .models import Recipe

class RecipeForm(forms.Form):
    next_week = forms.BooleanField(required=False)
    this_week = forms.BooleanField(required=False)

    def clean_next_week(self):
    	data = self.cleaned_data['next_week']
    	return data

    def clean_this_week(self):
    	data = self.cleaned_data['this_week']
    	return data

    def __init__(self, *args, **kwargs):
    	super(RecipeForm, self).__init__(*args, **kwargs)
    	self.fields['this_week'].widget.attrs.update({'class': 'blue'})