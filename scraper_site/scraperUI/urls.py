from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:search_term_id>/', views.details, name='detail'),
    path('<int:search_term_id>/results/', views.results, name='results'),
    path('<int:search_term_id>/add/', views.add, name='add'),
]
