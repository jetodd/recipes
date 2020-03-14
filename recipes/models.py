from django.db import models

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Recipe(models.Model):
	title = models.CharField(max_length=200)
	image = models.CharField(max_length=200, default="")
	pub_date = models.DateTimeField('date published')
	url = models.CharField(max_length=200)
	ingredients = models.TextField()
	steps = models.TextField()
	tags = models.ManyToManyField(Tag)
	this_week = models.BooleanField(default=False)
	next_week = models.BooleanField(default=False)
	cooked_count = models.IntegerField(default=0)
	def __str__(self):
		return self.title

class ShoppingItem(models.Model):
	name = models.CharField(max_length=200)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return self.name