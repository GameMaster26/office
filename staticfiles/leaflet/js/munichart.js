// Function to map intensity based on the count of cases
function getMuniColorByCases(count) {
    var intensityColors = [
        '#6DA9FF', // Medium-light blue
        '#6DA9FF', // Medium-light blue
        '#3399FF', // Medium blue
        '#3399FF', // Medium blue
        '#007BFF', // Primary blue (Bootstrap primary)
        '#007BFF', // Primary blue (Bootstrap primary)
        '#0069D9', // Dark blue
        '#0069D9', // Dark blue
        '#0056B3', // Darker blue
        '#0056B3', // Darker blue
        '#004085',  // Darkest blue
        '#004085',  // Darkest blue
    ];

    if (count < 50) {
        return intensityColors[0];
    } else if (count < 100) {
        return intensityColors[1];
    } else if (count < 200) {
        return intensityColors[2];
    } else if (count < 300) {
        return intensityColors[3];
    } else if (count < 400) {
        return intensityColors[4];
    } else if (count < 500) {
        return intensityColors[5];
    } else {
        return intensityColors[6];
    }
}

// Initialize Municipality Chart
function initMunicipalityChart(municipalities, municipality_case_counts) {
    var ctx = document.getElementById('municipalityChart').getContext('2d');
    var totalCasesPerMuni = municipality_case_counts.reduce((acc, val) => acc + val, 0); // Calculate total cases
    var backgroundColors = municipality_case_counts.map(count => getMuniColorByCases(count));
    var borderColors = backgroundColors;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: municipalities,
            datasets: [{
                label: 'Number of Cases per Municipality',
                data: municipality_case_counts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 30,
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
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                datalabels: {
                    formatter: (value) => value,
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 14
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// Initialize Gender Chart
function initGenderChart(genderLabels, genderData) {
    var ctxGender = document.getElementById('genderChart').getContext('2d');
    new Chart(ctxGender, {
        type: 'pie',
        data: {
            labels: genderLabels,
            datasets: [{
                label: 'Number of Cases',
                data: genderData,
                backgroundColor: [
                    'rgba(54, 162, 235, 1)', // Color for males
                    'rgba(255, 99, 132, 1)'  // Color for females
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)', // Border color for males
                    'rgba(255, 99, 132, 1)'  // Border color for females
                ],
                borderWidth: 1,
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
}

// Initialize Animal Chart
function initAnimalChart(animalLabels, animalData) {
    // Group data into "Dog", "Cat", and "Others"
    const groupedData = { 'Dog': 0, 'Cat': 0, 'Others': 0 };
    const otherAnimals = [];  // To store names of animals in "Others" category

    animalLabels.forEach((label, index) => {
        const count = animalData[index];
        if (label === 'Dog' || label === 'Cat') {
            groupedData[label] += count;
        } else {
            groupedData['Others'] += count;
            otherAnimals.push(`${label}: ${count}`);
        }
    });

    // Prepare data for Chart.js
    const chartLabels = Object.keys(groupedData);  // ["Dog", "Cat", "Others"]
    const chartData = Object.values(groupedData);  // Corresponding data counts

    // Tooltip content for "Others" category
    const othersTooltipText = otherAnimals.join(', ');

    var ctxAnimal = document.getElementById('animalChart').getContext('2d');
    new Chart(ctxAnimal, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Number of Cases',
                data: chartData,
                backgroundColor: [
                    'rgba(255, 165, 0, 1)', // Dog color
                    'rgba(255, 0, 0, 1)',   // Cat color
                    'rgba(128, 128, 128, 1)' // Others color
                ],
                borderColor: [
                    'rgba(255, 165, 0, 1)', // Dog border color
                    'rgba(255, 0, 0, 1)',   // Cat border color
                    'rgba(128, 128, 128, 1)' // Others border color
                ],
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        // Custom tooltip to show details when hovering "Others"
                        label: function(context) {
                            if (context.label === 'Others') {
                                return othersTooltipText; // Show "Others" details on hover
                            } else {
                                return `${context.label}: ${context.raw}`; // Show regular label and value for Dog/Cat
                            }
                        }
                    }
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        let percentage = (value * 100 / sum).toFixed(2);
                        return percentage > 0 ? percentage + "%" : ''; // Exclude 0% labels
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
}

