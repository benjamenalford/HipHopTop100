//
var myMap = L.map("map").setView([38.9822, -94.6708], 3);

var vinylIcon = L.icon({
    iconUrl: '../static/images/vinyl.png',
    iconSize: [20, 20],
    iconAnchor: [10, 10]
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    maxZoom: 11,
    id: "mapbox.light",
    accessToken: MAP_BOX_API_KEY
}).addTo(myMap);


d3.json("/api/albumData").then(data => {
    console.log(data);

    // place markers for albums
    data.forEach(row => {

        if (row.coordinates && row.coordinates.length > 0) {
            row.mapped = true;
            lat = row.coordinates[0].toFixed(2);;
            long = 0 - row.coordinates[1].toFixed(2);;
            marker = L.marker([lat, long], { icon: vinylIcon }).addTo(myMap);
            origin = ""
            if (row.origin) {
                origin = row.origin[0];
            }
            marker.bindPopup(`<h3>${row.artist}</h3><h4>${row.albumTitle}</h4><p>${origin}</p>`);
        }
    });

    // display a table
    var tableView = d3.select("#dataTable");

    data.forEach(row => {
        var r = tableView.select("tbody").append("tr");
        r.append("td").text(row.year);
        r.append("td").text(row.artist);
        r.append("td").text(row.albumTitle);
        r.append("td").text(row.origin);
        r.append("td").text(row.coordinates);
        r.append("td").append("a").attr("href", row.wikiUrl).attr("target", "_blank").text("Info")
        r.append("td").text(row.mapped);
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

}).then(e => {
    $(document).ready(function() {
        $('#dataTable').DataTable();
    });
})