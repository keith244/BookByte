document.addEventListener('DOMContentLoaded', function() {
    // Get the weekly reading data from the data attribute
    const weeklyDataElement = document.getElementById('weekly-data');
    const weeklyData = JSON.parse(weeklyDataElement.getAttribute('data-weekly'));
    
    // Prepare data for chart
    const labels = weeklyData.map(item => item.day);
    const pagesData = weeklyData.map(item => item.pages);
    
    // Create the weekly reading bar chart
    const weeklyCtx = document.getElementById('weeklyChart').getContext('2d');
    const weeklyChart = new Chart(weeklyCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Pages Read',
                data: pagesData,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',  // Monday
                    'rgba(75, 192, 192, 0.7)',  // Tuesday
                    'rgba(255, 206, 86, 0.7)',  // Wednesday
                    'rgba(153, 102, 255, 0.7)', // Thursday
                    'rgba(255, 159, 64, 0.7)',  // Friday
                    'rgba(255, 99, 132, 0.7)',  // Saturday
                    'rgba(75, 192, 192, 0.7)'   // Sunday
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Pages'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Day of Week'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Pages Read This Week',
                    font: {
                        size: 18
                    }
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y} pages`;
                        }
                    }
                }
            }
        }
    });
});