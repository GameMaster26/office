document.addEventListener('DOMContentLoaded', function() {
    const muniSelect = document.getElementById('id_muni_id');
    const brgySelect = document.getElementById('id_brgy_id');
    
    console.log(brgySelect);

    if (muniSelect && brgySelect) {
        muniSelect.addEventListener('change', function() {
            const muniId = muniSelect.value;

            if (muniId) {
                fetch(`/admin/load-barangays/?muni_id=${muniId}`)
                    .then(response => response.json())
                    .then(data => {
                        brgySelect.innerHTML = '<option value="">---------</option>';
                        data.barangays.forEach(brgy => {
                            const option = document.createElement('option');
                            option.value = brgy.id;
                            option.text = brgy.name;
                            brgySelect.appendChild(option);
                        });
                    });
            } else {
                brgySelect.innerHTML = '<option value="">---------</option>';
            }
        });
    }
});
