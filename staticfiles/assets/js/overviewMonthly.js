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

document.getElementById("downloadPDF").addEventListener("click", function () {
    // Identify the currently visible chart section
    const visibleChart = document.querySelector(".chart-container:not([style*='display: none']) canvas");

    if (visibleChart) {
        const imageData = visibleChart.toDataURL("image/png");

        // Create jsPDF instance for landscape mode
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF("l", "mm", "a4");

        // Page dimensions for A4 landscape
        const pageWidth = 297; // A4 width in mm
        const pageHeight = 210; // A4 height in mm

        // Image size (adjust as needed)
        const imgWidth = 250; // Width of the image (adjustable)
        const imgHeight = 120; // Height of the image (adjustable)

        // Calculate positions to center the image
        const xOffset = (pageWidth - imgWidth) / 2; // Center horizontally
        const yOffset = (pageHeight - imgHeight) / 2.5; // Center vertically, adjusted for title spacing

        // Add the title dynamically from the visible chart's title
        const title = visibleChart.closest(".chart-container").querySelector("h2").textContent;
        doc.setFontSize(18);
        doc.text(title, pageWidth / 2, 15, { align: "center" });

        // Add the treatment center to the top-left corner
        const treatmentCenter = "{{ treatment_center }}"; // Using the passed `treatment_center` value
        doc.setFontSize(14);
        doc.text(treatmentCenter, 10, 10); // Position at top-left (10mm from left, 10mm from top)

        // Add the date range below the title (centered)
        const dateRange = document.getElementById("date-range-display").textContent; // Get the date range text
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 20);

        // Add the chart image (centered below the title and date range)
        doc.addImage(imageData, "PNG", xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF with the specified name
        doc.save(`${title}.pdf`);
    } else {
        console.error("No visible chart found.");
    }
});
