from django.conf import settings
from django.db import models
from django.utils import timezone
from tour.models import Tour

class FavoriteTour(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # Add default value

    class Meta:
        unique_together = ('user', 'tour')

    def __str__(self):
        return f'{self.user.username} - {self.tour.name}'
