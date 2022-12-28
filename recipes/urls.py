from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:recipe_id>/detail', views.detail, name='detail'),
	path('<int:recipe_id>/cooked', views.cooked, name='cooked'),
	path('move', views.move, name='move'),
	path('position/this-week', views.save_this_week_position, name='this-week-position'),
	path('position/next-week', views.save_next_week_position, name='next-week-position'),
	path('tag/<int:tag_id>', views.tag, name='tag'),
	path('all', views.all, name='all'),
	path('shopping', views.shopping, name='shopping'),
	path('deleteitems', views.deleteitems, name='deleteitems'),
	path('search', views.search, name='search'),
	path('random', views.random, name='random')
]
