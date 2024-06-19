from datetime import timezone
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Coupon, Image, Itinerary, Tour, TourAvailability
from .serializers import (CouponSerializer, ImageSerializer,
                          ItinerarySerializer, TourAvailabilitySerializer,
                          TourCreateSerializer, TourDetailSerializer,
                          TourSerializer)


class TourListView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_queryset(self):
        queryset = Tour.objects.all()
        place = self.request.query_params.get('place')
        if place:
            queryset = queryset.filter(place__icontains=place)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = TourCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer

@api_view(['GET'])
def tour_detail(request, pk):
    try:
        tour = get_object_or_404(Tour, pk=pk)
        serializer = TourDetailSerializer(tour)
        return Response(serializer.data)
    except Tour.DoesNotExist:
        return Response(status=HTTPStatus.NOT_FOUND)

@api_view(['GET'])
def tour_itinerary(request, pk):
    try:
        tour = get_object_or_404(Tour, pk=pk)
        itinerary = Itinerary.objects.filter(tour=tour)
        serializer = ItinerarySerializer(itinerary, many=True)
        return Response(serializer.data)
    except Tour.DoesNotExist:
        return Response(status=HTTPStatus.NOT_FOUND)

class TourImagesView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        tour_id = self.kwargs.get('pk')
        return Image.objects.filter(tour_id=tour_id)

class TourAvailabilityListView(generics.ListCreateAPIView):
    queryset = TourAvailability.objects.all()
    serializer_class = TourAvailabilitySerializer

    def get_queryset(self):
        tour_id = self.kwargs.get('pk')
        return TourAvailability.objects.filter(tour_id=tour_id)

class TourAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourAvailability.objects.all()
    serializer_class = TourAvailabilitySerializer

# Consider adding a specific view for getting availability for a specific tour
class TourAvailabilityForTourView(generics.ListAPIView):
    serializer_class = TourAvailabilitySerializer

    def get_queryset(self):
        tour_id = self.kwargs['pk']
        return TourAvailability.objects.filter(tour_id=tour_id)

class PopularTourListView(generics.ListAPIView):
    queryset = Tour.objects.filter(is_popular=True)
    serializer_class = TourDetailSerializer

    def get_queryset(self):
        return Tour.objects.filter(is_popular=True)

class TrendingTourListView(generics.ListAPIView):
    queryset = Tour.objects.filter(is_trending=True)
    serializer_class = TourDetailSerializer

    def get_queryset(self):
        return Tour.objects.filter(is_trending=True)

class TourSearchView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            tour_id = int(kwargs.get('pk'))
            tour = Tour.objects.get(pk=tour_id)
            serializer = self.get_serializer(tour)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid tour ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def apply_coupon(request):
    """
    Apply a coupon to a tour and calculate the discounted price.
    """
    if request.method == 'GET':
        try:
            coupons = Coupon.objects.all()
            serializer = CouponSerializer(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Coupon.DoesNotExist:
            return Response({"error": "No coupons found."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            tour_id = request.data.get('tour_id')
            coupon_code = request.data.get('coupon_code')

            tour = Tour.objects.get(pk=tour_id)
            coupon = Coupon.objects.get(code=coupon_code, tour=tour)

            if coupon.expire_date < timezone.now().date() or coupon.max_uses <= 0:
                return Response({"error": "Coupon is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            discounted_price = tour.price - (tour.price * coupon.percentage_discount / 100)

            coupon.max_uses -= 1
            coupon.save()

            return Response({"discounted_price": discounted_price}, status=status.HTTP_200_OK)

        except (Tour.DoesNotExist, Coupon.DoesNotExist):
            return Response({"error": "Tour or Coupon not found."}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
