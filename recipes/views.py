import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

from .forms import ShoppingForm, ThisWeekForm, NextWeekForm
from .models import Tag, Recipe, ShoppingItem, ThisWeekItem, NextWeekItem, ThisWeekMealItem, NextWeekMealItem


# Create your views here.
def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:3]
    this_week = ThisWeekItem.objects.all().order_by('position')
    next_week = NextWeekItem.objects.all().order_by('position')
    most_popular_recipes_list = Recipe.objects.all().filter(cooked_count__gt=0).order_by('-cooked_count')[:3]
    shopping_list = ShoppingItem.objects.filter(recipe__isnull=False)

    queryset_list = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

    context = {'latest_recipes_list': latest_recipes_list, 'shopping': shopping_list, 'this_week': this_week,
               'next_week': next_week,
               'query': query, 'queryset_list': queryset_list, 'most_popular_recipes_list': most_popular_recipes_list}
    return render(request, 'recipes/index.html', context)


def random(request):
    recipe = Recipe.objects.order_by('?').first()

    return detail(request, recipe.id)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = json.loads(recipe.ingredients)
    steps = json.loads(recipe.steps)

    context = {'recipe': recipe, 'tags': recipe.tags.all(), 'ingredients': ingredients['ingredients'],
               'steps': steps['steps']}

    this_week_items = ThisWeekItem.objects.filter(recipe_id=recipe.id)
    this_week_item = this_week_items[0] if len(this_week_items) == 1 else None

    next_week_items = NextWeekItem.objects.filter(recipe_id=recipe.id)
    next_week_item = next_week_items[0] if len(next_week_items) == 1 else None

    if request.method == 'POST':
        this_week_form = context['this_week'] = ThisWeekForm(request.POST)
        next_week_form = context['next_week'] = NextWeekForm(request.POST)

        if this_week_form.is_valid() and next_week_form.is_valid():
            if this_week_item is None and this_week_form.cleaned_data['this_week']:
                this_week_item = ThisWeekItem(recipe_id=recipe.id)
                this_week_item.save()
            elif this_week_item is not None and not this_week_form.cleaned_data['this_week']:
                this_week_item.delete()
            if next_week_item is None and next_week_form.cleaned_data['next_week']:
                next_week_item = NextWeekItem(recipe_id=recipe.id)
                next_week_item.save()
            elif next_week_item is not None and not next_week_form.cleaned_data['next_week']:
                next_week_item.delete()
        return HttpResponseRedirect('/recipes')
    else:
        this_week = ThisWeekMealItem(this_week=this_week_item is not None)
        next_week = NextWeekMealItem(next_week=next_week_item is not None)

        context['this_week'] = ThisWeekForm(instance=this_week)
        context['next_week'] = NextWeekForm(instance=next_week)

    return render(request, 'recipes/detail.html', context)


def cooked(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    shopping_list = ShoppingItem.objects.filter(recipe=recipe)

    if request.method == 'POST':
        recipe.cooked_count += 1
        recipe.save()
        ThisWeekItem.objects.get(recipe_id=recipe_id).delete()
        if shopping_list:
            for item in shopping_list:
                item.delete()
        return HttpResponseRedirect('/recipes')


def shopping(request):
    shopping_list = ShoppingItem.objects.all()
    form = ShoppingForm()
    context = {'items': shopping_list, 'form': form}

    if request.method == 'POST':
        if form.is_valid:
            post = form.save(commit=False)
            post.name = request.POST['name']
            if request.POST['recipe']:
                post.recipe = get_object_or_404(Recipe, id=request.POST['recipe'])

            post.save()

    return render(request, 'recipes/shopping.html', context)


def move(request):
    recipes = Recipe.objects.filter(next_week__isnull=False)

    if request.method == 'POST':
        for recipe in recipes:
            this_week_items = ThisWeekItem.objects.filter(recipe_id=recipe.id)

            if len(this_week_items) == 0:
                this_week_item = ThisWeekItem(recipe_id=recipe.id)
                this_week_item.save()
            NextWeekItem.objects.get(recipe_id=recipe.id).delete()
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

    context = {'queryset_list': queryset_list, 'tags_list': tags_list, 'query': query}
    return render(request, 'recipes/search.html', context)


def save_this_week_position(request):
    ordered_ids = get_recipe_ids_for_position(request)

    current_order = 1
    for position in ordered_ids:
        item = ThisWeekItem.objects.get(recipe_id=position)
        item.position = current_order
        item.save()
        current_order += 1

    return HttpResponseRedirect('/recipes')


def save_next_week_position(request):
    ordered_ids = get_recipe_ids_for_position(request)

    current_order = 1
    for position in ordered_ids:
        item = NextWeekItem.objects.get(recipe_id=position)
        item.position = current_order
        item.save()
        current_order += 1

    return HttpResponseRedirect('/recipes')


def get_recipe_ids_for_position(request):
    ids = request.POST.get('position')
    ordered_ids = ids.split(',')
    return ordered_ids
