//
d3.json("/api/albumData").then(data => {
    console.log(data);

    // display a table
    var tableview = d3.select("#tableView");
    var table = tableview.append("table").classed("table", true);
    var header = table.append("tr")
    header.append("th").text("artist")
    header.append("th").text("album")
    header.append("th").text("year")
    data.forEach(row => {
        var r = table.append("tr");
        r.append("td").text(row.artist);
        r.append("td").text(row.albumTitle);
        r.append("td").text(row.year);
    })
});