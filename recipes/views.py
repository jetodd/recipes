import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

from .forms import RecipeForm, ShoppingForm
from .models import Tag, Recipe, ShoppingItem


# Create your views here.
def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:3]
    this_week = Recipe.objects.filter(this_week=True)
    next_week = Recipe.objects.filter(next_week=True)
    most_popular_recipes_list = Recipe.objects.all().filter(cooked_count__gt=0).order_by('-cooked_count')[:3]
    shopping = ShoppingItem.objects.filter(recipe__isnull=False)

    queryset_list = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

    context = {'latest_recipes_list': latest_recipes_list, 'this_week': this_week,
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
    shopping = ShoppingItem.objects.filter(recipe=recipe)
    ingredients = json.loads(recipe.ingredients)
    steps = json.loads(recipe.steps)
    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        recipe.cooked_count += 1
        recipe.this_week = False
        recipe.save()
        if (shopping):
            for item in shopping:
                item.delete()
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

def generate(request):
    recipes = Recipe.objects.filter(next_week=True)
    shopping = ShoppingItem.objects.all()

    if request.method == 'POST':
        for recipe in recipes:
            ingredients = json.loads(recipe.ingredients)
            print(ingredients)
            for ingredient in ingredients['ingredients']:
                item = ShoppingItem(name=ingredient, recipe=recipe)
                item.save()

        return HttpResponseRedirect('/recipes')

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

class RecipesView(ListView):
    model = Recipe
    paginate_by = 6
    context_object_name = 'recipes'
    template_name = 'recipes/all.html'

def all(request):
    recipes_list = Recipe.objects.all().order_by('-pub_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(recipes_list, 12)

    tags = Tag.objects.all()

    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    return render(request, 'recipes/all.html', {'recipes': recipes, 'tags': tags})

def search(request):
    queryset_list = Recipe.objects.all()
    tags_list = Tag.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)
        tags_list = tags_list.filter(name__icontains=query)
    if queryset_list.count() == 1 and tags_list.count() == 0:
        return HttpResponseRedirect('/recipes/' + str(queryset_list[0].id) + "/detail")
    
    context = {'queryset_list': queryset_list, 'tags_list': tags_list,'query': query}
    return render(request, 'recipes/search.html', context)