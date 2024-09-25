from django.shortcuts import render, get_object_or_404, redirect
from .forms import ActivityForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import UserObjective, Activity
from .forms import UserObjectiveForm
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ActivitySerializer, UserObjectiveSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# from django.http import HttpResponse
def accueil_view(request):
    activities = Activity.objects.all()  # Récupère toutes les activités

    # Récupérer les objectifs de l'utilisateur
    try:
        user_objective = UserObjective.objects.get(user=request.user)
    except UserObjective.DoesNotExist:
        user_objective = UserObjective(objectif_marche=10, objectif_jogging=5, objectif_velo=20)

    # Totaux
    total_marche = Activity.objects.aggregate(Sum('marche'))['marche__sum'] or 0
    total_jogging = Activity.objects.aggregate(Sum('jogging'))['jogging__sum'] or 0
    total_velo = Activity.objects.aggregate(Sum('velo'))['velo__sum'] or 0
    total_calories = Activity.objects.aggregate(Sum('calories'))['calories__sum'] or 0

    # Calcul du total des kilomètres effectués
    total_kilometres = total_marche + total_jogging + total_velo

    context = {
        'activities': activities,
        'user_objective': user_objective,
        'total_marche': total_marche,
        'total_jogging': total_jogging,
        'total_velo': total_velo,
        'total_calories': total_calories,
        'total_kilometres': total_kilometres,  # Vérifie que cette ligne est présente
    }
    
    return render(request, 'mon_application/accueil.html', context)

def contact(request):
    return render(request, 'contact.html')

@login_required
def activity_list(request):
    if request.user.is_authenticated:
        activities = Activity.objects.filter(user=request.user)
    else:
        activities = []
    return render(request, 'activity_list.html', {'activities': activities})

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)  # Ne pas enregistrer tout de suite
            activity.user = request.user  # Si tu as besoin d'associer un utilisateur
            activity.save()  # Enregistre l'activité et calcule total et calories
            return redirect('mon_application:activity_list')
    else:
        form = ActivityForm()
    
    return render(request, 'add_activity.html', {'form': form})

@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('mon_application:activity_list')
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})
@login_required
def delete_activity(request, pk):

    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        # Redirection vers la liste des activités
        return redirect('mon_application:activity_list')  # Redirection correcte vers l'URL
    return render(request, 'confirm_delete.html', {'activity': activity})  # Le bon template pour la confirmation

@login_required
def statistics_view(request):
    # Objectifs
    try:
        user_objective = UserObjective.objects.get(user=request.user)
    except UserObjective.DoesNotExist:
        user_objective = UserObjective(objectif_marche=10, objectif_jogging=5, objectif_velo=20)

    # Filtrer les activités pour l'utilisateur connecté
    user_activities = Activity.objects.filter(user=request.user)

    # Totaux
    total_marche = user_activities.aggregate(Sum('marche'))['marche__sum'] or 0
    total_jogging = user_activities.aggregate(Sum('jogging'))['jogging__sum'] or 0
    total_velo = user_activities.aggregate(Sum('velo'))['velo__sum'] or 0
    total_calories = user_activities.aggregate(Sum('calories'))['calories__sum'] or 0
    total_kilometres = total_marche + total_jogging + total_velo
    # Dernier enregistrement
    dernier_encodage = user_activities.last()
    distance_marche_derniere = dernier_encodage.marche if dernier_encodage else 0
    distance_jogging_derniere = dernier_encodage.jogging if dernier_encodage else 0
    distance_velo_derniere = dernier_encodage.velo if dernier_encodage else 0

    # Préparation des données pour le graphique
    labels = [activity.date.strftime('%Y-%m-%d') for activity in user_activities]  # Assurez-vous d'utiliser le bon champ de date
    marche_data = [activity.marche for activity in user_activities]
    jogging_data = [activity.jogging for activity in user_activities]
    velo_data = [activity.velo for activity in user_activities]
    calories_data = [activity.calories for activity in user_activities]

    # Calcul des totaux par date
    total_data = [m + j + v for m, j, v in zip(marche_data, jogging_data, velo_data)]

    context = {
        'total_marche': total_marche,
        'total_jogging': total_jogging,
        'total_velo': total_velo,
        'total_calories': total_calories,
        'total_kilometres': total_kilometres,  
        'distance_marche_derniere': distance_marche_derniere,
        'distance_jogging_derniere': distance_jogging_derniere,
        'distance_velo_derniere': distance_velo_derniere,
        'user_objective': user_objective,
        'labels': labels,  # Les dates pour le graphique
        'marche_data': marche_data,  # Données de marche
        'jogging_data': jogging_data,  # Données de jogging
        'velo_data': velo_data,  # Données de vélo
        'total_data': total_data,  # Données totales
        'calories_data': calories_data,  # Données de calories
    }

    return render(request, 'statistics_view.html', context)



@login_required
def update_objectives(request):
    try:
        objectives = UserObjective.objects.get(user=request.user)
    except UserObjective.DoesNotExist:
        objectives = UserObjective(user=request.user)

    if request.method == 'POST':
        form = UserObjectiveForm(request.POST, instance=objectives)
        if form.is_valid():
            form.save()
            return redirect('statistics_view')
    else:
        form = UserObjectiveForm(instance=objectives)

    return render(request, 'accueil.html', {'form': form})




@login_required
def user_objectives_view(request):
    # Récupérer ou créer les objectifs de l'utilisateur connecté avec des valeurs par défaut à zéro
    user_objective, created = UserObjective.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserObjectiveForm(request.POST, instance=user_objective)
        if form.is_valid():
            form.save()
            return redirect('mon_application:user_objectives')  # Redirection après modification
    else:
        form = UserObjectiveForm(instance=user_objective)

    context = {
        'form': form,
        'user_objective': user_objective,
    }
    return render(request, 'user_objectives.html', context)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def activity_list_api(request):
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associe l'utilisateur connecté
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_objective_api(request):
    try:
        user_objective = UserObjective.objects.get(user=request.user)
    except UserObjective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserObjectiveSerializer(user_objective)
    return Response(serializer.data)