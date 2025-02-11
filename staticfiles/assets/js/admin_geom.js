document.addEventListener('DOMContentLoaded', function () {
    function loadmap() {
        if (typeof L !== 'undefined') {
            var djoptions = {
                "srid": null,
                "extent": [[-90, -180], [90, 180]],
                "fitextent": true,
                "center": [11.64, 124.4642],
                "zoom": 10,
                "precision": 6,
                "minzoom": 3,
                "maxzoom": 18,
                "layers": [["Mapbox", "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {"attribution": "&copy; OpenStreetMap contributors"}]],
                "overlays": [],
                "attributionprefix": null,
                "scale": "metric",
                "minimap": false,
                "resetview": true,
                "tilesextent": []
            },
            options = {djoptions: djoptions, initfunc: loadmap, globals: false, callback: id_histories___prefix___geom_map_callback},
            map = L.map('id_histories-__prefix__-geom-map', options);
        } else {
            console.error('Leaflet library is not loaded');
        }
    }

    loadmap();
});
