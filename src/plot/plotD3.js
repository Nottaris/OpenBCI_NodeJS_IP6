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
    width = 1280 - margin.left - margin.right,
    height = 900 - margin.top - margin.bottom;

// set the ranges
var x = d3.scaleBand()      //TODO: d3.scaleLinear().range([0, width]);
    .rangeRound([0, width])
    .padding(0.05);
var y = d3.scaleLinear()
       //TODO .domain([d3.min(data.channel2),d3.max(data.channel2)])
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

var xAxisTranslate = height;

svg.append("g")
    .attr("transform", "translate(0, " + xAxisTranslate + ")")
    .call(xAxis)


var g = svg.selectAll("g")
    .data(data)
    .enter()
    .append("g")
    .attr("transform", function (d, i) {
        return "translate(0,0)";
    })

g.append("circle")
    .attr("cx", function (d, i) {
        return i * 10;
    })
    .attr("cy", function (d, i) {
        return d.channel2;
    })
    .attr("r", function (d) {
        return 3;
    })
    .attr("fill", function (d, i) {
        return "#c2e699";
    })

g.append("text")
    .attr("x", function (d, i) {
        return i * 10;
    })
    .attr("y", 105)
    .attr("stroke", "teal")
    .attr("font-size", "12px")
    .attr("font-family", "sans-serif")
    .text(function (d) {
        return d._count;
    });

// get human readable time
function parseDateTime(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
    var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
    var millisec = a.getMilliseconds() < 10 ? '00' + a.getMilliseconds() : a.getMilliseconds() < 100 ? '0' + a.getMilliseconds() : a.getMilliseconds();;
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec + ':' + millisec;
    return time; // + " @ " + UNIX_timestamp;
}
