document.addEventListener("DOMContentLoaded", function () {
    const mapElements = document.querySelectorAll('textarea[data-muni-boundary]');

    mapElements.forEach(function (element) {
        const boundary = element.getAttribute('data-muni-boundary');
        
        if (boundary) {
            // Parse the boundary GeoJSON
            const boundaryGeoJson = JSON.parse(boundary);

            // Find the leaflet map instance
            const mapId = element.id + '_map';  // Adjust based on how the map ID is generated
            const map = L.Map.instances.find(instance => instance._container.id === mapId);

            if (map) {
                // Fit the map view to the municipality boundary
                const boundaryLayer = L.geoJSON(boundaryGeoJson);
                map.fitBounds(boundaryLayer.getBounds());
            }
        }
    });
});
