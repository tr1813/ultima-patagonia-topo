

  // initialize the map

  var cave_data = L.layerGroup();


  var caveIcon = L.icon({
        iconSize:     [20, 17], // size of the icon
        shadowSize:   [50, 64], // size of the shadow
        iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        shadowAnchor: [4, 62],  // the same for the shadow
        popupAnchor:  [20, 0], // point from which the popup should open relative to the iconAnchor
        iconUrl: '../javascript/entrance_icon.png'
    });

    var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      token = 'pk.eyJ1IjoidHIxODEzIiwiYSI6ImNrYW04eHZzdjEyNDYyc3RkeGtsdm40YnIifQ.uLpBRjSRgl9hHISjrEphCQ',
      mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}';


   var outdoors = L.tileLayer(mbUrl, {attribution: mbAttr, id: 'mapbox/outdoors-v11', tileSize: 512, zoomOffset: -1, accessToken: token}),
     streets = L.tileLayer(mbUrl, {attribution: mbAttr, id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, accessToken: token});

  var info = L.control();



  info.onAdd = function (cave_data) {
      this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
      this.update();
      return this._div;
  };

  function createMarker(feature, latlng) {
    return L.marker(latlng, {icon: caveIcon});
  }

function onEachZone(feature, layer){
  if (feature.properties && feature.properties.Nom) {
    let popUpContent = `<h5>${feature.properties.Nom}</h5>`+
    `<p>${feature.properties.Cadastre_ID}</p>`;
    layer.bindPopup(popUpContent)
  }
};

function onEachShot(feature, layer){
  if (feature.properties && feature.properties._SURVEY) {
    let popUpContent = `<h5>${feature.properties._SURVEY}</h5>`
    layer.bindPopup(popUpContent)
  }
};

function onEachFeature(feature, layer) {
  if (feature.properties && feature.properties.link) {
    let lat  = Number(feature.geometry.coordinates[0].toPrecision(7))
    let long =  Number(feature.geometry.coordinates[1].toPrecision(7))
    let popUpContent =
      `<a href="${feature.properties.link}">`+
      `<h5>${feature.properties.name}</h5></a>`+
      `<p><em>Latitude:</em>${lat}°N<br><em>Longitude</em>${long}°E`+
      `<br><em>N° cadastral:</em>${feature.properties.no_cadastral}</p>`+

      `<p><em>Depth</em>: ${feature.properties.depth} m</p>`;

      layer.bindPopup(popUpContent);
      layer.bindTooltip(feature.properties.name);

   /* layer.bindPopup(`<a href="${feature.properties.link}"><em>${feature.properties.name}</em></a><p>${feature.geometry.coordinates[0]}<br>${feature.geometry.coordinates[1]}</p><p><em>Depth</em>:${feature.properties.depth} m</p>`)*/
  }
  else if (feature.properties) {
     let lat  = Number(feature.geometry.coordinates[0].toPrecision(7))
     let long =  Number(feature.geometry.coordinates[1].toPrecision(7))
     let popUpContent =
      `<h5>${feature.properties.name}</h5>`+
      `<p><em>Latitude:</em>${lat}°N<br><em>Longitude</em>${long}°E`+
      `<br><em>N° cadastral:</em>${feature.properties.no_cadastral}</p>`+

      `<p><em>Depth</em>: ${feature.properties.depth} m</p>`;

      layer.bindPopup(popUpContent);
      layer.bindTooltip(feature.properties.name);
   /* layer.bindPopup(`<a href="${feature.properties.link}"><em>${feature.properties.name}</em></a><p>${feature.geometry.coordinates[0]}<br>${feature.geometry.coordinates[1]}</p><p><em>Depth</em>:${feature.properties.depth} m</p>`)*/
  }
}


  var myZoneStyle = {
    "color": "#2e3538",
    "weight": 1,
    "opacity": 0.35
};

var myShotStyle = {
  "color": "#d45500",
  "weight": 2,
  "opacity": 1
};

 L.geoJSON(cadastre,{
   style: myZoneStyle,
   onEachFeature: onEachZone
 }).addTo(cave_data);

 L.geoJSON(visees,{
   style: myShotStyle,
   onEachFeature: onEachShot
 }).addTo(cave_data);

 L.geoJSON(geojsonFeature, {
    pointToLayer: createMarker,
     onEachFeature: onEachFeature
 }).addTo(cave_data);


 var legend = L.control({position: 'bottomright'});

  var mymap = L.map('mapid', {
    center:[-50.25, -75.755],
    zoom: 7,
    layers: [outdoors, cave_data]
  });


    var baseMaps = {
      "Outdoors": outdoors,
      "Streets": streets
  };

  var overlayMaps = {
      "caves sites": geojsonFeature,
      "zones": data
  };
  L.control.layers(baseMaps, overlayMaps).addTo(mymap);
  legend.addTo(mymap);
   info.addTo(mymap);
