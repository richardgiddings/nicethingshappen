from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('report/<int: nice_thing_id>/', views.report, name='report'),
]