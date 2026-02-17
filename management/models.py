from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class UserModel(AbstractUser):
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.username


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,)
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    size = models.DecimalField(max_digits=5, decimal_places=2)
    rooms = models.IntegerField()

    def __str__(self):
        return self.title


class Lease(models.Model):
    # zmienic na foreign key
    tenant = models.ManyToManyField(UserModel, related_name='leases')

    # zmienic na foreign key

    flat = models.OneToOneField(
        Property, related_name='leases',  on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=8, decimal_places=2)
    deposit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.flat} {self.tenant}'

# class Meter(models.Model):
#     flat = models.OneToOneField(
#         Property, related_name='meters',  on_delete=models.CASCADE)
#     value = models.DecimalField(max_digits=8, decimal_places=2)
#     date = models.DateField(auto_now_add=False)

#     class MeterChoices(models.TextChoices):
#         ELECTRICITY = 'kWh',
#         WATER = 'm3',
#         GAS = 'm3',
#         HEAT = 'kWh'


# class Bill(models.Model):
#     flat = models.OneToOneField(
#         Property, related_name='meters',  on_delete=models.CASCADE)
#     tenant = models.OneToOneField(
#         User, verbose_name=_(""), on_delete=models.CASCADE)
#     rent_amount = models.DecimalField(max_digits=8, decimal_places=2)
#     utilities_amount = models.DecimalField(max_digits=8, decimal_places=2)
#     is_paid = models.BooleanField(default=False)


# class Announcement(models.Model):

#     title = models.CharField(max_length=50)
#     content = models.CharField(max_length=250)
#     created_at = models.DateField(auto_now_add=True)


# class Issue(models.Model):
#     tenant = models.ForeignKey(
#         Property, related_name='issue', on_delete=models.CASCADE)
#     flat = models.ForeignKey(
#         Property, related_name='issue', on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     description = models.CharField(max_length=250)

#     class issueStatus(models.TextChoices):
#         OPEN = 'open'
#         IN_PROGRESS = 'in_progress'
#         DONE = 'done'
