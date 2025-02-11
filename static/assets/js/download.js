// Function to update reporting period
function updateReportingPeriod() {
    var startMonth = $('#startMonth').val();
    var endMonth = $('#endMonth').val();
    
    // Get the current year
    var currentYear = new Date().getFullYear();

    // Update the reporting period based on selected months
    if (startMonth && endMonth) {
        // If start and end months are the same
        if (startMonth === endMonth) {
            $("#reportingPeriod").html("<b>Reporting Period: " + startMonth + " - " + currentYear + "</b>");
        } else {
            $("#reportingPeriod").html("<b>Reporting Period: " + startMonth + " - " + endMonth + " " + currentYear +"</b>");
        }
    } else if (startMonth) {
        $("#reportingPeriod").html("<b>Reporting Period: " + startMonth + " - " + currentYear + "</b>");
    } else if (endMonth) {
        $("#reportingPeriod").html("<b>Reporting Period: " + endMonth + " " + currentYear + "</b>");
    } else {
        $("#reportingPeriod").html("<b>Reporting Period: " + currentYear + "</b>");
    }
}

// Update reporting period and submit form when start or end month changes
$('#startMonth, #endMonth').change(function() {
    updateReportingPeriod();
    $('form.filter-container').submit();  // Submit the form to update the table
});

// Initial update of reporting period
$(document).ready(function() {
    updateReportingPeriod(); // Update initially when the document is ready
});