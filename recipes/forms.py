from django import forms
from django.db.models import Q

from .models import Recipe, ShoppingItem, NextWeekItem, ThisWeekItem, ThisWeekMealItem, NextWeekMealItem


class ThisWeekForm(forms.ModelForm):
    class Meta:
        model = ThisWeekMealItem
        fields = ['this_week']


class NextWeekForm(forms.ModelForm):
    class Meta:
        model = NextWeekMealItem
        fields = ['next_week']


class ShoppingForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ('name', 'recipe')

    def __init__(self, *args, **kwargs):
        super(ShoppingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipe'].widget.attrs.update({'class': 'form-control'})

        available_recipe = Q(this_week__isnull=False) | Q(next_week__isnull=False)

        self.fields['recipe'].queryset = Recipe.objects.filter(available_recipe)
