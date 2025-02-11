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
    const otherAnimals = []; // To store names of animals in "Others" category

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
    const chartLabels = [];
    const chartData = [];
    const chartColors = [];
    const chartBorderColors = [];

    // Add data for Dog and Cat
    ['Dog', 'Cat', 'Others'].forEach((key) => {
        if (groupedData[key] > 0 || key === 'Others') {
            chartLabels.push(key);
            chartData.push(groupedData[key]);
            chartColors.push(
                key === 'Dog' ? 'rgba(255, 165, 0, 1)' :
                key === 'Cat' ? 'rgba(255, 0, 0, 1)' :
                'rgba(128, 128, 128, 1)' // "Others" color remains
            );
            chartBorderColors.push(
                key === 'Dog' ? 'rgba(255, 165, 0, 1)' :
                key === 'Cat' ? 'rgba(255, 0, 0, 1)' :
                'rgba(128, 128, 128, 1)'
            );
        }
    });

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
                backgroundColor: chartColors,
                borderColor: chartBorderColors,
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        generateLabels: function(chart) {
                            const labels = chart.data.labels.map((label, i) => {
                                const meta = chart.getDatasetMeta(0);
                                const hidden = meta.data[i].hidden;
                                return {
                                    text: label,
                                    fillStyle: chart.data.datasets[0].backgroundColor[i],
                                    strokeStyle: chart.data.datasets[0].borderColor[i],
                                    hidden: false,
                                    index: i
                                };
                            });

                            // Ensure Others is always in the legend, even if its value is 0
                            if (!labels.some(label => label.text === 'Others')) {
                                labels.push({
                                    text: 'Others',
                                    fillStyle: 'rgba(128, 128, 128, 1)',
                                    strokeStyle: 'rgba(128, 128, 128, 1)',
                                    hidden: false
                                });
                            }

                            return labels;
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        // Custom tooltip to show details when hovering "Others"
                        label: function(context) {
                            if (context.label === 'Others') {
                                return othersTooltipText || 'Others: 0'; // Show details or "Others: 0"
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

/* 
document.getElementById("downloadMunicipalityPDF").addEventListener("click", function() {
    const chartElement = document.getElementById("municipalityChart");
    const dateRange = document.getElementById("date-range-display").textContent; // Get the date range text

    if (chartElement) {
        var imageData = chartElement.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        var doc = new jsPDF('l', 'mm', 'a4'); // Landscape orientation

        const pageWidth = 297;  // A4 width in mm (landscape)
        const pageHeight = 210; // A4 height in mm (landscape)
        
        const imgWidth = 250;   // Width of the image (adjustable)
        const imgHeight = 120;  // Height of the image (adjustable)

        const xOffset = (pageWidth - imgWidth) / 2; 
        const yOffset = (pageHeight - imgHeight) / 2.5; // Adjusted to move closer to text

        // Add the main title
        doc.setFontSize(18);
        doc.text('Municipality Distribution of Cases', pageWidth / 2, 15, { align: 'center' });
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 18); // Date range directly below the title

        // Add the image (chart)
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF with the specified name
        doc.save('Municipality Chart.pdf');
    } else {
        console.error("Chart element not found");
    }
});



document.getElementById("downloadGenderPDF").addEventListener("click", function() {
    const chartElement = document.getElementById("genderChart");
    const dateRange = document.getElementById("date-range-display").textContent; // Get the date range text

    // Get the total number of males and females dynamically from the `dataGender`
    const maleCount = genderData[0];  // Assuming the first label is 'Male'
    const femaleCount = genderData[1]; // Assuming the second label is 'Female'

    if (chartElement) {
        var imageData = chartElement.toDataURL('image/png');
        
        const { jsPDF } = window.jspdf; 
        var doc = new jsPDF('l', 'mm', 'a4'); // 'l' for landscape, 'mm' for millimeters, 'a4' size

        // Page dimensions for A4 landscape
        const pageWidth = 297; 
        const pageHeight = 210; 

        // Define image size
        const imgWidth = 120; 
        const imgHeight = 110; 

        // Calculate positions to center the image
        const xOffset = (pageWidth - imgWidth) / 2; 
        const yOffset = (pageHeight - imgHeight) / 2.5; // Adjusted to move closer to text

        // Add the title
        doc.setFontSize(18);
        doc.text('Gender Distribution of Cases', pageWidth / 2, 15, { align: 'center' });
        
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 18); // Date range directly below the title

        // Add the total male and female counts dynamically
        doc.setFontSize(14);
        doc.text(`Total Males: ${maleCount}`, 20, 85); // Position for Male count
        doc.text(`Total Females: ${femaleCount}`, 20, 95); // Position for Female count

        // Add the image
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF
        doc.save('Sex Distribution.pdf');
    } else {
        console.error("Chart element not found");
    }
});



document.getElementById("downloadAnimalPDF").addEventListener("click", function() {
    const chartElement = document.getElementById("animalChart");
    const dateRange = document.getElementById("date-range-display").textContent; // Get the date range text

    // Group animals into Dog, Cat, and Others with their specific names
    const dogCount = animalData[0];  // Assuming 'Dog' is the first label
    const catCount = animalData[1];  // Assuming 'Cat' is the second label
    const otherCounts = [];  // This will hold specific animals and their counts

    // Start from the 3rd label and find all others
    for (let i = 2; i < animalLabels.length; i++) {
        otherCounts.push({ animal: animalLabels[i], count: animalData[i] });
    }

    // Now calculate the total for 'Others'
    const otherTotal = otherCounts.reduce((acc, curr) => acc + curr.count, 0); 

    if (chartElement) {
        var imageData = chartElement.toDataURL('image/png');
        
        const { jsPDF } = window.jspdf; 
        var doc = new jsPDF('l', 'mm', 'a4'); // 'l' for landscape, 'mm' for millimeters, 'a4' size

        // Page dimensions for A4 landscape
        const pageWidth = 297; 
        const pageHeight = 210; 

        // Define image size
        const imgWidth = 120; 
        const imgHeight = 110; 

        // Calculate positions to center the image
        const xOffset = (pageWidth - imgWidth) / 2; 
        const yOffset = (pageHeight - imgHeight) / 2.5; // Adjusted to move closer to text

        // Add the title
        doc.setFontSize(18);
        doc.text('Animal Distribution of Cases', pageWidth / 2, 15, { align: 'center' });
        
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 18); // Date range directly below the title

        // Add the total dog, cat counts dynamically
        doc.setFontSize(14);
        doc.text(`Dog: ${dogCount}`, 20, 55); // Position for Dog count
        doc.text(`Cat: ${catCount}`, 20, 65); // Position for Cat count

        // Add specific animals under "Others" dynamically
        let yOffsetOthers = 75; // Start from the position after Cats


        otherCounts.forEach(function(animal, index) {
            doc.text(`${animal.animal}: ${animal.count}`, 20, yOffsetOthers); // Display each specific animal
            yOffsetOthers += 10; // Adjust vertical space for each animal
        });

        // Add the image
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF
        doc.save('Animal Distribution.pdf');
    } else {
        console.error("Chart element not found");
    }
});



document.getElementById("downloadAllPDFs").addEventListener("click", function () {
    const dateRange = document.getElementById("date-range-display").textContent; // Get the date range text
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // Landscape orientation

    const pageWidth = 297;  // A4 width in mm (landscape)
    const pageHeight = 210; // A4 height in mm (landscape)

    // Chart dimensions
    const municipalityImgWidth = 150;
    const municipalityImgHeight = 70;

    const imgWidth = 70;    // Gender and Animal charts' width
    const imgHeight = 65;   // Gender and Animal charts' height

    // Positioning for elements
    const dateRangePos = { x: 5, y: 10 }; // Top-left corner
    const municipalityChartPos = { x: (pageWidth - municipalityImgWidth) / 2, y: 20 }; // Centered at the top
    const genderChartPos = { x: 50, y: pageHeight - imgHeight - 30 }; // Bottom-left (shifted right)
    const animalChartPos = { x: pageWidth - imgWidth - 20, y: pageHeight - imgHeight - 30 }; // Bottom-right

    // Gender and Animal Data
    const maleCount = genderData[0]; // Assuming the first label is 'Male'
    const femaleCount = genderData[1]; // Assuming the second label is 'Female'

    const dogCount = animalData[0]; // Assuming 'Dog' is the first label
    const catCount = animalData[1]; // Assuming 'Cat' is the second label

    // Add date range at the top-left
    doc.setFontSize(12);
    doc.text(dateRange, dateRangePos.x, dateRangePos.y); // Date range top-left

    // Add Municipality Chart
    const municipalityChart = document.getElementById("municipalityChart");
    if (municipalityChart) {
        const municipalityImage = municipalityChart.toDataURL('image/png');
        doc.setFontSize(14);
        doc.text("Municipality Distribution of Cases", pageWidth / 2, 15, { align: 'center' });
        doc.addImage(municipalityImage, 'PNG', municipalityChartPos.x, municipalityChartPos.y, municipalityImgWidth, municipalityImgHeight);
    }

    // Add Gender Chart
    const genderChart = document.getElementById("genderChart");
    if (genderChart) {
        const genderImage = genderChart.toDataURL('image/png');
        doc.setFontSize(14);
        doc.text("Gender Distribution", genderChartPos.x + imgWidth / 2, genderChartPos.y - 5, { align: 'center' }); // Adjusted for totals
        doc.addImage(genderImage, 'PNG', genderChartPos.x, genderChartPos.y, imgWidth, imgHeight);

        // Add totals for gender on the left side (raised even higher)
        doc.setFontSize(12);
        doc.text(`Male: ${maleCount}`, 20, genderChartPos.y + imgHeight - 45); // Raised higher by 20 units
        doc.text(`Female: ${femaleCount}`, 20, genderChartPos.y + imgHeight - 35); // Raised higher by 20 units
    }

    // Add Animal Chart
    const animalChart = document.getElementById("animalChart");
    if (animalChart) {
        const animalImage = animalChart.toDataURL('image/png');
        doc.setFontSize(14);
        doc.text("Animal Source of Exposure", animalChartPos.x + imgWidth / 2, animalChartPos.y - 5, { align: 'center' }); // Adjusted for totals
        doc.addImage(animalImage, 'PNG', animalChartPos.x, animalChartPos.y, imgWidth, imgHeight);

        // Add totals for animals on the right side (raised higher by 20 units)
        doc.setFontSize(12);
        doc.text(`Dog: ${dogCount}`, pageWidth - imgWidth - 50, animalChartPos.y + imgHeight - 55); // Raised higher by 20 units
        doc.text(`Cat: ${catCount}`, pageWidth - imgWidth - 50, animalChartPos.y + imgHeight - 45); // Raised higher by 20 units

        // Add specific animals under "Others" dynamically
        const otherCounts = [];  // This will hold specific animals and their counts
        for (let i = 2; i < animalLabels.length; i++) {
            otherCounts.push({ animal: animalLabels[i], count: animalData[i] });
        }

        // Add "Other Animals" section and list the animals with their counts
        let yOffsetOthers = animalChartPos.y + imgHeight - 35; // Start from the position after Dog and Cat

        otherCounts.forEach(function(animal, index) {
            doc.text(`${animal.animal}: ${animal.count}`, pageWidth - imgWidth - 50, yOffsetOthers); // Display each specific animal
            yOffsetOthers += 10; // Adjust vertical space for each animal
        });
    }

    // Save the final PDF with all charts on one page
    doc.save("Case Distribution Summary");
}); */

