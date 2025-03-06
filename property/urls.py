from django.urls import path

from .views import create_property, create_reservation, create_reserved

urlpatterns = [
    path('create/', create_property, name='create_property'),
    # Need to change below URL logics and request objects
    path('<int:pk>/reservation/', create_reservation, name='create_reservation'),
    path('<int:pk>/reservation/reserved/<int:rpk>', create_reserved, name='create_reserved')
]