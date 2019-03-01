import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import RecipeForm, ShoppingForm
from .models import Tag, Recipe, ShoppingItem


# Create your views here.
def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:5]
    tags_list = Tag.objects.all()
    this_week = Recipe.objects.filter(this_week=True)
    next_week = Recipe.objects.filter(next_week=True)
    most_popular_recipes_list = Recipe.objects.all().filter(cooked_count__gt=0).order_by('-cooked_count')[:5]
    shopping = ShoppingItem.objects.filter(recipe__isnull=False)

    queryset_list = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

    context = {'latest_recipes_list': latest_recipes_list, 'tags_list': tags_list, 'this_week': this_week,
               'next_week': next_week, 'shopping': shopping,
               'query': query, 'queryset_list': queryset_list, 'most_popular_recipes_list': most_popular_recipes_list}
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = json.loads(recipe.ingredients)
    steps = json.loads(recipe.steps)
    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe.save()
            return HttpResponseRedirect('/recipes')

    context = {'recipe': recipe, 'tags': recipe.tags.all(), 'ingredients': ingredients['ingredients'],
               'steps': steps['steps'], 'form': form}
    return render(request, 'recipes/detail.html', context)


def cooked(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = json.loads(recipe.ingredients)
    steps = json.loads(recipe.steps)
    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        recipe.cooked_count += 1
        recipe.this_week = False
        recipe.save()
        return HttpResponseRedirect('/recipes')

def shopping(request):
    shopping = ShoppingItem.objects.all()
    form = ShoppingForm()
    context = {'items': shopping, 'form': form}

    if request.method == 'POST':
        if form.is_valid:
            post = form.save(commit=False)
            post.name = request.POST['name']
            if request.POST['recipe']:
                post.recipe = get_object_or_404(Recipe, id=request.POST['recipe'])

            post.save()

    return render(request, 'recipes/shopping.html', context)


def move(request):
    recipes = Recipe.objects.filter(next_week=True)

    if request.method == 'POST':
        for recipe in recipes:
            recipe.this_week = True
            recipe.next_week = False
            recipe.save()
        return HttpResponseRedirect('/recipes')

def deleteshopping(request):
    shopping = ShoppingItem.objects.all()

    if request.method == 'POST':
        for item in shopping:
            item.delete()
        return HttpResponseRedirect('/recipes/shopping')

def deleteitems(request):
    if request.method == 'POST':
        for item in request.POST.getlist('item'):
            delete_item = ShoppingItem.objects.filter(name=item)
            delete_item[0].delete()
        return HttpResponseRedirect('/recipes/shopping')


def tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    recipes = Recipe.objects.filter(tags__in=[tag_id]).order_by('-cooked_count')
    context = {'tag': tag, 'recipes': recipes}
    return render(request, 'recipes/tag.html', context)


def all(request):
    recipes = Recipe.objects.all().order_by('-cooked_count')
    context = {'recipes': recipes}
    return render(request, 'recipes/all.html', context)
