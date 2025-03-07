from django.urls import path

from .views import create_property, create_reservation, create_reserved, cancel_reservation

urlpatterns = [
    path('create/', create_property, name='create_property'),
    # Need to change below URL logics and request objects
    path('reservation/', create_reservation, name='create_reservation'),
    path('reservation/<int:pk>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('reservation/<int:pk>/reserved', create_reserved, name='create_reserved')
]