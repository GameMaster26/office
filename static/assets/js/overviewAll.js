// Open the modal when the "Download PDFs" button is clicked
document.getElementById("downloadAllPDFs").addEventListener("click", function () {
    const downloadModal = new bootstrap.Modal(document.getElementById('downloadModal'));
    downloadModal.show();
});

// Functions for downloading specific PDFs
function downloadMunicipalityPDF() {
    const chartElement = document.getElementById("municipalityChart");
    const dateRange = document.getElementById("date-range-display").textContent;
    
    
    if (chartElement) {
        var imageData = chartElement.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        var doc = new jsPDF('l', 'mm', 'a4'); // Landscape orientation

        const pageWidth = 297;  // A4 width in mm (landscape)
        const pageHeight = 210; // A4 height in mm (landscape)
        
        const imgWidth = 250;   // Width of the image (adjustable)
        const imgHeight = 120;  // Height of the image (adjustable)

        const xOffset = (pageWidth - imgWidth) / 2; 
        const yOffset = (pageHeight - imgHeight) / 2; // Adjusted to move closer to text

        // Add municipality name at the top-left corner
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text(`Animal Bite Treatment Center: ${municipality}`, 10,20); // Top-left at (10, 15)

        // Add the main title
        doc.setFontSize(14);
        doc.text('Municipality Distribution of Cases', pageWidth / 2, 20, { align: 'center' });
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 23); // Date range directly below the title

        

        // Add the "Prepared by" section to the Municipality PDF
        doc.setFont("helvetica", "normal");  // Ensure "Prepared by" is in regular font
        doc.setFontSize(12);

        // Calculate the X position to center the text
        const centerX = pageWidth / 2;

        // Adjust Y position to move the "Prepared by" section higher
        const higherY = pageHeight - 30;  // Position it 30mm above the bottom (you can adjust this further)

        // "Prepared by" centered at the new position
        doc.text('Prepared by: ', centerX, higherY, { align: 'center' });  // Center "Prepared by:"

        // Set bold for the name
        doc.setFont("helvetica", "bold");  // Make fname and lname bold
        const nameText = `${fname} ${lname}`;
        doc.text(nameText, centerX, higherY + 8, { align: 'center' });  // Add the name 5mm below "Prepared by"




        // Add the image (chart)
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF with the specified name
        doc.save('Municipality Chart.pdf');
    } else {
        console.error("Chart element not found");
    }
}

function downloadGenderPDF() {
    const chartElement = document.getElementById("genderChart");
    const dateRange = document.getElementById("date-range-display").textContent;

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
        const yOffset = (pageHeight - imgHeight) / 2; // Adjusted to move closer to text

        // Add municipality name at the top-left corner
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text(`Animal Bite Treatment Center: ${municipality}`, 10,20); // Top-left at (10, 15)

        // Add the title
        doc.setFontSize(18);
        doc.text('Gender Distribution of Cases', pageWidth / 2, 20, { align: 'center' });
        
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth / 2.8, 23); // Date range directly below the title

        // Add the total male and female counts dynamically
        doc.setFontSize(14);
        doc.text(`Total Males: ${maleCount}`, 20, 85); // Position for Male count
        doc.text(`Total Females: ${femaleCount}`, 20, 95); // Position for Female count

        // Add the "Prepared by" section to the Municipality PDF
        doc.setFont("helvetica", "normal");  // Ensure "Prepared by" is in regular font
        doc.setFontSize(12);

        // Calculate the X position to center the text
        const centerX = pageWidth / 2;

        // Adjust Y position to move the "Prepared by" section higher
        const higherY = pageHeight - 30;  // Position it 30mm above the bottom (you can adjust this further)

        // "Prepared by" centered at the new position
        doc.text('Prepared by: ', centerX, higherY, { align: 'center' });  // Center "Prepared by:"

        // Set bold for the name
        doc.setFont("helvetica", "bold");  // Make fname and lname bold
        const nameText = `${fname} ${lname}`;
        doc.text(nameText, centerX, higherY + 8, { align: 'center' });  // Add the name 5mm below "Prepared by"

        // Add the image
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        // Save the PDF
        doc.save('Sex Distribution.pdf');
    } else {
        console.error("Chart element not found");
    }
}

