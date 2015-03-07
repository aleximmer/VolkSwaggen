var homeTemplate = $("#homeTemplate").html();
var mapTemplate = $("#mapTemplate").html();

var mapDfd;
var stationsDfd;
var markers = [];

var position = {
  lat: 52.502230,
  lng: 13.413197
};
var selectedStation;

/* Circle Stuff*/
var notificationCircleColor = "green";

function showHome(data) {
  showTemplate(homeTemplate, data);
}

function showMap(data) {
  showTemplate(mapTemplate, data);

  var mapOptions = {
    center: new google.maps.LatLng(52.502230, 13.413197),
    zoom: 13,
    draggable: false,
    scrollwheel: false,
    disableDoubleClickZoom: true,
    mapTypeControl: false,
    panControl: false,
    streetViewControl: false,
    zoomControl: false,
    styles: [
      {
        'featureType': 'poi',
        'elementType': 'labels',
        'stylers': [
          { 'visibility': 'off' }
        ]
      },
      {
        'featureType': 'administrative.province',
        'stylers': [
          { 'weight': 3.7 }
        ]
      }
    ],
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  mapDfd = new $.Deferred();
  stationsDfd = new $.Deferred();

  var map = new google.maps.Map(document.getElementById("map"), mapOptions);

  google.maps.event.addListener(map, 'tilesloaded', function() {
    mapDfd.resolve();
  });

  getGasStations();

  $.when(mapDfd, stationsDfd).done(function() {
    hideSpinner();
  });

  stationsDfd.done(function(data) {
    _.each(data.stations, function(station) {
      var latLng = new google.maps.LatLng(station.lat, station.lng);
      var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        curser: "pointer",
        click: function() {
          console.log("marker clicked");
        }
      });
      google.maps.event.addListener(marker, 'click', function() {
        selectedStation = station;
        showOverlay(2,2);
      });
    });
  });
}

function showTemplate(template, data) {
  $("#content").html(_.template(template, data));
}

showHome({});

function changeCircleColor(color) {
  var colorClass;
  switch (color) {
    case "green":
      colorClass = "green";
      break;
    case "yellow":
      colorClass = "yellow";
      break;
    case "red":
      colorClass = "red";
      break;
    default:
      return new Error("wrong color input.");
  }

  var $circle = $("#notification-circle");
  $circle.removeClass(notificationCircleColor);
  $circle.addClass(colorClass);
  notificationCircleColor = colorClass;
}

function changeCircleMessage(text) {
  var $circleMessage = $("#circle-message");
  $circleMessage.text(text);
}

function changeCircleCount(count) {
  var $circleCount = $("#circle-count");
  $circleCount.text(count);
}

function showOverlay(saving, delay) {
  $("#overlay-euro-value").text(saving);
  $("#overlay-minutes-value").text(delay);
  $("#overlay").fadeIn();
}

function hideOverlay() {
  $("#overlay").fadeOut();
}

function showSpinner() {
  $("#spinner-wrapper").fadeIn();
}

function hideSpinner() {
  $("#spinner-wrapper").fadeOut();
}

function getGasStations() {
  $.get("/richtigTanken/gasStations").done(function(data) {
    stationsDfd.resolve(data);
  });
}

function routeToGasStation() {
  // var url = "http://maps.google.com/maps?" + "saddr=52.502230,13.413197" + "&daddr=52.50198,13.409852";
  var url = "http://maps.google.com/maps?" + "saddr=" + position.lat + "," + position.lng + "&daddr=" + selectedStation.lat + ","+ selectedStation.lng;
  window.location.replace(url);
}

function getUser() {
  $.ajax("/users").done(function(data) {
    console.log(data);
  });
}

function sendShit() {
  var value = {
        "x": "53.2322323",
        "y": "54.2323423",
        "verbrauch": "0.23"
    }
  $.ajax("/richtigTanken/newValue/", {
    type: "POST",
    dataType: 'json',
    contentType: 'application/json, charset=utf-8',
    data: JSON.stringify(value)
  }).done(function(data) {
    console.log(data);
  })
}

function endRoute() {
  $.ajax("/richtigTanken/endRoute/", {
    type: "POST",
    dataType: 'text',
    data: "nothing"
  }).done(function(data) {
    console.log(data);
  })
}
