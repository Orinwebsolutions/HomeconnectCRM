from django.urls import path

from .views import create_lead, update_lead

urlpatterns = [
    path('create/', create_lead, name='create_lead'),
    path('update/<int:pk>/', update_lead, name='update_lead'),
]