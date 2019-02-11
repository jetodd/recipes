from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Recipe
from .forms import RecipeForm
import json

# Create your views here.
def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:5]
    tags_list = Tag.objects.all()
    this_week = Recipe.objects.filter(this_week=True)
    next_week = Recipe.objects.filter(next_week=True)

    queryset_list = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
    	queryset_list = queryset_list.filter(title__icontains=query)

    context = {'latest_recipes_list': latest_recipes_list, 'tags_list': tags_list, 'this_week': this_week, 'next_week': next_week, 
    'query': query, 'queryset_list': queryset_list}
    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
	recipe = Recipe.objects.get(id=recipe_id)
	ingredients  = json.loads(recipe.ingredients)
	steps = json.loads(recipe.steps)
	form = RecipeForm(request.POST)

	context = {'recipe': recipe, 'tags': recipe.tags.all(), 'ingredients': ingredients['ingredients'], 'steps': steps['steps'], 'form': form}
	
	if request.method == 'POST':
		if form.is_valid():
			# need to sanitize and set variables
			recipe.this_week = form.cleaned_data['this_week']
			recipe.next_week = form.cleaned_data["next_week"]
			recipe.save()
			return render(request, 'recipes/detail.html', context)
	
	return render(request, 'recipes/detail.html', context)

def tag(request, tag_id):
	tag = Tag.objects.get(id=tag_id)
	recipes = Recipe.objects.filter(tags__in=[tag_id])
	context = {'tag': tag, 'recipes': recipes}
	return render(request, 'recipes/tag.html', context)