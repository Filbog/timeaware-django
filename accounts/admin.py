from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "goal", "is_staff"]
    # fieldsets = UserAdmin.fieldsets + ((None, {"fields": "email"}))
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "goal")}),)


# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
