from django.contrib import admin
from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.ScheduleListView.as_view(), name='schedule_list'),
    path('week/<int:year>/<int:month>/<int:day>/', views.ScheduleListView.as_view(), name='schedule_list'),
    # path('create/<int:year>/<int:month>/<int:day>/', views.ScheduleCreateView.as_view(), name='schedule_create'),
]