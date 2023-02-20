from django.urls import path

from . import views

app_name = 'scraperUI'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:search_term_id>/', views.details, name='details'),
    path('<int:search_term_id>/results/', views.results, name='results'),
    path('<int:search_term_id>/add/', views.add, name='add'),
]
