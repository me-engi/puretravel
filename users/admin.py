from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Customer, DeliveryBoy, ShopOwner, Tourguide, UserGroup,
                     UserPermission, UserPro)


class CustomUserAdmin(UserAdmin):
    model = UserPro
    list_display = ['username', 'email', 'phone_number', 'address', 'date_joined', 'is_active']
    search_fields = ['username', 'email', 'phone_number', 'address']
    list_filter = ['date_joined', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'address', 'password1', 'password2'),
        }),
    )


class CustomerAdmin(CustomUserAdmin):
    model = Customer


class DeliveryBoyAdmin(CustomUserAdmin):
    model = DeliveryBoy


class ShopOwnerAdmin(CustomUserAdmin):
    model = ShopOwner


class TourguideAdmin(CustomUserAdmin):
    model = Tourguide


admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeliveryBoy, DeliveryBoyAdmin)
admin.site.register(ShopOwner, ShopOwnerAdmin)
admin.site.register(Tourguide, TourguideAdmin)
admin.site.register(UserPro, CustomUserAdmin)
admin.site.register(UserGroup)
admin.site.register(UserPermission)
