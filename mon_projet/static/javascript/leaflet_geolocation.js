// Initialisation de la carte
const map = L.map('map').setView([51.505, -0.09], 13);

// Chargement de la couche de tuiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variables pour stocker la position de l'utilisateur, la distance et la vitesse
let startPosition = null;
let distance = 0;
let geoInterval = null;  // Pour stocker l'intervalle de géolocalisation
let activityType = '';  // Type d'activité sélectionné
let chronoInterval = null;
let secondsElapsed = 0;

// Facteurs de calories par km en fonction du type d'activité
const calorieFactors = {
    marche: 50,   // Marche : 50 kcal/km
    jogging: 80,  // Jogging : 80 kcal/km
    velo: 40      // Vélo : 40 kcal/km
};

// Fonction de géolocalisation
function locateUser() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            // Mise à jour de la position initiale
            if (!startPosition) {
                startPosition = [lat, lng];
                L.marker(startPosition).addTo(map).bindPopup('Départ').openPopup();
                map.setView(startPosition, 13);
            } else {
                // Calcul de la distance entre deux points
                const newPosition = [lat, lng];
                const distanceTemp = map.distance(startPosition, newPosition) / 1000; // Distance en km
                distance += distanceTemp;
                startPosition = newPosition;

                // Affichage de la distance
                document.getElementById('distance').textContent = distance.toFixed(2);

                // Calcul et affichage de la vitesse (km/h)
                const hoursElapsed = secondsElapsed / 3600;  // Convertir les secondes en heures
                const speed = distance / hoursElapsed;
                document.getElementById('speed').textContent = speed.toFixed(2);

                // Calcul et affichage des calories dépensées
                const caloriesBurned = distance * calorieFactors[activityType];
                document.getElementById('calories').textContent = caloriesBurned.toFixed(2);

                // Mise à jour de la carte avec la nouvelle position
                L.marker(newPosition).addTo(map);
                map.panTo(newPosition);
            }
        });
    } else {
        alert("La géolocalisation n'est pas prise en charge par votre navigateur.");
    }
}

// Fonction de mise à jour du chronomètre
function updateChrono() {
    secondsElapsed++;
    const hours = Math.floor(secondsElapsed / 3600);
    const minutes = Math.floor((secondsElapsed % 3600) / 60);
    const seconds = secondsElapsed % 60;

    document.getElementById('chrono').textContent = 
        `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Démarrer l'activité et le chronomètre
document.getElementById('startActivity').addEventListener('click', function() {
    if (!activityStarted) {
        activityStarted = true;
        
        // Récupérer le type d'activité choisi
        activityType = document.getElementById('activityType').value;
        
        // Changer le texte du bouton
        document.getElementById('startActivity').textContent = "Activité en cours...";

        // Démarre la géolocalisation répétée toutes les 5 secondes
        geoInterval = setInterval(locateUser, 5000);

        // Démarre le chronomètre
        chronoInterval = setInterval(updateChrono, 1000);

        // Désactiver le bouton démarrer et activer le bouton stop
        document.getElementById('startActivity').disabled = true;
        document.getElementById('stopActivity').disabled = false;
    }
});

// Stopper l'activité et le chronomètre
document.getElementById('stopActivity').addEventListener('click', function() {
    if (activityStarted) {
        activityStarted = false;

        // Stopper la géolocalisation et le chronomètre
        clearInterval(geoInterval);
        clearInterval(chronoInterval);

        // Réinitialiser les boutons
        document.getElementById('startActivity').disabled = false;
        document.getElementById('stopActivity').disabled = true;

        // Afficher que l'activité est terminée
        document.getElementById('startActivity').textContent = "Démarrer l'activité";
        alert("Activité terminée ! Distance totale : " + distance.toFixed(2) + " km, Calories : " + (distance * calorieFactors[activityType]).toFixed(2) + " kcal");
    }
});
