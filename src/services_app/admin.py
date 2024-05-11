from django.contrib import admin

from src.services_app.models import Service, ServiceGroup

admin.site.register(Service)
admin.site.register(ServiceGroup)
