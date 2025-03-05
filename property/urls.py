from django.urls import path

from .views import create_property, create_reservation, create_reserved

urlpatterns = [
    path('create/', create_property, name='create_property'),
    path('<int:pk>/reservation/', create_reservation, name='create_reservation'),
    path('reserved/<int:pk>/', create_reserved, name='create_reserved')
]