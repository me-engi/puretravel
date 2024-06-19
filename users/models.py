from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.models import Permission as AuthPermission
from django.db import models


class UserPro(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Customer(UserPro):
    pass


class DeliveryBoy(UserPro):
    pass


class ShopOwner(UserPro):
    pass


class Tourguide(UserPro):
    pass


class UserGroup(models.Model):
    user = models.ForeignKey(UserPro, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"


class UserPermission(models.Model):
    user = models.ForeignKey(UserPro, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.permission.name}"

