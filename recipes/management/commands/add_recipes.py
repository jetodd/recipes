from django.core.management.base import BaseCommand
from django.utils import timezone
from recipes.models import Recipe, Tag
from django.conf import settings
import json
import os
import sys


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'recipes.json'), encoding='utf-8') as f:
            try:
                data = json.load(f)
                recipes = data["recipes"]
                for recipe in recipes:
                    tag_ids = []
                    recipe_ids = []                   
                    if 'related' in recipe:
                        for r in recipe['related']:
                            related = Recipe.objects.filter(image__iexact=r)
                            print('Adding related recipe ' + related[0].title + ' to recipe ' + recipe['title'])
                            recipe_ids.append(related[0].id)
                            
                    if 'tags' in recipe:
                        for tag in recipe['tags']:
                            existing_tags = Tag.objects.filter(name__iexact=tag)
                            if existing_tags:
                                print('Tag ' + tag + ' already exists, skipping')
                                tag_ids.append(existing_tags[0].id)
                            else:
                                print('Adding new tag for ' + tag)
                                new_tag = Tag(name=tag)
                                new_tag.save()
                                tag_ids.append(new_tag.id)

                    existing_recipes = Recipe.objects.filter(title__iexact=recipe['title'])
                    if existing_recipes:
                        print('Recipe ' + recipe['title'] + ' already exists, updating')
                        update_recipe = existing_recipes[0]
                        string_ingredients = '{"ingredients":' + json.dumps(recipe['ingredients']) + '}'
                        string_steps = '{"steps":' + json.dumps(recipe['steps']) + '}'
                        update_recipe.title = recipe['title']
                        update_recipe.image = recipe['image']
                        update_recipe.url = recipe['url']
                        update_recipe.ingredients = string_ingredients
                        update_recipe.steps = string_steps
                        update_recipe.prep = recipe.get('prep', False)
                        update_recipe.save()

                        if 'tags' in recipe:
                            update_recipe.tags.set(tag_ids)
                        if 'related' in recipe:
                            update_recipe.related.set(recipe_ids)
                    else:
                        print('Adding new recipe for ' + recipe['title'])
                        string_ingredients = '{"ingredients":' + json.dumps(recipe['ingredients']) + '}'
                        string_steps = '{"steps":' + json.dumps(recipe['steps']) + '}'
                        r = Recipe(title=recipe['title'], image=recipe['image'], pub_date=timezone.now(),
                                   url=recipe['url'], ingredients=string_ingredients,
                                   steps=string_steps, prep=recipe.get('prep', False))
                        r.save()
                        if 'tags' in recipe:
                            r.tags.set(tag_ids)
                        if 'related' in recipe:
                            r.related.set(recipe_ids)
            except ValueError as e:
                print("Invalid JSON, please use an online formatter silly.")
                print(e)
                sys.exit(1)
