from django.db import models

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Recipe(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	url = models.CharField(max_length=200)
	ingredients = models.TextField()
	steps = models.TextField()
	image = models.CharField(max_length=200)
	tags = models.ManyToManyField(Tag)
	this_week = models.BooleanField(default=False)
	next_week = models.BooleanField(default=False)
	def __str__(self):
		return self.title