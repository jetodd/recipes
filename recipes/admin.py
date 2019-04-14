from django.contrib import admin

# Register your models here.
from .models import Tag, Recipe, ShoppingItem

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(ShoppingItem)