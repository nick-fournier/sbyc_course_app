
// Your JSON string
const jsonString = JSON.parse(document.getElementById("course_data").textContent);

// Parse the JSON string
var courses = JSON.parse(jsonString);

// Get the select element
var courseSelect = document.getElementById("courseSelect");

// Populate the select options
Object.keys(courses).forEach(courseNumber => {
  var option = document.createElement("option");
  option.value = courseNumber;
  option.text = "Course " + courseNumber;
  courseSelect.add(option);
});

// Initialize the map
var map = L.map('map').setView([37.77724166666667, -122.37284166666666], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Function to load the selected route
function loadRoute() {
  var selectedCourseNumber = courseSelect.value;
  var selectedCourse = courses[selectedCourseNumber];

  // Clear previous markers
  map.eachLayer(layer => {
    if (layer instanceof L.Marker || layer instanceof L.Polyline) {
      map.removeLayer(layer);
    }
  });

  // Clear previous table rows
  var routeTable = document.getElementById("routeTable");
  while (routeTable.rows.length > 1) {
    routeTable.deleteRow(1);
  }

  // Plot the route
  var routePoints = selectedCourse.map(point => [point.lat, point.lon]);
  var polyline = L.polyline(routePoints, { color: 'blue' }).addTo(map);

  // Add circle markers for each point with a radius based on Precision_value and label
  selectedCourse.forEach(point => {
    var circle = L.circle([point.lat, point.lon], {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5,
      radius: point.precision_value
    }).addTo(map);

    // Add a label with the name of the point
    L.marker([point.lat, point.lon], {
      icon: L.divIcon({
        className: 'dummy',
        html: `<div style="margin-left: 10px; margin-top: -10px;">${point.name}</div>`,
        iconSize: [0, 0], // Set iconSize to [0, 0] to disable the default icon
        iconAnchor: [0, 0]  // Set iconAnchor to [0, 0] to disable the default icon
      })
    }).addTo(map);

    circle.bindPopup(`<b>${point.name}</b><br>${point.rounding}, Bearing: ${point.bearing}`);
    
    // Add row to the table
    var row = routeTable.insertRow();
    row.innerHTML = `<td>${point.order}</td><td>${point.name}</td><td>${point.rounding}</td><td>${point.bearing}</td><td>${point.lat.toFixed(6)}</td><td>${point.lon.toFixed(6)}</td>`;

  });

  // Fit the map to the bounds of the route
  map.fitBounds(polyline.getBounds());
}

// Load the initial route
loadRoute();

// Function to change rounding order
function changeRounding() {
  var selectedCourseNumber = courseSelect.value;
  var selectedCourse = courses[selectedCourseNumber];

  // Find all "W" and "R" points in the route
  var wPoints = selectedCourse.filter(point => point.name === "W");
  var rPoints = selectedCourse.filter(point => point.name === "R");

  // Swap the Order values for each pair
  for (var i = 0; i < Math.min(wPoints.length, rPoints.length); i++) {
      var tempOrder = wPoints[i].order;
      wPoints[i].order = rPoints[i].order;
      rPoints[i].order = tempOrder;
  }

  // Sort the course_data array based on the Order values
  selectedCourse.sort((a, b) => a.order - b.order);

  // Update the rounding display
  var roundingOption = roundingDisplay.innerText.includes("Port") ? "Starboard" : "Port";
  roundingDisplay.innerText = `${roundingOption} rounding (${roundingOption === "Port" ? "red" : "green"} flag)`;

  // Reload the route
  loadRoute();

}

// Function to download the course as a GPX file
function downloadGPX() {

  var selectedCourseNumber = courseSelect.value;
  var selectedCourse = courses[selectedCourseNumber];
  
  var gpxData = generateGPX(selectedCourse, selectedCourseNumber, roundingOption);
  var blob = new Blob([gpxData], { type: "application/gpx+xml" });

  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = `course_${selectedCourseNumber}.gpx`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Function to generate GPX data from the course
function generateGPX(course, courseNumber, roundingOption) {
  var gpx = `<?xml version="1.0" encoding="UTF-8"?>
  <gpx version="1.1" creator="FNS Course App">
    <rte>
      <name>SBYC FNS Course #${courseNumber} ${roundingOption} windward rounding</name>
      <rtept>`;

  course.forEach(point => {
    gpx += `<trkpt lat="${point.lat}" lon="${point.lon}">
              <name>${point.name}</name>
            </trkpt>`;
  });

  gpx += `</rtept>
    </rte>
  </gpx>`;

  return gpx;
}
