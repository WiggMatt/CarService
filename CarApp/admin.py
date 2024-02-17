from django.contrib import admin

from CarApp.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    model = Car
    list_display = ['brand', 'model', 'license_plate', 'color', 'vin_number', 'client']
    search_fields = ['sts', 'brand', 'model', 'license_plate', 'vin_number', 'client']
    list_filter = ['brand', 'body_type', 'color']
    ordering = ['brand']
