from django.urls import path

from .views import (BookingDetailView, BookingListView, BookingPersonDetail,
                    BookingPersonList)

urlpatterns = [
    path('api/bookings/', BookingListView.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('api/bookings/<int:booking_id>/persons/', BookingPersonList.as_view(), name='booking-person-list'),
    path('api/bookings/<int:booking_id>/persons/<int:traveler_number>/', BookingPersonDetail.as_view(), name='booking-person-detail'),
]