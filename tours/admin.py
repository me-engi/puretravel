from django.contrib import admin

from .models import Coupon, Image, Itinerary, Tour, TourAvailability


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class TourAvailabilityInline(admin.TabularInline):
    model = TourAvailability
    extra = 1


class CouponInline(admin.TabularInline):
    model = Coupon
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [ItineraryInline, ImageInline, TourAvailabilityInline, CouponInline]
    list_display = ['id', 'name', 'country', 'price', 'max_participants', 'is_popular', 'is_trending']
    list_filter = ['country', 'is_popular', 'is_trending']
    search_fields = ['name', 'description']

    fieldsets = [
        (None, {'fields': ['name', 'country', 'description']}),
        ('Pricing', {'fields': ['pre_price', 'price', 'max_participants']}),
        ('Flags', {'fields': ['is_popular', 'is_trending']}),
        ('Included and Excluded', {'fields': ['included', 'excluded'], 'classes': ['collapse']}),
    ]

    readonly_fields = ['pre_price']  # Make pre_price readonly

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.append('pre_price')  # Ensure pre_price remains readonly for existing objects
        return readonly_fields

admin.site.register(Image)
admin.site.register(Itinerary)
admin.site.register(TourAvailability)
admin.site.register(Coupon)
