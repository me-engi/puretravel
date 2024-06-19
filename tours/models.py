import os

from django.db import models
from mysite import settings


def tour_image_upload_path(instance, filename):
    return os.path.join("tour_images", instance.tour.name, filename)

class Itinerary(models.Model):
    tour = models.ForeignKey('Tour', related_name='itinerary', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Place')
    day_number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Day {self.day_number}: {self.description}"

class Image(models.Model):
    tour = models.ForeignKey('Tour', related_name='tour_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=tour_image_upload_path)

    def __str__(self):
        return f"Image for {self.tour.name}"

class TourAvailability(models.Model):
    tour = models.ForeignKey('Tour', related_name='availabilities', on_delete=models.CASCADE)
    unavailable_date = models.DateField()

    def __str__(self):
        return f"{self.tour.name} - {self.unavailable_date}"

class Coupon(models.Model):
    tour = models.ForeignKey('Tour', related_name='coupons', on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    max_uses = models.PositiveIntegerField()
    percentage_discount = models.PositiveIntegerField()
    expire_date = models.DateField()

    def __str__(self):
        return f"{self.code} - {self.tour.name}"

class Tour(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='India')
    description = models.TextField()
    pre_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_participants = models.PositiveIntegerField(default=100)
    is_popular = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    included = models.TextField(blank=True, help_text="Comma-separated list of things included in the tour")
    excluded = models.TextField(blank=True, help_text="Comma-separated list of things excluded from the tour")

    def __str__(self):
        return self.name
