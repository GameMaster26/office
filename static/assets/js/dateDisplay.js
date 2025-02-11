document.addEventListener('DOMContentLoaded', function () {
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const dateRangeDisplay = document.getElementById('date-range-display');

    function updateDateRangeDisplay() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        // Update the date range display
        if (startDate && endDate) {
            const formattedStartDate = new Date(startDate).toLocaleDateString();
            const formattedEndDate = new Date(endDate).toLocaleDateString();
            dateRangeDisplay.innerHTML = `
                <h5 class="text-primary">Date Range: ${formattedStartDate} to ${formattedEndDate}</h5>
            `;
        } else {
            // Get the current date
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear();

            // Create the default start date as January 1st of the current year
            const defaultStartDate = new Date(currentYear, 0, 1); // January 1st of the current year
            const formattedStartDate = defaultStartDate.toLocaleDateString();
            const formattedEndDate = currentDate.toLocaleDateString(); // Current date as end date

            dateRangeDisplay.innerHTML = `
                <h5 class="text-primary">${formattedStartDate} to ${formattedEndDate}</h5>
            `;
        }
    }

    // Add event listeners to update the display when dates are changed
    startDateInput.addEventListener('change', updateDateRangeDisplay);
    endDateInput.addEventListener('change', updateDateRangeDisplay);

    // Initial update on page load
    updateDateRangeDisplay();
});
