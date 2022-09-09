

  // initialize the map

  var cave_data = L.layerGroup();

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

  // method that we will use to update the control based on feature properties passed
  info.update = function (props) {
    function significantFigure(string) {
      var pos = string.search(".")
      return string.slice(0,pos+4)
    };

      this._div.innerHTML = '<h4>Therion scrap name</h4>' +  (props ?
          '<b>Name: </b>' + props._NAME + '<br /><b>Survey: </b>' + props._SURVEY + '<br /><b>Average altitude: </b>'+ significantFigure(String(props._Z)) +' m'
          : 'Hover over a cave passage');
  };



function onEachFeature(feature, layer) {
  if (feature.properties && feature.properties.link) {
    let lat  = Number(feature.geometry.coordinates[0].toPrecision(7))
    let long =  Number(feature.geometry.coordinates[1].toPrecision(7))
    let popUpContent =
      `<a href="${feature.properties.link}">`+
      `<em>${feature.properties.name}</em></a>`+
      `<p>${lat}°N<br>${long}°E</p>`+
      `<p><em>Depth</em>: ${feature.properties.depth} m</p>`;

      layer.bindPopup(popUpContent)
   /* layer.bindPopup(`<a href="${feature.properties.link}"><em>${feature.properties.name}</em></a><p>${feature.geometry.coordinates[0]}<br>${feature.geometry.coordinates[1]}</p><p><em>Depth</em>:${feature.properties.depth} m</p>`)*/
  }
  else if (feature.properties) {
     let lat  = Number(feature.geometry.coordinates[0].toPrecision(7))
     let long =  Number(feature.geometry.coordinates[1].toPrecision(7))
     let popUpContent =
      `<em>${feature.properties.name}</em>`+
      `<p>${lat}°N<br>${long}°E</p>`+
      `<p><em>Depth</em>: ${feature.properties.depth} m</p>`;

      layer.bindPopup(popUpContent)
   /* layer.bindPopup(`<a href="${feature.properties.link}"><em>${feature.properties.name}</em></a><p>${feature.geometry.coordinates[0]}<br>${feature.geometry.coordinates[1]}</p><p><em>Depth</em>:${feature.properties.depth} m</p>`)*/
  }
}


