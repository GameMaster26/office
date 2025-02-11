// doctor_form.js
document.addEventListener('DOMContentLoaded', function() {
    const municipalityField = document.getElementById('id_muni_id');
    const barangayField = document.getElementById('id_brgy_id');

    municipalityField.addEventListener('change', function() {
        const municipalityId = this.value;

        // Clear current options in barangay field
        barangayField.innerHTML = '<option value="">---------</option>';

        if (municipalityId) {
            // Fetch barangays for the selected municipality via Django admin’s related model URLs
            fetch(`/admin/yourapp/barangay/?muni_id=${municipalityId}&json=true`)
                .then(response => response.json())
                .then(data => {
                    data.results.forEach(function(item) {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = item.text;
                        barangayField.appendChild(option);
                    });
                });
        }
    });
});
