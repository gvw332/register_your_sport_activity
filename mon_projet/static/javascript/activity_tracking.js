// Fonction pour récupérer le token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Exemple d'utilisation de la fonction getCookie pour le fetch
document.getElementById('stopActivity').addEventListener('click', function() {
    if (activityStarted) {
        activityStarted = false;

        // Calcul des données
        const speed = (distance / (secondsElapsed / 3600)).toFixed(2);  // Vitesse en km/h
        const data = {
            activityType: activityType,
            totalDistance: distance.toFixed(2),
            speed: speed,
            caloriesBurned: (distance * calorieFactors[activityType]).toFixed(2),
            marche: activityType === 'marche' ? distance.toFixed(2) : 0,
            jogging: activityType === 'jogging' ? distance.toFixed(2) : 0,
            velo: activityType === 'velo' ? distance.toFixed(2) : 0
        };
        // console.log(data);
        // Envoi des données au serveur avec le token CSRF
        fetch('/activities/ajouter-activite-ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assurez-vous de gérer CSRF si CSRF est activé
            },
            body: JSON.stringify(data)  // Assurez-vous que 'data' est un objet JavaScript valide
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Erreur:', error);
        });
    }
});
