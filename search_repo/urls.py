from django.urls import path
from . import views

urlpatterns = [
    # Home page URL
    path('', views.home, name='home'),

    # Search page URL
    path('search/', views.search, name='search'),
]