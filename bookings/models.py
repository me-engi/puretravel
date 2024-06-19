# models.py

from django.db import models
from django.utils import timezone  # Import timezone module

from mysite import settings
from tour.models import Tour, TourAvailability


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    total_travelers = models.PositiveIntegerField(default=1)
    payment_status = models.BooleanField(default=False, blank=True, null=True)
    pay_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tour_availability = models.ForeignKey(TourAvailability, on_delete=models.CASCADE, null=True)  # Add default date

    def save(self, *args, **kwargs):
        # Calculate the total amount based on the tour's price and the number of travelers
        self.pay_total_amount = self.tour.price * self.total_travelers

        # Set the tour availability for the booking
        if not self.tour_availability:
            # If no specific availability is provided, use the tour's default availability
            self.tour_availability = self.tour.default_availability

        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Booking for {self.tour.name} on {self.tour_availability.unavailable_date}"


class BookingPerson(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ID_PROOF_CHOICES = [
        ('aadhar_card', 'Aadhar Card'),
        ('citizenship', 'Citizenship'),
        ('passport', 'Passport'),
    ]


    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)
    traveler_number = models.PositiveIntegerField(default=False, null=True, blank=True)
    traveler_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField( blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    id_proof_type = models.CharField(max_length=50, choices=ID_PROOF_CHOICES, blank=True, null=True)
    id_proof_upload = models.ImageField(upload_to='id_proof_uploads/', blank=True, null=True)
    photo = models.ImageField(upload_to='booking_photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
    # Ensure that traveler_number does not exceed total_travelers
       if self.traveler_number is not None and self.booking is not None and self.booking.total_travelers is not None:
           if self.traveler_number > self.booking.total_travelers:
               raise ValueError("Traveler number cannot exceed total travelers.")

       super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.traveler_name}'s details for booking {self.booking.id}, Traveler {self.traveler_number}"




class PaymentStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment status for booking {self.booking.id}"
