var homeTemplate = $("#homeTemplate").html();
var mapTemplate = $("#mapTemplate").html();

var mapDfd;
var markers = [];
var currentBestStations = [];
var currentPosition;
var currentColor;
var stopped = false;
var currentData;
var moving = false;
var index = 0;

var position = {
  lat: 52.502230,
  lng: 13.413197
};
var selectedStation;

/* Circle Stuff*/
var notificationCircleColor = "green";

function showHome(data) {
  showTemplate(homeTemplate, data);
  startRoute();
  if (currentData) {
    dispatchServerResponse(currentData);
  }
}

function showMap(data) {
  stopRoute();
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
    fitBounds: true,
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

  new google.maps.Marker({
    position: new google.maps.LatLng(currentPosition.lat, currentPosition.lng),
    map: map,
    icon: "http://google.github.io/material-design-icons/maps/svg/ic_directions_car_24px.svg"
  });

  mapDfd.done(function(data) {
    _.each(currentData.stations, function(station) {
      var latLng = new google.maps.LatLng(station.lat, station.lng);
      var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        curser: "pointer",
        icon: "http://google.github.io/material-design-icons/maps/svg/ic_local_gas_station_24px.svg"
      });

      google.maps.event.addListener(marker, 'click', function() {
        selectedStation = station;
        showOverlay(station.benzin, getDistance(new google.maps.LatLng(currentPosition.lat, currentPosition.lng), latLng));
      });

      var infoWindow = new google.maps.InfoWindow({
        content: station.name + " "  + station.benzin + "&euro;"
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

function getDistance(a, b) {
  return google.maps.geometry.spherical.computeDistanceBetween(a, b);
}


function dispatchServerResponse(data) {
  console.log("bam");
  currentData = data;
  switch (data.farbe) {
    case "green":
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
  currentColor = color;
  var colorClass;
  switch (color) {
    case "green":
      colorClass = "green";
      break;
    case "yellow":
      colorClass = "yellow";
      break;
    case "red":
      colorClass = "deep-orange";
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

function roundThatShit(count) {
  count = count + "";
  var countParts= count.split(".");
  if (countParts[1] && countParts[1].length > 2) {
    countParts[1] = countParts[1].slice(0,2);
  }
  return countParts.join(".")
}

function roundThatShitVöllig(count) {
  count = count + "";
  var countParts = count.split(".");
  return countParts[0];
}
var istNull = true;
function changeCircleCount(count) {
  console.log(count);
  if (count <= 0) {
    if (!istNull) {
      istNull = true;
      $("#richtigesTanken").hide();
      $("#keinTanken").show();
    }
    return;
  } else if (istNull) {
    istNull = false;
    $("#keinTanken").hide();
    $("#richtigesTanken").show();
  }
  count = roundThatShit(count);
  var $circleCount = $("#circle-count");
  $circleCount.text(count);
}

function showOverlay(saving, delay) {
  $("#overlay-euro-value").text(roundThatShit(saving));
  $("#overlay-minutes-value").text(roundThatShitVöllig((delay * 10 / (35 / 3.6))/60));
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


function startRoute() {
  moving = true;
  stopped = false;

  function nextWaypoint(index) {
    if (stopped) {
      return;
    }

    if (!moving || index >= waypoints.length) {
      return endRoute();
    }

    sendWaypoint(waypoints[index]);
    currentPosition = {
      lat: waypoints[index].lat,
      lng: waypoints[index].lng
    };
    setTimeout(function() {
      nextWaypoint(index + 1);
    }, 2000);
  }
  nextWaypoint(index);
}

function reset() {
  index = 0;
  stopped = true;
  moving = false;
  endRoute();
}

function stopRoute() {
  stopped = true;
}

function endRoute() {
  moving = false;
  $.post("/richtigTanken/endRoute/", {
    dataType: 'text',
    data: "nothing"
  }).done(function(data) {
    console.log("end");
  })
}
