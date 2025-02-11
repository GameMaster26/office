document.addEventListener('DOMContentLoaded', function () {
    if (typeof L !== 'undefined') {
        var leafletMap = document.querySelector('.leaflet-widget');

        if (leafletMap) {
            var map = L.map(leafletMap.id).setView([11.555813, 124.414872], 13);  // Default coordinates
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
        }
    } else {
        console.error('Leaflet is not loaded.');
    }
});
