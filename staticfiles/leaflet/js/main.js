window.onload = init;


function init(){
    
    // Get total_cases from the data attribute in HTML
    const totalCasesElement = document.getElementById('total-cases-data');
    const totalCases = parseInt(totalCasesElement.getAttribute('data-total-cases'), 10);

    const totalCasesRabies = document.getElementById('total-rabies-data');
    const totalRabibesCases = parseInt(totalCasesRabies.getAttribute('data-rabies-cases'), 10);

    // Check for screen width to adjust zoom and control sizes for mobile
    const isMobile = window.innerWidth <= 600;
    const minZoom = isMobile ? 9 : 10; // Set lower zoom for smaller screens


    // Get heatmap data from script tag
    var heatmapDataScript = document.getElementById('heatmap-data');
    var heatmapData = JSON.parse(heatmapDataScript.textContent);

    

    //creating variables for each base layer
    const Dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{
        attribution: 'Animal Bite and Rabies Monitoring with GEO Mapping &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        maxZoom: 19, 
    })
    const StreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        //attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    })
    const Light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    })

    const maxBounds = L.latLngBounds(
        L.latLng(11.358607609157232, 123.91744935882099), // Southwest corner
        L.latLng(11.897821676214718, 125.01560057070333) // Northeast corner
        );

    //Creating the center of the map 
    const mymap = L.map('mama',{
        center:[11.6400,124.4642],
        zoom: isMobile ? 9 : 10.8,  // Adjust default zoom based on screen size
        minZoom: minZoom, // Dynamic min zoom 
        zoomSnap:0.75,
        zoomDelta:1,
        layers:[Dark],
        zoomControl:false,
        /* scrollWheelZoom: false, */
        gestureHandling: true,
    }).setMaxBounds(maxBounds);

    // Add zoom control manually to the bottom left
    L.control.zoom({
        position: 'bottomright'
    }).addTo(mymap);

    // Create a custom layer control
    /* var customLayerControl = L.Control.extend({
        options: {
            position: 'topright' 
        },
        
        onAdd: function (map) {
            var div = L.DomUtil.create('div', 'custom-layer-control');
            
            
            div.innerHTML = `
                <div style="background-color: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); text-align: center; height:90px">
                    <label for="layerSelect" style="margin: 0; color:blue;">Select Base Layer</label><br>
                    <select id="layerSelect" style="margin-top: 5px; padding: 5px; border-radius: 4px; width:120px">
                        <option value="dark" selected>Dark</option>
                        <option value="light">Light</option>
                    </select>
                </div>
            `;
            L.DomEvent.disableClickPropagation(div);
            
            
            div.querySelector('#layerSelect').onchange = function () {
                if (this.value === 'dark') {
                    map.removeLayer(Light);
                    map.addLayer(Dark);
                } else {
                    map.removeLayer(Dark);
                    map.addLayer(Light);
                }
            };
            
            return div;
        }
    });
    customLayerControl = new customLayerControl();
    mymap.addControl(customLayerControl); */

    var baseLayers = {
        "Dark": Dark,
        "Light": Light
    };
    
    // Add the layer control to the map (top right by default)
    L.control.layers(baseLayers).addTo(mymap);

    // Create a heatmap layer and add it to the map
    var heat = L.heatLayer(heatmapData, {
        radius: 3,
        blur: 1,
        maxZoom: 20,
        gradient: {
            0.2: 'blue',     // Low intensity
            0.4: 'cyan',     // Medium-low intensity
            0.6: 'lime',     // Medium intensity (green/yellowish)
            0.8: 'orange',   // High intensity 
            1.0: 'red'    
        },
        minOpacity: 0.5,
        maxIntensity: 100,
        opacity: 0.1
        
    }).addTo(mymap);


    // Function to create a continuously looping ping effect outside of the marker
    function createPingEffect(latlng, map) {
        let pingCircle = L.circle(latlng, {
            radius: 50,  // Starting radius for the ping effect
            color: 'red',  // Bright color for visibility
            fillColor: 'red',
            fillOpacity: 0.5,
            opacity: 0.5
        }).addTo(map);

        let radius = 2000;  // Starting size
        let maxRadius = 100000;  // Max radius for better visibility
        let opacity = 0.5;  // Starting opacity

        function animatePing() {
            radius += 20;  // Increase radius
            opacity -= 0.05;  // Decrease opacity

            pingCircle.setRadius(radius);
            pingCircle.setStyle({
                opacity: opacity,
                fillOpacity: opacity * 0.5  // Keep fill opacity consistent
            });

            // Reset the ping effect when it fades out
            if (radius >= maxRadius || opacity <= 0) {
                // Reset radius and opacity
                radius = 2500;
                opacity = 0.5;

                pingCircle.setRadius(radius);
                pingCircle.setStyle({
                    opacity: opacity,
                    fillOpacity: opacity * 0.5  // Keep fill opacity consistent
                });

                // Make it invisible after animation and stop further animation
                pingCircle.setStyle({
                    opacity: 0,  // Make it invisible
                    fillOpacity: 0  // Make the fill invisible
                });

                // After 5 seconds, restart the animation
                setTimeout(() => {
                    animatePing();  // Restart the animation after the 5-second pause
                }, 5000);  // 5 seconds delay
            } else {
                // Continue animating in a loop
                setTimeout(animatePing, 250);  // Animation speed
            }
        }

        // Start the ping animation
        animatePing();
    }



    // Get rabies heatmap data from script tag
    var rabiesHeatmapDataScript = document.getElementById('rabies-heatmap-data');
    var rabiesHeatmapData = JSON.parse(rabiesHeatmapDataScript.textContent);

    // Create a heatmap layer for human rabies cases
    var rabiesHeat = L.heatLayer(rabiesHeatmapData, {
        radius: 4,  // Smaller radius for heatmap
        blur: 8,    // Increase blur for softness
        maxZoom: 20,
        gradient: {
            0.0: 'purple',
            0.5: 'magenta',
            1.0: 'red',
        },
        minOpacity: 0.7,
        maxIntensity: 50,
        opacity: 0.9,
    }).addTo(mymap);

    // Add markers for individual rabies cases and trigger the ping effect
    // Inside your rabiesHeatmapData.forEach function, keep the existing code and ensure the marker looks like this:
    rabiesHeatmapData.forEach(function(point) {
        // Add a smaller marker
        var marker = L.circleMarker([point[0], point[1]], {
            radius: 1,  // Smaller size for human rabies marker
            color: 'blue',
            fillColor: 'purple',
            fillOpacity: 0.1,
        }).addTo(mymap);

        // Add a popup with case details
        marker.bindPopup("<b>Human Rabies Case</b><br>Location: " + point[0] + ", " + point[1]);

        // Trigger the ping effect outside the marker location
        // Offset the ping effect slightly so it appears outside the marker
        createPingEffect([point[0], point[1]], mymap);
    });


    
    var totalCasesControl = L.control({ position: 'topleft' });
    totalCasesControl.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'total-cases-control'); 
        div.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: red; margin: 0; font-size: 20px;">${totalCases}</h2> 
            <h4 style="color: black; margin: 0; font-size: 12px;">Total Patients with <span style="color: red; font-size: 15px; "> ${totalRabibesCases}</span> Rabies Cases</h4>
   
        </div>
        `;
        div.style.backgroundColor = 'rgba(255, 255, 255, 1)';
        div.style.padding = isMobile ? '5px' : '8px'; // Adjusted padding
        div.style.borderRadius = '6px'; // Slightly smaller border radius
        div.style.fontFamily = 'Arial, sans-serif';
        div.style.fontSize = '12px'; // Decreased font size
        div.style.boxShadow = '0 0 5px rgba(0, 0, 0, 0.3)'; // Optional: Add shadow
        return div;
    };

    // Add the custom control to the map
    totalCasesControl.addTo(mymap);

    // Handling the filter button click event
    document.getElementById('filterButton').addEventListener('click', function() {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        // Create a new form to submit the filter dates
        const form = document.createElement('form');
        form.method = 'GET';
        form.action = window.location.href;

        // Add start date and end date as hidden inputs
        const startInput = document.createElement('input');
        startInput.type = 'hidden';
        startInput.name = 'startDate';
        startInput.value = startDate;

        const endInput = document.createElement('input');
        endInput.type = 'hidden';
        endInput.name = 'endDate';
        endInput.value = endDate;

        form.appendChild(startInput);
        form.appendChild(endInput);
        document.body.appendChild(form);
        form.submit();
    });

    /* const legendImage = '/static/assets/leaflet/images/legend.png';
    const legendBounds = [[11.409384136258941, 124.10549110104539],[11.440794239094634,124.17252621504488]]
    const legendOverlay = L.imageOverlay(legendImage,legendBounds).addTo(mymap) */

    mymap.on('click', function(e){
        console.log(e.latlng)
    });


    // Create a legend control and add it to the bottom left
    var legend = L.control({ position: 'bottomleft' });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'legend'); // Create a div with the 'legend' class
        div.innerHTML = `
            <div style="background: linear-gradient(to right, blue, cyan, lime, orange, red); width: 115px; height: 40px; position: relative; color: white; text-align: center; border-radius: 10px">
                <span style="position: absolute; left: 5px; top: 10px;">Low</span>
                <span style="position: absolute; left: 50%; transform: translateX(-50%); top: 10px;">Medium</span>
                <span style="position: absolute; right: 5px; top: 10px;">High</span>
            </div>
        `;

        // Style the legend div
        div.style.backgroundColor = 'white'; // White background for the whole legend container
        div.style.padding = '1px'; // Adjust padding
        div.style.border = '2px solid gray';
        div.style.borderRadius = '10px';
        div.style.fontSize = '12px';
        div.style.width = '120px'; // Adjust width


        return div;
    };

    // Add the legend to the map
    legend.addTo(mymap);
}