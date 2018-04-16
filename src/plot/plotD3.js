/**
 * plot data with d3js
 */
var data = null;

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'data.json', false);
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
    data = JSON.parse(response);
});

//tweak data
data.forEach(function (d) {
    d.datetime = parseDateTime(d.timestamp);
    d.channel2 = d.channelData[1] * 1000000;
});

// set the dimensions of the canvas
var margin = { top: 20, right: 60, bottom: 20, left: 60 },
    width = 900 - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;

// set the ranges
var x = d3.scaleLinear()
        .domain([0,1000])
        .range([0, width]);

var minCh2 = 10000;        
var maxCh2 = 0; 
data.forEach(function (d) {
    if(maxCh2<d.channel2){
        maxCh2=d.channel2;
    }
    if(minCh2>d.channel2){
        minCh2=d.channel2;
    }
});

var y = d3.scaleLinear()
         .domain([minCh2,maxCh2])
         .range([height, 0]);

// define the axis
var xAxis = d3.axisBottom(x).ticks(10);
var yAxis = d3.axisLeft(y).ticks(10);

// add the SVG element
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
    .call(yAxis);

svg.append("g")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis)

var g = svg.selectAll("g")
    .data(data)
    .enter()

g.append("circle")
    .attr("cx", function (d) {
        return x(d._count);
    })
    .attr("cy", function (d) {
        return y(d.channel2);
    })
    .attr("r", function () {
        return 2;
    })
    .attr("fill", function () {
        return "#c2e6e9";
    })

// get human readable time
function parseDateTime(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp);
    var hour = a.getHours();
    var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
    var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
    var millisec = a.getMilliseconds() < 10 ? '00' + a.getMilliseconds() : a.getMilliseconds() < 100 ? '0' + a.getMilliseconds() : a.getMilliseconds();;
    var time = hour + ':' + min + ':' + sec + ':' + millisec;
    return time;
}
