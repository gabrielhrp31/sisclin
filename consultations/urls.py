from django.urls import path
from . import views

urlpatterns = [
    #schedule urls
    path('', views.index, name="schedule"),
    path('get/', views.get_schedules, name="get_schedules"),
    path('view_edit/<slug:type>/<int:id>/', views.view_edit, name="view_edit_schedules"),
    path('new/<slug:type>/', views.new_schedule, name="new_schedule"),
    #procedure urls
    path('procedures/', views.list_procedures, name='procedures'),
    path('procedures/new/', views.new_procedure, name='new_procedure'),
    path('procedures/view_edit/<int:id>/', views.view_edit_procedure, name='view_edit_procedure'),
]