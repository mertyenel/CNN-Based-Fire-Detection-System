# classifier/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classify/', views.classify_image, name='classify_image'),
    path('random-classify/', views.random_classify_image, name='random_classify_image'),
]