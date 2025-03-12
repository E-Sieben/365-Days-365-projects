async function updateMap() {
  //Mapbox
  mapboxgl.accessToken = "YOUR-TOKEN";
  var map = new mapboxgl.Map({
    container: "map",
    style: mapDesign,
    center: [6.786094, 51.284714],
    zoom: 10,
  });

  map.on("load", function () {
    map.addLayer({
      id: "traffic",
      type: "line",
      source: {
        type: "vector",
        url: "mapbox://mapbox.mapbox-traffic-v1",
      },
      "source-layer": "traffic",
      layout: {
        "line-join": "round",
        "line-cap": "round",
      },
      paint: {
        "line-color": [
          "case",
          ["==", ["get", "congestion"], "low"],
          "#30a255",
          ["==", ["get", "congestion"], "moderate"],
          "#FFFF00",
          ["==", ["get", "congestion"], "heavy"],
          "#FF0000",
          "#000000",
        ],
        "line-width": 3,
      },
    });
  });
}
