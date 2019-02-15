from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns= [
	path('', views.index, name='index'),
	path('<int:recipe_id>/detail', views.detail, name='detail'),
	path('tag/<int:tag_id>', views.tag, name='tag'),
	path('all', views.all, name='all')
]