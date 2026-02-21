from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel, Property, Lease, Announcement, MetersModel, BillModel


admin.site.register(UserModel)
admin.site.register(Property)
admin.site.register(Lease)
admin.site.register(Announcement)
admin.site.register(MetersModel)
admin.site.register(BillModel)

# Register your models here.
