from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns= [
	path('', views.index, name='index'),
	path('<int:recipe_id>/detail', views.detail, name='detail'),
	path('<int:recipe_id>/cooked', views.cooked, name='cooked'),
	path('move', views.move, name='move'),
	path('tag/<int:tag_id>', views.tag, name='tag'),
	path('all', views.all, name='all'),
	path('shopping', views.shopping, name='shopping'),
	path('deleteshopping', views.deleteshopping, name='deleteshopping')
]
