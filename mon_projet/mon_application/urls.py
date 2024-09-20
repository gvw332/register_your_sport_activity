from django.urls import path
from . import views

app_name = 'mon_application' 
urlpatterns = [
   
    path('activity_list/', views.activity_list, name='activity_list'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('update_objectives/', views.update_objectives, name='update_objectives'),
    path('statistics/', views.statistics_view, name='statistics_view'),
]