from django.urls import path
from . import views

urlpatterns = [
    #schedule urls
    path('', views.index, name="schedule"),
    path('get/', views.get_schedules, name="get_schedules"),
    path('edit/<slug:type>/<int:id>/', views.edit, name="edit_schedules"),
    path('view/<int:id>/', views.view, name="view_schedules"),
    path('new/<slug:type>/', views.new_schedule, name="new_schedule"),
    path('delete/<int:id>/<slug:location>/', views.delete_consultation, name="delete_consultation"),
    path('delete/<int:id>/', views.delete_schedule, name='delete_schedule'),
    #procedure urls
    path('procedures/', views.list_procedures, name='procedures'),
    path('procedures/get/', views.get_procedures, name='get_procedures'),
    path('procedures/new/', views.new_procedure, name='new_procedure'),
    path('procedures/view_edit/<int:id>/', views.view_edit_procedure, name='view_edit_procedure'),
    path('procedures/delete/<int:id>/', views.delete_procedure, name='delete_procedure'),
]