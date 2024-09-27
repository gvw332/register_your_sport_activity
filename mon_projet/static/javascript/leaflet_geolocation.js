// Initialisation de la carte
const map = L.map('map').setView([50.5667, 4.6833], 18);

// Chargement de la couche de tuiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variables pour stocker la position de l'utilisateur, la distance, le tracé, et la vitesse
let startPosition = null;
let distance = 0;
let geoInterval = null;
let activityType = '';
let chronoInterval = null;
let secondsElapsed = 0;
let path = [];  // Tableau pour stocker les positions et tracer le chemin
let polyline = null;  // Référence au tracé de la polyline

// Facteurs de calories par km en fonction du type d'activité
const calorieFactors = {
    marche: 50,
    jogging: 80,
    velo: 40
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

                // Initialiser le tracé avec la première position
                path.push(startPosition);
                polyline = L.polyline(path, {color: 'blue'}).addTo(map);
            } else {
                const newPosition = [lat, lng];
                const distanceTemp = map.distance(startPosition, newPosition) / 1000;
                distance += distanceTemp;
                startPosition = newPosition;

                // Mise à jour du tracé avec la nouvelle position
                path.push(newPosition);
                polyline.setLatLngs(path);  // Met à jour le tracé avec les nouvelles positions

                // Mise à jour de la distance et des informations de l'activité
                document.getElementById('distance').textContent = distance.toFixed(2);
                const hoursElapsed = secondsElapsed / 3600;
                const speed = distance / hoursElapsed;
                document.getElementById('speed').textContent = speed.toFixed(2);
                const caloriesBurned = distance * calorieFactors[activityType];
                document.getElementById('calories').textContent = caloriesBurned.toFixed(2);

                // Mise à jour de la carte
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

let activityStarted = false;

// Démarrer l'activité et le chronomètre
document.getElementById('startActivity').addEventListener('click', function() {
    if (!activityStarted) {
        activityStarted = true;

        // Récupérer le type d'activité
        activityType = document.getElementById('activityType').value;

        // Changer le texte du bouton
        document.getElementById('startActivity').textContent = "Activité en cours...";

        // Démarre la géolocalisation toutes les 5 secondes
        geoInterval = setInterval(locateUser, 1000);

        // Démarre le chronomètre
        chronoInterval = setInterval(updateChrono, 1000);

        document.getElementById('startActivity').disabled = true;
        document.getElementById('stopActivity').disabled = false;
    }
});

// Stopper l'activité
document.getElementById('stopActivity').addEventListener('click', function() {
    if (activityStarted) {
        activityStarted = false;

        clearInterval(geoInterval);
        clearInterval(chronoInterval);

        document.getElementById('startActivity').disabled = false;
        document.getElementById('stopActivity').disabled = true;

        document.getElementById('startActivity').textContent = "Démarrer l'activité";
        alert("Activité terminée ! Distance totale : " + distance.toFixed(2) + " km, Calories : " + (distance * calorieFactors[activityType]).toFixed(2) + " kcal");
    }
});
