from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel, Property, Lease


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_landlord', 'is_tenant')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(UserModel)
admin.site.register(Property)
admin.site.register(Lease)

# Register your models here.
