document.addEventListener('DOMContentLoaded', function() {
    // Function to retrieve data from data attributes
    function getDataAttributes(element) {
        const data = {};
        for (const attr of element.attributes) {
            if (attr.name.startsWith('data-')) {
                const key = attr.name.slice(5).replace(/-./g, match => match.charAt(1).toUpperCase());
                data[key] = JSON.parse(attr.value);
            }
        }
        return data;
    }

    // Cases per Municipality
    var ctx = document.getElementById('municipalityChart').getContext('2d');
    var municipalityData = getDataAttributes(document.getElementById('municipalityChart'));
    var muni = municipalityData.municipalities;
    var countMuni = municipalityData.municipalityCaseCounts;

    // Define an array of colors
    var colors = [
        'rgba(54, 162, 235, 0.9)',
        'rgba(255, 99, 132, 0.9)', 
        'rgba(75, 192, 192, 0.9)', 
        'rgba(255, 206, 86, 0.9)',  
        'rgba(153, 102, 255, 0.9)',
        'rgba(255, 159, 64, 0.9)', 
        'rgba(228, 228, 128, 0.9)',
        'rgba(178, 12, 128, 0.9)',
    ];

    var backgroundColors = colors.slice(0, muni.length);

    var municipalityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: muni,
            datasets: [{
                label: 'Number of Cases per Municipality',
                data: countMuni,
                backgroundColor: backgroundColors,
                borderColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Municipality'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Cases'
                    }
                }
            }
        }
    });

    // Gender Chart
    var ctxGender = document.getElementById('genderChart').getContext('2d');
    var genderData = getDataAttributes(document.getElementById('genderChart'));
    var genderLabels = genderData.genderLabels;
    var genderDataValues = genderData.genderData;

    var genderChart = new Chart(ctxGender, {
        type: 'pie',
        data: {
            labels: genderLabels,
            datasets: [{
                label: 'Number of Cases',
                data: genderDataValues,
                backgroundColor: [
                    'rgba(54, 162, 235, 1)', // Color for males
                    'rgba(255, 99, 132, 1)'  // Color for females
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',   // Border color for males
                    'rgba(255, 99, 132, 1)'    // Border color for females
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        let percentage = (value * 100 / sum).toFixed(2) + "%";
                        return percentage;
                    },
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: '14'
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });

    // Animal Chart
    var ctxAnimal = document.getElementById('animalChart').getContext('2d');
    var animalData = getDataAttributes(document.getElementById('animalChart'));
    var animalLabels = animalData.animalLabels;
    var animalDataValues = animalData.animalData;

    var animalChart = new Chart(ctxAnimal, {
        type: 'pie',
        data: {
            labels: animalLabels,
            datasets: [{
                label: 'Number of Cases',
                data: animalDataValues,
                backgroundColor: [
                    'rgba(255, 165, 0, 1)', // Color for cats (orange)
                    'rgba(255, 0, 0, 1)',   // Color for dogs (red)
                    'rgba(128, 128, 128, 1)' // Color for others (grey)
                ],
                borderColor: [
                    'rgba(255, 165, 0, 1)', // Border color for cats (orange)
                    'rgba(255, 0, 0, 1)',   // Border color for dogs (red)
                    'rgba(128, 128, 128, 1)' // Border color for others (grey)
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        let percentage = (value * 100 / sum).toFixed(2) + "%";
                        return percentage;
                    },
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: '14'
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });

    // Gender Scroll
    document.getElementById('scrollToGender').addEventListener('click', function () {
        document.getElementById('scrollGender').scrollIntoView({ 
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest' 
        });
    });
   
    // Animal Scroll
    document.getElementById('scrollToAnimal').addEventListener('click', function () {
        document.getElementById('scrollAnimal').scrollIntoView({ 
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest'
        });
    });
});
