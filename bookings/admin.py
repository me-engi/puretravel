from django.contrib import admin

from .models import Booking, BookingPerson, PaymentStatus


class BookingPersonInline(admin.TabularInline):
    model = BookingPerson
    extra = 1
    show_change_link = True

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'total_travelers', 'payment_status', 'pay_total_amount')
    list_filter = ('payment_status', 'total_travelers')
    search_fields = ('tour__name', 'id')
    inlines = [BookingPersonInline]

@admin.register(BookingPerson)
class BookingPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'traveler_number', 'traveler_name', 'phone_number', 'email')
    list_filter = ('booking__tour', 'booking__total_travelers')
    search_fields = ('booking__tour__name', 'traveler_name', 'phone_number', 'email')

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'payment_successful')
    list_filter = ('payment_successful',)
    search_fields = ('booking__tour__name',)
