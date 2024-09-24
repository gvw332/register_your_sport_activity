function updateChart(labels, marcheData, joggingData, veloData, totalData, caloriesData) {
    const ctx = document.getElementById('activityChart').getContext('2d');
    new Chart(ctx, {
      type: 'line', // Type de graphique
      data: {
        labels: labels, // Étiquettes des axes (dates)
        datasets: [
          {
            label: 'Marche (km)',
            data: marcheData,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
          },
          {
            label: 'Jogging (km)',
            data: joggingData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
          },
          {
            label: 'Vélo (km)',
            data: veloData,
            borderColor: 'rgb(255, 206, 86)',
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            tension: 0.1
          },
          {
            label: 'Total (km)',
            data: totalData,
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            tension: 0.1
          },
          {
            label: 'Calories (kcal)',
            data: caloriesData,
            borderColor: 'rgb(153, 102, 255)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Évolution de marche, course à pied et vélo'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Distance (km) / Calories (kcal)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Date'
            }
          }
        }
      }
    });
}