function downloadAnimalPDF() {
    const chartElement = document.getElementById("animalChart");
    const dateRange = document.getElementById("date-range-display").textContent;

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
        const imageData = chartElement.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF('l', 'mm', 'a4');
        // Page dimensions for A4 landscape
        const pageWidth = 297; 
        const pageHeight = 210; 

        // Define image size
        const imgWidth = 120; 
        const imgHeight = 110; 

        // Calculate positions to center the image
        const xOffset = (pageWidth - imgWidth) / 2; 
        const yOffset = (pageHeight - imgHeight) / 2; // Adjusted to move closer to text

        // Add municipality name at the top-left corner
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text(`Animal Bite Treatment Center: ${municipality}`, 10,20); // Top-left at (10, 15)

        // Add the title
        doc.setFontSize(18);
        doc.text('Animal Distribution of Cases', pageWidth / 2, 20, { align: 'center' });
        
        // Add the date range below the title
        doc.setFontSize(12);
        doc.text(dateRange, pageWidth /2.8, 23); // Date range directly below the title

        // Add the total dog, cat counts dynamically
        doc.setFontSize(14);
        doc.text(`Dog: ${dogCount}`, 20, 55); // Position for Dog count
        doc.text(`Cat: ${catCount}`, 20, 65); // Position for Cat count

        // Add the "Prepared by" section to the Municipality PDF
        doc.setFont("helvetica", "normal");  // Ensure "Prepared by" is in regular font
        doc.setFontSize(12);

        // Calculate the X position to center the text
        const centerX = pageWidth / 2;

        // Adjust Y position to move the "Prepared by" section higher
        const higherY = pageHeight - 30;  // Position it 30mm above the bottom (you can adjust this further)

        // "Prepared by" centered at the new position
        doc.text('Prepared by: ', centerX, higherY, { align: 'center' });  // Center "Prepared by:"

        // Set bold for the name
        doc.setFont("helvetica", "bold");  // Make fname and lname bold
        const nameText = `${fname} ${lname}`;
        doc.text(nameText, centerX, higherY + 8, { align: 'center' });  // Add the name 5mm below "Prepared by"

        // Add specific animals under "Others" dynamically
        let yOffsetOthers = 75; // Start from the position after Cats


        otherCounts.forEach(function(animal, index) {
            doc.text(`${animal.animal}: ${animal.count}`, 20, yOffsetOthers); // Display each specific animal
            yOffsetOthers += 10; // Adjust vertical space for each animal
        });

        // Add the image
        doc.addImage(imageData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

        doc.save('Animal Distribution.pdf');
    }
    else {
        console.error("Chart element not found");
    }
}

function downloadAllPDFs() {
    const dateRange = document.getElementById("date-range-display").textContent;
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4');
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
    // Add the "Prepared by" section to the Municipality PDF
    doc.setFontSize(12);
    doc.text(`Prepared by: ${fname} ${lname}`, 20, pageHeight - 10)

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
        doc.text(`Dog: ${dogCount}`, pageWidth - imgWidth - 50, animalChartPos.y + imgHeight - 45); // Raised higher by 20 units
        doc.text(`Cat: ${catCount}`, pageWidth - imgWidth - 50, animalChartPos.y + imgHeight - 35); // Raised higher by 20 units

        // Add specific animals under "Others" dynamically
        const otherCounts = [];  // This will hold specific animals and their counts
        for (let i = 2; i < animalLabels.length; i++) {
            otherCounts.push({ animal: animalLabels[i], count: animalData[i] });
        }

        // Add "Other Animals" section and list the animals with their counts
        let yOffsetOthers = animalChartPos.y + imgHeight - 25; // Start from the position after Dog and Cat

        otherCounts.forEach(function(animal, index) {
            doc.text(`${animal.animal}: ${animal.count}`, pageWidth - imgWidth - 50, yOffsetOthers); // Display each specific animal
            yOffsetOthers += 10; // Adjust vertical space for each animal
        });
    }
    doc.save('Case Distribution Summary.pdf');
}

document.getElementById("confirmDownload").addEventListener("click", function () {
    const selectedCharts = [];
    const form = document.getElementById("chartSelectionForm");

    // Log form elements
    console.log('Form elements:', form);

    // Check each checkbox and add selected values to an array
    form.querySelectorAll("input[type=checkbox]:checked").forEach((checkbox) => {
        selectedCharts.push(checkbox.value);
    });

    console.log("Selected charts:", selectedCharts);

    if (selectedCharts.length === 0) {
        alert("Please select at least one chart to download.");
        return;
    }

    if (selectedCharts.includes("all")) {
        console.log("Downloading all charts...");
        downloadAllPDFs();
        bootstrap.Modal.getInstance(document.getElementById('downloadModal')).hide();
        return;
    }

    selectedCharts.forEach((chart) => {
        console.log("Downloading chart:", chart);
        if (chart === "municipality") {
            downloadMunicipalityPDF();
        } else if (chart === "gender") {
            downloadGenderPDF();
        } else if (chart === "animal") {
            downloadAnimalPDF();
        }
    });

    // Close the modal
    bootstrap.Modal.getInstance(document.getElementById('downloadModal')).hide();
});

