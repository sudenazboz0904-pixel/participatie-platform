from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('stem/<slug:proposal_slug>/', views.vote, name='vote'),
]
