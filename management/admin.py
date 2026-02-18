from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel, Property, Lease


admin.site.register(UserModel)
admin.site.register(Property)
admin.site.register(Lease)

# Register your models here.