var geojsonFeature = {
"type": "FeatureCollection",
"name": "cave_sites",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "id": 5, "name": "M-17", "short_name": "M17", "presented": "False", "position": 3, "C14samples": null, "C14_used": null , "depth": 89}, "geometry": { "type": "Point", "coordinates": [ 13.762522443776271, 46.245946369854053 ] } },
{ "type": "Feature", "properties": { "id": 2, "name": "Guffert Eisschacht", "short_name": "GU", "presented": "True", "position": 7, "C14samples": "20 (0)", "C14_used": "17" , "link":"https://tr1813.github.io/ancient-ice-in-austria/html/guffert.html", "depth": null}, "geometry": { "type": "Point", "coordinates": [ 11.820032941343642, 47.536128125226163 ] } },
{ "type": "Feature", "properties": { "id": 3, "name": "Hundalm Tropfstein-<br>und Eishöhle", "short_name": "HU", "presented": "True", "position": 1, "C14samples": "10 (1)", "C14_used": "8", "link": "https://tr1813.github.io/ancient-ice-in-austria/html/hundalm.html", "depth": 55 }, "geometry": { "type": "Point", "coordinates": [ 12.050400653587111, 47.551995830084515 ] } },
{ "type": "Feature", "properties": { "id": 4, "name": "Anton Gaugg<br>Eisschacht", "short_name": "AG", "presented": "False", "position": 3, "C14samples": null, "C14_used": null }, "geometry": { "type": "Point", "coordinates": [ 11.332138641160379, 47.404453851580193 ] } },
{ "type": "Feature", "properties": { "id": 1, "name": "Eisgruben<br>Eishöhle", "short_name": "EE", "presented": "True", "position": 7, "C14samples": "20 (0)", "C14_used": "16",  "link":"https://tr1813.github.io/ancient-ice-in-austria/html/eisgruben.html", "depth": null}, "geometry": { "type": "Point", "coordinates": [ 13.694163270887012, 47.602443023494843 ] } },
{ "type": "Feature", "properties": { "id": 7, "name": "Kraterschacht", "short_name": "KS", "presented": "True", "position": 1, "C14samples": "5 (1)", "C14_used": "3", "link": "https://tr1813.github.io/ancient-ice-in-austria/html/kraterschacht.html", "depth": null}, "geometry": { "type": "Point", "coordinates": [ 14.353741963030156, 47.76978856713469 ] } },
{ "type": "Feature", "properties": { "id": 8, "name": "Großer<br>Naturschacht", "short_name": "GN", "presented": "True", "position": 1, "C14samples": "9 (2)", "C14_used": "5" ,"link": "https://tr1813.github.io/ancient-ice-in-austria/html/grosser-naturschacht.html", "depth": null}, "geometry": { "type": "Point", "coordinates": [ 13.671789730321089, 46.599515185258099 ] } },
{ "type": "Feature", "properties": { "id": 9, "name": "Tremml-Schacht", "short_name": "TS", "presented": "True", "position": 1, "C14samples": "2", "C14_used": "2", "link": "https://tr1813.github.io/ancient-ice-in-austria/html/tremml.html", "depth": null }, "geometry": { "type": "Point", "coordinates": [ 15.172370083323887, 47.633935463635453 ] } },
{ "type": "Feature", "properties": { "id": 10, "name": "Bärenloch Eishöhle", "short_name": "BL", "presented": "True", "position": 7, "C14samples": "23 (0)", "C14_used": "17", "link": "https://tr1813.github.io/ancient-ice-in-austria/html/baerenloch.html" , "depth": null}, "geometry": { "type": "Point", "coordinates": [ 14.965173467501407, 47.560225309937522 ] } },
{ "type": "Feature", "properties": { "id": 6, "name": "Hochschneid<br>Eishöhle", "short_name": "HE", "presented": "True", "position": 3, "C14samples": "15 (0)", "C14_used": "11", "link": "https://tr1813.github.io/ancient-ice-in-austria/html/hochschneid.html", "depth": null }, "geometry": { "type": "Point", "coordinates": [ 13.706546374952568, 47.80326656366897 ] } }
]
};


var cavesiteMarkerOptions = {
    radius: 5,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

/*L.geoJSON(cave_sites, {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
    },
}).addTo(cave_data);*/

L.geoJSON(geojsonFeature, {
    style: {
    radius: 5,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
    },
    onEachFeature: onEachFeature
}).addTo(cave_data);



 var legend = L.control({position: 'bottomright'});
/*

  function highlightFeature(e) {
      var layer = e.target;

      layer.setStyle({
          weight: 3,
          color: '#ffaa00',
          dashArray: '',
          fillOpacity: 0.7
      });

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
      info.update(layer.feature.properties);
  }

  // reset to default state
  function resetHighlight(e) {
      cave_site.resetStyle(e.target);
      info.update();
  }


  function zoomToFeature(e) {
      mymap.fitBounds(e.target.getBounds());
  }

  function onEachSurvey(feature, layer) {
      // does this feature have a property named popupContent?
      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
      })
      layer.bindPopup(feature.properties.name)
  }

 mig_outline = L.geoJSON(mig_outline, {
      style: style,
      onEachFeature: onEachSurvey
  }).addTo(cave_data);

sites = L.geoJSON(cave_sites, {
  pointToLayer: function (feature, latlng) {
      return L.circleMarker(latlng, cavesiteMarkerOptions);
    }
  }).addTo(cave_data);

*/


  var mymap = L.map('mapid', {
    center:[47.25, 12.755],
    zoom: 7,
    layers: [outdoors, cave_data]
  });

    var baseMaps = {
      "Outdoors": outdoors,
      "Streets": streets
  };

  var overlayMaps = {
      "caves sites": geojsonFeature
  };
  L.control.layers(baseMaps, overlayMaps).addTo(mymap);
  legend.addTo(mymap);
   info.addTo(mymap);
