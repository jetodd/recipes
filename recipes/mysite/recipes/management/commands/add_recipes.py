from django.core.management.base import BaseCommand
from django.utils import timezone
from recipes.models import Recipe, Tag
import json

class Command(BaseCommand):
	def handle(self, *args, **options):
		with open('recipes.json') as f:
			data = json.load(f)
			recipes = data["recipes"]
			for recipe in recipes:
				tag_ids = []
				for tag in recipe['tags']:
					if Tag.objects.filter(name=tag):
						print('Tag ' + tag + ' already exists, skipping')
						tag_ids.append(Tag.objects.filter(name=tag)[0].id)
					else:
						print('Adding new tag for ' + tag)
						new_tag = Tag(name=tag)
						new_tag.save()
						tag_ids.append(new_tag.id)
				if Recipe.objects.filter(title=recipe['title']):
					print('Recipe ' + recipe['title'] + ' already exists, updating')
					update_recipe = Recipe.objects.filter(title=recipe['title'])[0]
					string_ingredients = '{"ingredients":' + json.dumps(recipe['ingredients']) + '}'
					string_steps = '{"steps":' + json.dumps(recipe['steps']) + '}'

					update_recipe.title = recipe['title']
					update_recipe.url = recipe['url']
					update_recipe.ingredients = string_ingredients
					update_recipe.steps = string_steps
					update_recipe.save()
					update_recipe.tags.set(tag_ids)
				else:
					print('Adding new recipe for ' + recipe['title'])
					string_ingredients = '{"ingredients":' + json.dumps(recipe['ingredients']) + '}'
					string_steps = '{"steps":' + json.dumps(recipe['steps']) + '}'
					r = Recipe(title=recipe['title'], pub_date=timezone.now(), url=recipe['url'], ingredients=string_ingredients, 
						steps=string_steps, image=recipe['image'])
					r.save()
					r.tags.set(tag_ids)
