window.onload = init;

function init() {
    const totalCasesRabies = document.getElementById('total-rabies-data');
    const totalRabibesCases = parseInt(totalCasesRabies.getAttribute('data-rabies-cases'), 10);
    
    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    const Light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
    });

    const maxBounds = L.latLngBounds(
        L.latLng(11.358607609157232, 123.91744935882099),
        L.latLng(11.897821676214718, 125.01560057070333)
    );

    const mymap = L.map('choropleth', {
        center: [11.6400, 124.4642],
        zoom: 11,
        minZoom: 10,
        layers: [Light],
        zoomControl: false,
        gestureHandling: true,
        dragging: true,
    }).setMaxBounds(maxBounds);

    L.control.zoom({
        position: 'bottomright'
    }).addTo(mymap);

    function highlightFeature(e) {
        var layer = e.target;
        layer.setStyle({
            weight: 1,
            color: '#FF0000',
            dashArray: '',
            fillOpacity: 0.7
        });
        if (!L.Browser.ie && !L.Browser.edge) {
            layer.bringToFront();
        }
    
        var patientCount = densityData[layer.feature.properties.pk];
        var patientDisplay = (patientCount && patientCount > 0) ? patientCount : "No Patient";
    
        layer.bindTooltip(
            "<b>Barangay: " + layer.feature.properties.brgy_name + "</b>" + 
            "<br><span style='color:red;'>Patients: " + patientDisplay + "</span>"
        )
        .openTooltip()
        .setOffset([20, 20]);
    }
    
    function resetHighlight(e) {
        geojson.resetStyle(e.target);
        e.target.closeTooltip();
    }
    
    function zoomToFeature(e) {
        mymap.fitBounds(e.target.getBounds());
    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });

        var patientCount = densityData[feature.properties.pk];
        var patientText = (patientCount > 0) ? "Patients: " + patientCount : "No Patient";

        layer.bindTooltip(
            "<b>Barangay: " + feature.properties.brgy_name + "</b>" +
            "<br><span style='color:red;'>Patients: " + patientCount + "</span>"
        );
    }

    var geojson = L.geoJson(biliranData, {
        style: function(feature) {
            var density = densityData[feature.properties.pk] || 0;
            return {
                color: 'black',
                weight: 0.2,
                fillOpacity: 0.7,
                fillColor: getColor(density)
            };
        },
        onEachFeature: onEachFeature
    }).addTo(mymap);

    function getColor(d) {
        return d > 1000 ? '#800026' :
               d > 500  ? '#BD0026' :
               d > 200  ? '#E31A1C' :
               d > 100  ? '#FC4E2A' :
               d > 50   ? '#FD8D3C' :
               d > 20   ? '#FEB24C' :
               d > 10   ? '#FED976' :
               d > 0    ? '#FFFFCC' :
                          '#FFFFFF';
    }
    

    var info = L.control({ position: 'topright' });
    
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'hoverBarangay');
        this.update();
        return this._div;
    };
    
    info.update = function (props) {
        this._div.innerHTML = 'Hover over a barangay';
    };
    
    info.addTo(mymap);
    
    var totalPatientsControl = L.control({ position: 'topleft' });
    
    totalPatientsControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'totalPatients');
        this.update();
        return this._div;
    };
    
    totalPatientsControl.update = function () {
        var totalPatients = 0;
        var totalRabiesCases = totalRabibesCases;
    
        for (var key in densityData) {
            if (densityData.hasOwnProperty(key)) {
                totalPatients += densityData[key];
            }
        }
    
        this._div.innerHTML = `
            <div style="text-align: center;">
            <h2 style="color: red; margin: 0; font-size: 20px;">${totalPatients}</h2> 
            <h4 style="color: black; margin: 0; font-size: 12px;">
                Total Patients with <span style="color: red; font-size: 16px;">${totalRabiesCases}</span> Rabies Cases
            </h4>
        </div>`;
    };
    
    totalPatientsControl.addTo(mymap);
    
    var legend = L.control({ position: 'bottomleft' });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend'),
            grades = [1001, 501, 201, 101, 51, 21, 11, 1, 0];  // Reverse order
        div.innerHTML += '<h6 style="text-align: center; margin-bottom: 10px;">Patient Density</h6>';
        
        // Loop through density intervals in reverse to generate labels
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[i]) + '"></i> ' +
                (grades[i] === 0 ? '0' : (grades[i] === 1001 ? '1000+' : grades[i] + '&ndash;' + (grades[i - 1] - 1))) + '<br>';
        }
    
        div.style.padding = '10px';
        div.style.background = 'white';
        div.style.borderRadius = '5px';
        div.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.3)';
        div.style.fontSize = '14px';
        div.style.color = 'black';
        div.style.width = '150px';
    
        return div;
    };

    // Correctly add the legend to the mymap
    legend.addTo(mymap);

    var rabiesHeatmapDataScript = document.getElementById('rabies-heatmap-data');
    var rabiesHeatmapData = JSON.parse(rabiesHeatmapDataScript.textContent);

    var rabiesHeat = L.heatLayer(rabiesHeatmapData, {
        radius: 5,
        blur: 1,
        maxZoom: 10,
        gradient: {
            0.0: 'red',
            0.5: 'red',
            1.0: 'red',
        },
        minOpacity: 0.5,
        maxIntensity: 100,
        opacity: 0.7,
    }).addTo(mymap);
}
