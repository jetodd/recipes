from django.core.management.base import BaseCommand
from django.utils import timezone
from recipes.models import Recipe, Tag
import requests
import os
from PIL import Image
import math

class Command(BaseCommand):
	def handle(self, *args, **options):
		for r in Recipe.objects.all():
			imagePath = os.getcwd() + "/recipes/static/img/" + str(r.id) + ".jpg"
			if not os.path.exists(imagePath):
				picture_request = requests.get(r.image)
				if picture_request.status_code == 200:
						with open(imagePath, 'wb') as f:
							f.write(picture_request.content)
				im = Image.open(imagePath)
				width, height = im.size
				newHeight = math.ceil((180 * height) / width)

				im = im.resize((180, newHeight), Image.ANTIALIAS)
				im.save(imagePath)
