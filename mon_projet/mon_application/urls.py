from django.urls import path
from . import views

app_name = 'mon_application' 
urlpatterns = [
    path('activity_list/', views.activity_list, name='activity_list'),  # URL pour voir la liste des activités
    path('add_activity/', views.add_activity, name='add_activity'),      # URL pour ajouter une activité
    path('edit_activity/<int:pk>/', views.edit_activity, name='edit_activity'),  # URL pour éditer une activité
    path('delete_activity/<int:pk>/', views.delete_activity, name='delete_activity'),  # URL pour supprimer une activité
    path('statistics/', views.statistics_view, name='statistics_view'),  # URL pour voir les statistiques
    path('update_objectives/', views.update_objectives, name='update_objectives'),  # URL pour mettre à jour les objectifs
    path('objectifs/', views.user_objectives_view, name='user_objectives'),  # URL pour voir les objectifs
    
    # Routes API - Conservez le préfixe /api pour ces routes
    path('api/activities/', views.activity_list_api, name='activity_list_api'),  # URL API pour la liste des activités
    path('api/user_objective/', views.user_objective_api, name='user_objective_api'),  # URL API pour les objectifs utilisateur
]