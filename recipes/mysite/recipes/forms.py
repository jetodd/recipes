from django import forms

from .models import Recipe, ShoppingItem

class RecipeForm(forms.ModelForm):
    class Meta:
    	model = Recipe
    	fields = ('this_week', 'next_week')

    def __init__(self, *args, **kwargs):
    	super(RecipeForm, self).__init__(*args, **kwargs)
    
    def clean_this_week(self):
    	data = self.cleaned_data['this_week']
    	return data

    def clean_next_week(self):
    	data = self.cleaned_data['next_week']
    	return data

class ShoppingForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(ShoppingForm, self).__init__(*args, **kwargs)