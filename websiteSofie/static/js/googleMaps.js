function initMap() {
  var mapDiv = document.getElementById('map');
  var map = new google.maps.Map(mapDiv, {
    center: {lat: 51.172278, lng: 4.501100},
    zoom: 16
  });
}
