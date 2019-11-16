//
var myMap = L.map("map").setView([38.9822, -94.6708], 3);

var vinylIcon = L.icon({
    iconUrl: '../static/images/vinyl.png',
    iconSize: [20, 20],
    iconAnchor: [10, 10]
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    maxZoom: 11,
    id: "mapbox.pencil",
    accessToken: MAP_BOX_API_KEY
}).addTo(myMap);


d3.json("/api/albumData").then(data => {
    console.log(data);

    // display a table
    var tableview = d3.select("#tableView");
    var table = tableview.append("table").classed("table", true);
    var header = table.append("tr");
    header.append("th").text("artist");
    header.append("th").text("album");
    header.append("th").text("year");
    data.forEach(row => {
        var r = table.append("tr");
        r.append("td").text(row.artist);
        r.append("td").text(row.albumTitle);
        r.append("td").text(row.year);
    })

    // place markers for albums
    data.forEach(row => {
        if (row.coordinates && row.coordinates.length > 0) {
            lat = row.coordinates[0];
            long = 0 - row.coordinates[1];
            marker = L.marker([lat, long], { icon: vinylIcon }).addTo(myMap);
            origin = ""
            if (row.origin) {
                origin = row.origin[0];
            }
            marker.bindPopup(`<h3>${row.artist}</h3><h4>${row.albumTitle}</h4><p>${origin}</p>`);
        }
    });

    // Plot some data
    var trace1 = {
        x: data.map(r => r.year),
        y: data.map(r => r.year),
        type: "bar"
    };

    var data = [trace1];

    var layout = {
        title: "Releases By Year"
    };

    Plotly.newPlot("plot", data, layout);

})