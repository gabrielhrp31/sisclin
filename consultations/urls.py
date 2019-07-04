from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="schedule"),
    path('get/', views.get_schedules, name="get_schedules"),
    path('view_edit/<slug:type>/<int:id>', views.view_edit, name="view_edit_schedules"),
    path('new/<slug:type>', views.new_schedule, name="new_schedule"),
]