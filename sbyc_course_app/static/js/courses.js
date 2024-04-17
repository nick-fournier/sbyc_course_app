
// Your JSON string
const jsonString = JSON.parse(document.getElementById("course_data").textContent);

// Parse the JSON string
var courses = JSON.parse(jsonString);

// Get the select element
var courseSelect = document.getElementById("courseSelect");

// Add an option to the course select called "Marks" that just shows the marks without polylines
var option = document.createElement("option");
option.value = "marks";
option.text = "Marks";
courseSelect.add(option);

// Populate the select options
Object.keys(courses).forEach(courseNumber => {
  var option = document.createElement("option");
  option.value = courseNumber;
  option.text = "Course " + courseNumber;
  courseSelect.add(option);
});

// Add the marks data to the courses object
courses['marks'] = getMarks();

// Initialize the map
var map = L.map('map').setView([37.77724166666667, -122.37284166666666], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Function to load the selected route
function loadRoute() {
  // Clear previous markers
  map.eachLayer(layer => {
    if (layer instanceof L.Marker || layer instanceof L.Polyline || layer instanceof L.Circle) {
      map.removeLayer(layer);
    }
  });

  // Clear previous table rows
  var routeTable = document.getElementById("routeTable");
  while (routeTable.rows.length > 1) {
    routeTable.deleteRow(1);
  }

  var selectedCourse = courses[courseSelect.value];

  // Plot the route
  var routePoints = selectedCourse.map(point => [point.lat, point.lon]);
  var polyline = L.polyline(routePoints, { color: 'blue' })
  if (courseSelect.value !== "marks") {
    polyline.addTo(map);
  }
  
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
    row.innerHTML = `
    <td>${point.order}</td>
    <td>${point.name}</td>
    <td>${point.rounding}</td>
    <td>${point.bearing}</td>`;
  });

  // Fit the map to the bounds of the route
  map.fitBounds(polyline.getBounds());
}

// Load the initial route
loadRoute();

// Function to either select course or generate marks data
function getMarks() {
  // Create course as a list of all unique points from all courses
  marks = [];

  // For each course in courses and each point in course
  Object.values(courses).forEach(course => {
    course.forEach(point => {
      if (!marks.some(p => p.name === point.name)) {
        // Make a copy of the point object to avoid modifying the original object
        point = Object.assign({}, point);
        // set order to empty and bearing as lat/lon string "lat, lon"
        point.bearing = `${point.lat.toFixed(6)}, ${point.lon.toFixed(6)}`
        point.order = "";
        marks.push(point);
      }
    });
  });

  return(marks)
}

// Function to change rounding order
function changeRounding() {
  var selectedCourse = courses[courseSelect.value];

  // Find all "W" and "R" points in the route
  var wPoints = selectedCourse.filter(point => point.name === "W");
  var rPoints = selectedCourse.filter(point => point.name === "R");

  // Swap the rounding label if port or starboard in the course
  selectedCourse.forEach(point => {
    if (point.rounding === 'PORT' && ['W', 'R'].includes(point.name)) {
      point.rounding = 'STARBOARD'
    } else if (point.rounding === "STARBOARD" && ['W', 'R'].includes(point.name)) {
      point.rounding = 'PORT'
    }
  })

  // Swap the Order values for each pair and the 'rounding' label
  for (var i = 0; i < Math.min(wPoints.length, rPoints.length); i++) {
      var tempOrder = wPoints[i].order;
      wPoints[i].order = rPoints[i].order;
      rPoints[i].order = tempOrder;
  }

  // Sort the course_data array based on the Order values
  selectedCourse.sort((a, b) => a.order - b.order);

  // Update the rounding button text and color. If port and red, set to starboard and green, and vice versa
  var roundingButton = document.getElementById("roundingButton");
  roundingButton.innerText = roundingButton.innerText.includes("Port") ? "Starboard" : "Port";
  roundingButton.style.backgroundColor = roundingButton.innerText.includes("Port") ? "red" : "green";

  // Reload the route
  loadRoute();

}

// Function to download the course as a GPX file
function downloadGPX() {

  var selectedCourseNumber = courseSelect.value;
  var selectedCourse = courses[selectedCourseNumber];
  var roundingOption = roundingButton.innerText.includes("Port") ? "Port" : "Starboard";

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

// Function to get the current GPS location
function getGPSLocation() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        });
      }, reject);
    } else {
      reject(new Error("Geolocation is not supported by this browser."));
    }
  });
}

// Function to display a location as a blue circle on a map
function displayLocation(map, latitude, longitude) {
  L.circle([latitude, longitude], {
    color: 'blue',
    fillColor: '#30f',
    fillOpacity: 0.5,
    radius: 50
  }).addTo(map);
}

// Usage
getGPSLocation().then(position => {
  displayLocation(map, position.latitude, position.longitude);
}).catch(error => {
  console.error(error);
});