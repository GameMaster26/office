// Intensity colors for case counts
const intensityColors = [
    '#6DA9FF', '#6DA9FF', '#3399FF', '#3399FF', '#007BFF', '#007BFF', 
    '#0069D9', '#0069D9', '#0056B3', '#0056B3', '#004085', '#004085'
];

// Function to get color based on case count
function getColorByCases(count, isWeekly = false) {
    if (count < 50) return intensityColors[0];
    if (count < 100) return intensityColors[1];
    if (count < 200) return intensityColors[2];
    if (count < 300) return intensityColors[3];
    if (count < 400) return intensityColors[4];
    if (count < 500) return intensityColors[5];
    if (isWeekly && count < 600) return intensityColors[6];  // Adjust if weekly cases need different thresholds
    return intensityColors[7];  // Darkest color for higher cases
}

// Initialize charts with appropriate data
function initCasesChart(chartId, labels, caseCounts, chartType = 'bar', borderRadius = 30, isWeekly = false) {
    const ctx = document.getElementById(chartId).getContext('2d');
    const backgroundColors = caseCounts.map(count => getColorByCases(count, isWeekly));
    const borderColors = backgroundColors.map(color => color.replace('0.6', '0.7'));

    return new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: `${chartId.replace('CasesChart', '')} Cases`,
                data: caseCounts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: borderRadius,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: chartId.replace('CasesChart', ' Time Period') } },
                y: { beginAtZero: true, title: { display: true, text: 'Number of Cases' } }
            }
        }
    });
}

// Monthly Cases Chart
function initMonthlyCasesChart(months, caseCounts) {
    initCasesChart('monthlyCasesChart', months, caseCounts, 'bar', 30);
}

// Weekly Cases Chart
function initWeeklyCasesChart(weeks, weeklyCounts) {
    initCasesChart('weeklyCasesChart', weeks, weeklyCounts, 'bar', 50, true);
}

// Daily Cases Chart
function initDailyCasesChart(days, dailyCounts) {
    initCasesChart('dailyCasesChart', days, dailyCounts, 'bar', 50);
}

// Quarterly Cases Chart
function initQuarterlyCasesChart(quarters, quarterlyCounts) {
    initCasesChart('quarterlyCasesChart', quarters, quarterlyCounts, 'bar', 30);
}

// Annual Cases Chart
function initAnnualCasesChart(years, annualCounts) {
    initCasesChart('annualCasesChart', years, annualCounts, 'bar', 50);
}

// Scroll function to smooth scroll to a target element
function smoothScroll(targetId) {
    document.getElementById(targetId).scrollIntoView({ 
        behavior: 'smooth',
        block: 'center',
        inline: 'nearest' 
    });
}

// Scroll Event Listeners
document.getElementById('scrollToGender').addEventListener('click', () => smoothScroll('scrollGender'));
document.getElementById('scrollToAnimal').addEventListener('click', () => smoothScroll('scrollAnimal'));
document.getElementById('scrollToWeeklyCases').addEventListener('click', () => smoothScroll('monthlyCasesScroll'));
document.getElementById('scrollToMunicipality').addEventListener('click', () => smoothScroll('distributionMunicipality'));

// Toggle sections logic
function toggleSections(showSectionId) {
    const sections = ['weeklyCasesSection', 'monthlyCasesSection', 'quarterlyCasesSection', 'annualCasesSection'];
    sections.forEach(section => {
        const sectionElement = document.getElementById(section);
        if (section === showSectionId) {
            sectionElement.style.display = 'block';
        } else {
            sectionElement.style.display = 'none';
        }
    });
}

// Section Toggle Event Listeners
document.getElementById('showWeekly').addEventListener('click', () => toggleSections('weeklyCasesSection'));
document.getElementById('showMonthly').addEventListener('click', () => toggleSections('monthlyCasesSection'));
document.getElementById('showQuarterly').addEventListener('click', () => toggleSections('quarterlyCasesSection'));
document.getElementById('showAnnual').addEventListener('click', () => toggleSections('annualCasesSection'));

// Initialize all the charts when page loads with the data passed from Django
document.addEventListener('DOMContentLoaded', () => {
    const months = {{ months|safe }};
    const caseCounts = {{ case_counts|safe }};
    const weeks = {{ weeks|safe }};
    const weeklyCounts = {{ weekly_case_counts|safe }};
    const days = {{ days|safe }};
    const dailyCounts = {{ daily_case_counts|safe }};
    const quarters = {{ quarters|safe }};
    const quarterlyCounts = {{ quarterly_case_counts|safe }};
    const years = {{ years|safe }};
    const annualCounts = {{ annual_case_counts|safe }};
    
    // Initialize charts with provided data
    initMonthlyCasesChart(months, caseCounts);
    initWeeklyCasesChart(weeks, weeklyCounts);
    initDailyCasesChart(days, dailyCounts);
    initQuarterlyCasesChart(quarters, quarterlyCounts);
    initAnnualCasesChart(years, annualCounts);
});
