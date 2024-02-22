from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from AuthenticationApp.models import Client, Manager, Mechanic, CustomUser, MechanicSpecialization


@admin.register(Client)
class CustomClientAdmin(UserAdmin):
    model = Client
    list_display = ['bio', 'username', 'phone_number']
    search_fields = ('username', 'bio', 'phone_number', 'license_num')
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('bio', 'phone_number', 'license_num')}),
        ('Права', {'fields': ('is_active', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "bio", "phone_number", 'license_num', "password1", "password2"),
            },
        ),
    )


@admin.register(Manager)
class CustomManagerAdmin(UserAdmin):
    model = Manager
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


class MechanicSpecializationInline(admin.TabularInline):
    model = MechanicSpecialization
    extra = 1


@admin.register(Mechanic)
class CustomManagerAdmin(UserAdmin):
    model = Mechanic
    list_display = ['bio', 'username', 'phone_number']
    search_fields = ('username', 'bio', 'phone_number')
    ordering = ['username']
    inlines = [MechanicSpecializationInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('bio', 'phone_number')}),
        ('Права', {'fields': ('is_active', 'groups', 'user_permissions')}),
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


@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    model = CustomUser
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_superuser=True)
