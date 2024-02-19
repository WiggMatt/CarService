from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from AuthenticationApp.models import Client


@admin.register(Client)
class CustomUserAdmin(UserAdmin):
    model = Client
    list_display = ['bio', 'username', 'phone_number', 'is_staff']
    search_fields = ('username', 'bio', 'phone_number')
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('bio', 'phone_number')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "bio", "phone_number", "password1", "password2"),
            },
        ),
    )
