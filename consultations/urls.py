from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="schedule"),
    path('get/', views.get_consultations, name="consultations"),
    path('new/', views.new_consultation, name="new_consultation"),
]