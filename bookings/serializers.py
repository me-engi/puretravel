from rest_framework import serializers

from tour.models import Tour

from .models import Booking, BookingPerson


class BookingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPerson
        fields = '__all__'
        extra_kwargs = {
            'booking': {'required': False},  # Make the field not required for creation
        }

class BookingPersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPerson
        fields = '__all__'
        extra_kwargs = {
            'booking': {'required': False},  # Make the field not required for creation
        }

    def create(self, validated_data):
        booking = self.context['booking']
        return BookingPerson.objects.create(booking=booking, **validated_data)

class BookingDetailSerializer(serializers.ModelSerializer):
    persons = BookingPersonSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def get_id_proof_upload(self, instance):
        return instance.id_proof_upload.url if instance.id_proof_upload else None

    def get_photo(self, instance):
        return instance.photo.url if instance.photo else None

class BookingCreateSerializer(serializers.ModelSerializer):
    persons = BookingPersonSerializer(many=True, required=False)
    tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        persons_data = validated_data.pop('persons', None)
        booking = Booking.objects.create(**validated_data)

        if persons_data:
            for person_data in persons_data:
                id_proof_upload = person_data.pop('id_proof_upload', None)
                photo = person_data.pop('photo', None)

                # Create BookingPerson without bulk_create to handle file uploads
                person = BookingPerson.objects.create(booking=booking, **person_data)

                # Handle file uploads separately
                if id_proof_upload:
                    person.id_proof_upload = id_proof_upload
                if photo:
                    person.photo = photo

                person.save()

        return booking

    def update(self, instance, validated_data):
        persons_data = validated_data.pop('persons', None)

        # Update regular fields
        instance.tour = validated_data.get('tour', instance.tour)
        instance.total_travelers = validated_data.get('total_travelers', instance.total_travelers)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.save()

        if persons_data is not None:
            # Create or update BookingPerson instances in the updated data
            for person_data in persons_data:
                traveler_number = person_data.get('traveler_number')
                person, created = BookingPerson.objects.get_or_create(booking=instance, traveler_number=traveler_number)

                # Update person fields
                person.traveler_name = person_data.get('traveler_name', person.traveler_name)
                person.phone_number = person_data.get('phone_number', person.phone_number)
                person.email = person_data.get('email', person.email)
                person.address = person_data.get('address', person.address)
                person.id_proof_type = person_data.get('id_proof_type', person.id_proof_type)

                # Handle file uploads separately
                id_proof_upload = person_data.get('id_proof_upload')
                photo = person_data.get('photo')

                if id_proof_upload:
                    person.id_proof_upload = id_proof_upload
                if photo:
                    person.photo = photo

                person.save()

            # Delete BookingPerson instances not present in the updated data
            updated_traveler_numbers = {person_data['traveler_number'] for person_data in persons_data}
            instance.persons.exclude(traveler_number__in=updated_traveler_numbers).delete()

        return instance
