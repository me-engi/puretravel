# favourite/views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteTour
from tour.models import Tour
from .serializers import FavoriteTourSerializer

class FavoriteTourToggle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tour_id):
        # Retrieve the tour object or return 404 if not found
        tour = get_object_or_404(Tour, id=tour_id)

        # Toggle favorite status for the current user
        try:
            favorite_instance = FavoriteTour.objects.get(user=request.user, tour=tour)
            favorite_instance.delete()  # Remove from favorites if already favorited
            return Response({'message': 'Tour removed from favorites'})
        except FavoriteTour.DoesNotExist:
            favorite_instance = FavoriteTour(user=request.user, tour=tour)
            favorite_instance.save()  # Add to favorites
            return Response({'message': 'Tour added to favorites'})

class FavoriteTourUntoggle(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tour_id):
        # Retrieve the tour object or return 404 if not found
        tour = get_object_or_404(Tour, id=tour_id)

        # Remove tour from favorites for the current user
        try:
            favorite_instance = FavoriteTour.objects.get(user=request.user, tour=tour)
            favorite_instance.delete()  # Remove from favorites
            return Response({'message': 'Tour removed from favorites'})
        except FavoriteTour.DoesNotExist:
            return Response({'error': 'Tour is not in favorites'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteTourList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        favorite_tours = FavoriteTour.objects.filter(user=user)
        serializer = FavoriteTourSerializer(favorite_tours, many=True)
        return Response(serializer.data)