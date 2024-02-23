from django.urls import path
from . import views

urlpatterns = [
    path('appeals/', views.appeals_view, name='appeals_view'),
    path('appeals/create_appeal/', views.create_appeal, name='create_appeal'),
    path('all-appeals/', views.all_appeals_view, name='all_appeals'),
    path('appeal/<int:appeal_id>/', views.appeal_details, name='appeal_details'),
]
