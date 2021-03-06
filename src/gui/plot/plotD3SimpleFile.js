/**
 * plot file data with d3js
 *
 */
var path = 'data/plot/jsondata.json';
var plotdata = null;

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', path, false);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}

loadJSON(function (response) {
    // Parse JSON string into object
    plotdata = JSON.parse(response);
});

//tweak data
plotdata.forEach(function (d) {
    // channelData is Volts V, for microvolts µV
    d.channel1 = d.channelData[0] * 1000000;
    d.channel2 = d.channelData[1] * 1000000;
    d.channel3 = d.channelData[2] * 1000000;
    d.channel4 = d.channelData[3] * 1000000;
    d.channel5 = d.channelData[4] * 1000000;
    d.channel6 = d.channelData[5] * 1000000;
    d.channel7 = d.channelData[6] * 1000000;
    d.channel8 = d.channelData[7] * 1000000;
});

//---------setup plot-----------------------//
// set the dimensions of the canvas
var margin = {top: 60, right: 60, bottom: 60, left: 60},
    width = 1020 - margin.left - margin.right,
    height = 720 - margin.top - margin.bottom;

// set the ranges/scales
var minDate = plotdata[0].datetime;
var size = Object.keys(plotdata).length;
var maxDate = plotdata[size - 1].datetime;

//x Axis Scale by data[]_count
var x = d3.scaleLinear()
    .domain([0, size - 1])
    .range([0, width]);

var minCh2 = 10000;
var maxCh2 = 0;
plotdata.forEach(function (d) {
    if (maxCh2 < d.channel2) {
        maxCh2 = d.channel2;
    }
    if (minCh2 > d.channel2) {
        minCh2 = d.channel2;
    }
});

// y Axis Scale by Channel 2 values 2*min until 2*max
var y = d3.scaleLinear()
    .domain([8 * minCh2, 8 * maxCh2])
    .range([height, 0]);

// define the axis
var xAxis = d3.axisBottom(x).ticks(10);
var yAxis = d3.axisLeft(y).ticks(0);

// add the SVG element
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// y-axis
svg.append("g")
    .call(yAxis);

// y-axis Label
svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Channels");

// x-axis
svg.append("g")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis)

// x-axis Label
svg.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom - 5) + ")")
    .style("text-anchor", "middle")
    .text("Samples 250Hz");

//-------------data----------//
var height16 = height / 16; //ajust lines from 0 middleline in y axis
// define the 1 line
var valueline1 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel1) - 7 * height16;
    });
// define the 2nd line
var valueline2 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel2) - 5 * height16;
    });
// define the 3nd line
var valueline3 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel3) - 3 * height16;
    });
// define the 4nd line
var valueline4 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel4) - height16;
    });
// define the 5nd line
var valueline5 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel5) + height16;
    });
// define the 6nd line
var valueline6 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel6) + 3 * height16;
    });
// define the 7nd line
var valueline7 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel7) + 5 * height16;
    });
// define the 8nd line
var valueline8 = d3.line()
    .x(function (d, index) {
        return x(index);
    })
    .y(function (d) {
        return y(d.channel8) + 7 * height16;
    });


// Add the valueline path.
var path1 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "grey")
    .attr("id", "Channel1")
    .attr("active", true)
    .attr("d", valueline1);

var path2 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "purple")
    .attr("id", "Channel2")
    .attr("active", true)
    .attr("d", valueline2);

var path3 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "blue")
    .attr("id", "Channel3")
    .attr("active", true)
    .attr("d", valueline3);

var path4 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "green")
    .attr("id", "Channel4")
    .attr("active", true)
    .attr("d", valueline4);

var path5 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "rgb(250, 196, 61)")
    .attr("id", "Channel5")
    .attr("active", true)
    .attr("d", valueline5);

var path6 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "orange")
    .attr("id", "Channel6")
    .attr("active", true)
    .attr("d", valueline6);

var path7 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "red")
    .attr("id", "Channel7")
    .attr("active", true)
    .attr("d", valueline7);

var path8 = svg.append("path")
    .data([plotdata])
    .attr("class", "line")
    .style("stroke", "rgb(148, 47, 47)")
    .attr("id", "Channel8")
    .attr("active", true)
    .attr("d", valueline8);

// add a title
svg.append("text")
    .attr("x", (width / 2))
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("font-size", "20px")
    .text("EEG plot");

// gridlines in x axis function
function make_x_gridlines() {
    return d3.axisBottom(x)
        .ticks(10)
}

// gridlines in y axis function
function make_y_gridlines() {
    return d3.axisLeft(y)
        .ticks(10)
}

// add the X gridlines
svg.append("g")
    .attr("class", "grid")
    .attr("transform", "translate(0," + height + ")")
    .call(make_x_gridlines()
        .tickSize(-height)
        .tickFormat("")
    )

// add the Y gridlines
svg.append("g")
    .attr("class", "grid")
    .call(make_y_gridlines()
        .tickSize(-width)
        .tickFormat("")
    )

//show or hide channels
function toggleChannel(channel) {
    // determine if current line is visible
    let active = d3.select("path#" + channel).attr("active") === 'true';
    let newOpacity = (active) ? 0 : 1;
    // hide or show the elements
    d3.select("path#" + channel).style("opacity", newOpacity);
    // update whether or not the elements are active
    d3.select("path#" + channel).attr("active", !active);
}