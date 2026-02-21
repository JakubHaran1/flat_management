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
    tenant = models.ForeignKey(
        UserModel, related_name='tenant_leases', on_delete=models.CASCADE)
    landlord = models.ForeignKey(
        UserModel, related_name='landlord_leases', on_delete=models.CASCADE)

    flat = models.ForeignKey(
        Property, related_name='leases',  on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=8, decimal_places=2)
    deposit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.flat} {self.tenant}'


class BillModel(models.Model):
    lease = models.ForeignKey(
        Lease, related_name='bills',  on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    rent_amount = models.DecimalField(max_digits=8, decimal_places=2)
    utilities_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)


class MetersModel(models.Model):
    electricity = models.DecimalField(max_digits=8, decimal_places=2)
    water = models.DecimalField(max_digits=8, decimal_places=2)
    gas = models.DecimalField(max_digits=8, decimal_places=2)
    heat = models.DecimalField(max_digits=8, decimal_places=2)
    bill = models.OneToOneField(
        BillModel,  related_name='meters', on_delete=models.CASCADE, default="")


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    sender = models.ForeignKey(
        UserModel, related_name='sender_announcement', on_delete=models.CASCADE)
    recipient = models.ManyToManyField(
        UserModel, related_name='recipient_announcement')

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
