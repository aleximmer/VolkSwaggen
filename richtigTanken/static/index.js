var homeTemplate = $("#homeTemplate").html();
var mapTemplate = $("#mapTemplate").html();

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
    mapTypeControl: false,
    panControl: false,
    streetViewControl: false,
    zoomControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);
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

function getUser() {
  $.ajax("localhost:8000/users").done(function(data) {
    console.log(data);
  });
}
