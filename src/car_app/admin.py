from django.contrib import admin

from src.users_app.models import Client
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    model = Car
    list_display = ['brand', 'model', 'license_plate', 'color', 'vin_number', 'client']
    search_fields = ['sts', 'brand', 'model', 'license_plate', 'vin_number', 'client']
    list_filter = ['brand', 'body_type', 'color']
    ordering = ['brand']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            # Ограничиваем выбор клиента только теми, у кого is_client = True
            kwargs["queryset"] = Client.objects.filter(is_client=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)