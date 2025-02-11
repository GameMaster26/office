// Function to initialize the Monthly Cases Chart
function initMonthlyChart(months, caseCounts) {
    var ctx = document.getElementById('monthlyCasesChart').getContext('2d');
    
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

    // Function to map intensity based on the count of cases (for monthly cases)
    function getMonthlyColorByCases(count) {
        if (count < 50) {
            return intensityColors[0]; // Very light grey for low counts
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
            return intensityColors[6]; // Darker grey for high counts
        }
    }

    // Generate background and border colors based on the number of monthly cases
    var backgroundColors = caseCounts.map(count => getMonthlyColorByCases(count));
    var borderColors = backgroundColors.map(color => color.replace('0.6', '0.7')); // Darker border

    var monthlyCasesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Monthly Cases',
                data: caseCounts,
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
                        text: 'Month'
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

// Function to initialize the Weekly Cases Chart
function initWeeklyChart(weeks, weeklyCounts) {
    var ctxWeekly = document.getElementById('weeklyCasesChart').getContext('2d');

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

    // Function to map intensity based on the count of cases (for weekly cases)
    function getColorByCases(count) {
        if (count < 50) {
            return intensityColors[0]; // Very light grey for low counts
        } else if (count < 100) {
            return intensityColors[1];
        } else if (count < 200) {
            return intensityColors[2];
        } else if (count < 250) {
            return intensityColors[3];
        } else if (count < 300) {
            return intensityColors[4];
        } else if (count < 350) {
            return intensityColors[5];
        } else {
            return intensityColors[6]; // Darkest grey for high counts
        }
    }

    // Generate background and border colors based on the number of weekly cases
    var backgroundColors = weeklyCounts.map(count => getColorByCases(count));
    var borderColors = backgroundColors.map(color => color.replace('0.6', '0.7')); // Adjust border opacity if needed

    var weeklyCasesChart = new Chart(ctxWeekly, {
        type: 'bar',
        data: {
            labels: weeks,
            datasets: [{
                label: 'Weekly Cases',
                data: weeklyCounts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 50,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Week'
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

// Function to initialize the Daily Cases Chart
function initDailyChart(days, dailyCounts) {
    var ctxDaily = document.getElementById('dailyCasesChart').getContext('2d');

    var dailyCasesChart = new Chart(ctxDaily, {
        type: 'bar',
        data: {
            labels: days,
            datasets: [{
                label: 'Daily Cases',
                data: dailyCounts,
                backgroundColor: 'rgba(0, 123, 255, 0.6)',
                borderColor: 'rgba(0, 123, 255, 0.7)',
                borderWidth: 1,
                borderRadius: 50,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Day'
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
        }
    });
}

// Function to initialize the Quarterly Cases Chart
function initQuarterlyChart(quarters, quarterlyCounts) {
    var ctxQuarterly = document.getElementById('quarterlyCasesChart').getContext('2d');

    var quarterlyCasesChart = new Chart(ctxQuarterly, {
        type: 'bar',
        data: {
            labels: quarters,
            datasets: [{
                label: 'Quarterly Cases',
                data: quarterlyCounts,
                backgroundColor: 'rgba(0, 123, 255, 0.6)',
                borderColor: 'rgba(0, 123, 255, 0.7)',
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
                        text: 'Year'
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

// Function to initialize the Annual Cases Chart
function initAnnualChart(years, annualCounts) {
    var ctxAnnual = document.getElementById('annualCasesChart').getContext('2d');

    var annualCasesChart = new Chart(ctxAnnual, {
        type: 'bar',
        data: {
            labels: years,
            datasets: [{
                label: 'Annual Cases',
                data: annualCounts,
                backgroundColor: 'rgba(0, 123, 255, 0.6)',
                borderColor: 'rgba(0, 123, 255, 0.7)',
                borderWidth: 1,
                borderRadius: 50,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
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
        plugins: [ChartDataLabels] // Add ChartDataLabels plugin
    });
}


// This function will be called to initialize charts
function initializeCharts(data) {
    initMonthlyChart(data.months, data.caseCounts);
    initWeeklyChart(data.weeks, data.weeklyCounts);
    initDailyChart(data.days, data.dailyCounts);
    initQuarterlyChart(data.quarters, data.quarterlyCounts);
    initAnnualChart(data.years, data.annualCounts);
}
