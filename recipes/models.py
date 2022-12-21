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
    cooked_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ThisWeekMealItem(models.Model):
    this_week = models.BooleanField()


class NextWeekMealItem(models.Model):
    next_week = models.BooleanField()


class ThisWeekItem(models.Model):
    position = models.IntegerField(blank=False, default=100_000)
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='this_week')

    def __str__(self):
        return self.position


class NextWeekItem(models.Model):
    position = models.IntegerField(blank=False, default=100_000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='next_week')

    def __str__(self):
        return self.position


class ShoppingItem(models.Model):
    name = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
