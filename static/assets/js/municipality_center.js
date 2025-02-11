    document.addEventListener('DOMContentLoaded', function () {
        const municipalitySelect = document.querySelector('.municipality-select');

        if (municipalitySelect) {
            municipalitySelect.addEventListener('change', function () {
                const muniId = this.value;  // Get selected municipality ID
                if (muniId) {
                    fetch(`/get-municipality-boundary/?muni_id=${muniId}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.center) {
                                // Use the returned center coordinates to update your Leaflet map
                                const center = data.center;
                                const zoom = data.zoom || 12;  // Default zoom if not provided
                                // Assuming you have a function to set the center and zoom level of your Leaflet map
                                setMapCenter(center[0], center[1], zoom);
                            } else {
                                console.error('Invalid response', data);
                            }
                        })
                        .catch(error => console.error('Error fetching municipality boundary:', error));
                }
            });
        }
    });

    // Assuming you have a function to set the map center
    function setMapCenter(lat, lng, zoom) {
        // Replace with your actual Leaflet map instance and logic
        id_geom-div-map.setView([lat, lng], zoom);
    }
