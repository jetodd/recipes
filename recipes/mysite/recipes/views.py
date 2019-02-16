from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tag, Recipe
from django.http import HttpResponseRedirect
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
	recipe = get_object_or_404(Recipe, id=recipe_id)
	ingredients  = json.loads(recipe.ingredients)
	steps = json.loads(recipe.steps)
	form = RecipeForm(instance=recipe)

	if request.method == 'POST':
		form = RecipeForm(request.POST, instance=recipe)
		if form.is_valid():
			recipe.save()
			return HttpResponseRedirect('/recipes')
	
	context = {'recipe': recipe, 'tags': recipe.tags.all(), 'ingredients': ingredients['ingredients'], 'steps': steps['steps'], 'form': form}
	return render(request, 'recipes/detail.html', context)

def cooked(request, recipe_id):
	recipe = get_object_or_404(Recipe, id=recipe_id)
	ingredients = json.loads(recipe.ingredients)
	steps = json.loads(recipe.steps)
	form = RecipeForm(instance=recipe)

	if request.method == 'POST':
		print('save')
		recipe.cooked_count += 1
		recipe.this_week = False
		recipe.save()
		return HttpResponseRedirect('/recipes')

def move(request):
	recipes = Recipe.objects.filter(next_week=True)

	if request.method == 'POST':
		for recipe in recipes:
			print (recipe)
			recipe.this_week = True
			recipe.next_week = False
			recipe.save()
		return HttpResponseRedirect('/recipes')


def tag(request, tag_id):
	tag = Tag.objects.get(id=tag_id)
	recipes = Recipe.objects.filter(tags__in=[tag_id])
	context = {'tag': tag, 'recipes': recipes}
	return render(request, 'recipes/tag.html', context)

def all(request):
	recipes = Recipe.objects.all()
	context = {'recipes': recipes}
	return render(request, 'recipes/all.html', context)
