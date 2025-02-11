document.addEventListener('DOMContentLoaded', function() {
    const municipalitySelects = document.querySelectorAll('.municipality-select');
    municipalitySelects.forEach(select => {
        select.addEventListener('change', function() {
            const muniId = this.value;
            const barangaySelect = this.closest('fieldset').querySelector('.barangay-select');
            fetch(`/admin/your_app_name/get_barangays/?muni_id=${muniId}`)
                .then(response => response.json())
                .then(data => {
                    barangaySelect.innerHTML = '';
                    data.forEach(barangay => {
                        const option = document.createElement('option');
                        option.value = barangay.id;
                        option.textContent = barangay.brgy_name;
                        barangaySelect.appendChild(option);
                    });
                });
        });
    });
});
