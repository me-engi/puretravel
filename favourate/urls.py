# favorites/urls.py

from django.urls import path
from .views import FavoriteTourToggle, FavoriteTourUntoggle
from .views import  FavoriteTourList


urlpatterns = [
    path('toggle-favorite/<int:tour_id>/', FavoriteTourToggle.as_view(), name='toggle_favorite'),
    path('untoggle-favorite/<int:tour_id>/', FavoriteTourUntoggle.as_view(), name='untoggle_favorite'),
    path('favorite-tours/', FavoriteTourList.as_view(), name='favorite_tours'),
]
