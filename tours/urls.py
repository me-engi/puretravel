from django.urls import path
from .views import (
    TourListView, TourDetailView, TourImagesView, TourSearchView,
    PopularTourListView, TrendingTourListView, apply_coupon,
    TourAvailabilityListView, TourAvailabilityDetailView,
    TourAvailabilityForTourView  # Import the view for tour availability
)

urlpatterns = [
    path('', TourListView.as_view(), name='tour-list'),
    path('<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('<int:pk>/images/', TourImagesView.as_view(), name='tour-images'),
    path('<int:pk>/availability/', TourAvailabilityForTourView.as_view(), name='tour-availability-for-tour'),
    path('availability/', TourAvailabilityListView.as_view(), name='tour-availability-list'),
    path('availability/<int:pk>/', TourAvailabilityDetailView.as_view(), name='tour-availability-detail'),
    path('search/<int:pk>/', TourSearchView.as_view(), name='tour-search'),
    path('popular/', PopularTourListView.as_view(), name='popular-tours'),
    path('trending/', TrendingTourListView.as_view(), name='trending-tours'),
    path('popular/<int:pk>/', PopularTourListView.as_view(), name='popular-tour-detail'),
    path('trending/<int:pk>/', TrendingTourListView.as_view(), name='trending-tour-detail'),
    path('apply-coupon/', apply_coupon, name='apply-coupon'),
]
