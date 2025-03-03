from django.urls import path

from .views import create_lead, update_lead, get_lead, lead_assign, cancel_lead

urlpatterns = [
    path('get/<int:pk>/', get_lead, name='get_lead'),
    path('create/', create_lead, name='create_lead'),
    path('update/<int:pk>/', update_lead, name='update_lead'),
    path('cancel/<int:pk>/', cancel_lead, name='cancel_lead'),
    path('<int:pk>/assign/', lead_assign, name='lead_assign'),
]