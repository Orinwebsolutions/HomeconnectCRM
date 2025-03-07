from django.urls import path

from .views import create_lead, update_lead, get_lead, lead_assign, change_status

urlpatterns = [
    path('get/<int:pk>/', get_lead, name='get_lead'),
    path('create/', create_lead, name='create_lead'),
    path('update/<int:pk>/', update_lead, name='update_lead'),
    path('<int:pk>/assign/', lead_assign, name='lead_assign'),
    path('<int:pk>/change-status/', change_status, name='change_status'),
]