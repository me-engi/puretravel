from rest_framework import serializers
from .models import Image, Tour, Itinerary, TourAvailability, Coupon

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class TourAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAvailability
        fields = ['id', 'tour', 'unavailable_date']  # Add 'id' field to include the primary key

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class PopularTourSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'name', 'tour_images']
        read_only_fields = ['is_popular']

class TrendingTourSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'name', 'tour_images']
        read_only_fields = ['is_trending']

class TourSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True, read_only=True)
    itinerary = ItinerarySerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'

class TourCreateSerializer(serializers.ModelSerializer):
    itinerary = ItinerarySerializer(many=True, required=False)

    class Meta:
        model = Tour
        fields = '__all__'

    def create(self, validated_data):
        itinerary_data = validated_data.pop('itinerary', None)
        tour = Tour.objects.create(**validated_data)

        if itinerary_data:
            for day_data in itinerary_data:
                Itinerary.objects.create(tour=tour, **day_data)

        return tour

class TourDetailSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True, read_only=True)
    itinerary = ItinerarySerializer(many=True, read_only=True)
    coupon_set = CouponSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'
