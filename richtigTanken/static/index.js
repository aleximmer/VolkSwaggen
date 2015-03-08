var homeTemplate = $("#homeTemplate").html();
var mapTemplate = $("#mapTemplate").html();

var mapDfd;
var stationsDfd;
var markers = [];
var currentBestStations = [];

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
    center: new google.maps.LatLng(52.504826, 13.4112459),
    zoom: 14,
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

  var map = new google.maps.Map(document.getElementById("map"), mapOptions);

  google.maps.event.addListener(map, 'tilesloaded', function() {
    mapDfd.resolve();
  });

  mapDfd.done(function(data) {
    _.each(currentBestStations, function(station) {
      var latLng = new google.maps.LatLng(station.lat, station.lng);
      var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        curser: "pointer"
      });
      google.maps.event.addListener(marker, 'click', function() {
        selectedStation = station;
        showOverlay(2,2);
      });
      var infoWindow = new google.maps.InfoWindow({
        content: station.name
      });
      google.maps.event.addListener(infoWindow, 'domready', function(){
        $(".gm-style-iw").next("div").hide();
      });
      infoWindow.open(map, marker);
    });
    hideSpinner();
  });
}


function showTemplate(template, data) {
  $("#content").html(_.template(template, data));
}

showHome({});
startRoute();

function dispatchServerResponse(data) {
  currentBestStations = data.stations;
  switch (data.farbe) {
    case "greenn":
      changeCircleColor("green");
      changeCircleMessage("Du könntest tanken.");
      break;
    case "gelb":
      changeCircleColor("yellow");
      changeCircleMessage("Du solltest bald tanken.");
      break;
    case "rot":
      changeCircleColor("red");
      changeCircleMessage("Du musst jetzt tanken.");
      break;
    default:
      return new Error("wrong color input.");
  }
  changeCircleCount(data.ersparnis);
}

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
  count = count + "";
  var countParts= count.split(".");
  if (countParts[1] && countParts[1].length > 2) {
    countParts[1] = countParts[1].slice(0,2);
  }
  var $circleCount = $("#circle-count");
  $circleCount.text(countParts.join("."));
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
  $.get("/richtigTanken/nearGasStations").done(function(data) {
    stationsDfd.resolve(data);
  });
}

function getAllGasStations() {
  $.get("/richtigTanken/allGasStations").done(function(data) {
    stationsDfd.resolve(data);
  });
}

function routeToGasStation() {
  // var url = "http://maps.google.com/maps?" + "saddr=52.502230,13.413197" + "&daddr=52.50198,13.409852";
  var url = "http://maps.google.com/maps?" + "saddr=" + position.lat + "," + position.lng + "&daddr=" + selectedStation.lat + ","+ selectedStation.lng + "&dirflg=d";
  window.location.replace(url);
}

function getUser() {
  $.ajax("/users").done(dispatchServerReponse);
}

function sendWaypoint(waypoint) {

  $.ajax("/richtigTanken/newValue/", {
    type: "POST",
    dataType: 'json',
    contentType: 'application/json, charset=utf-8',
    data: JSON.stringify(waypoint)
  }).done(dispatchServerResponse);
}

var moving;
function startRoute() {
  moving = true;
  var index = 0;


  function nextWaypoint(index) {

    if (!moving || index >= waypoints.length) {
      return endRoute();
    }

    sendWaypoint(waypoints[index]);
    setTimeout(function() {
      nextWaypoint(index + 1);
    }, 2000);
  }
  nextWaypoint(0);
}

function endRoute() {
  if (!moving) {
    return;
  }
  moving = false;
  $.post("/richtigTanken/endRoute/", {
    dataType: 'text',
    data: "nothing"
  }).done(function(data) {
    console.log("end");
  })
}
