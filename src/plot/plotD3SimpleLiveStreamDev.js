/**
 * plot file data with d3js
 */
//data to plot - default start values before samples are coming in
var nullsample = {"accelData":[0,0,0],"channelData":[0.00004,0.00003,0.00002,0.00001,-0.00001,-0.00002,-0.00003,-0.00004],"auxData":{"type":"Buffer","data":[0,0,0,0,0,0]},"sampleNumber":0,"startByte":160,"stopByte":192,"valid":true,"timestamp":1523041989391,"boardTime":0,"_count":0};

var channels = [
    {id:"Channel1", stroke:"grey", values:[]},
    {id:"Channel2", stroke:"purple", values:[]},
    {id:"Channel3", stroke:"blue", values:[]},
    {id:"Channel4", stroke:"green", values:[]},
    {id:"Channel5", stroke:"rgb(250, 196, 61)", values:[]},
    {id:"Channel6", stroke:"orange", values:[]},
    {id:"Channel7", stroke:"red", values:[]},
    {id:"Channel8", stroke:"rgb(148, 47, 47)", values:[]}
];

//create start array
for (let c = 0; c<8; c++){
//for every channel c 0-7
    for (let index = 1; index < 1000; index++) {
        //for 1000 times
        channels[c].values.push({volt:nullsample.channelData[c]*1000000});
    }
}
console.log("start:");
console.log(channels);

//shift for all values arrays of channels (delete first entry)
function shiftChannels(){
    channels.forEach( c => c.values.shift() );
}


//---------setup plot-----------------------//
// set the dimensions of the canvas
var margin = { top: 60, right: 60, bottom: 60, left: 60 },
    width = 1020 - margin.left - margin.right,
    height = 720 - margin.top - margin.bottom;

// set the ranges/scales

//x Axis Scale by data[]_count
var x = d3.scaleLinear()
    .domain([0,1000])
    .range([0, width]);

// y Axis Scale -200 to 200
var y = d3.scaleLinear()
    .domain([-800,800])
    .range([height, 0]);

// define the axis
var xAxis = d3.axisBottom(x).ticks(10);
var yAxis = d3.axisLeft(y).ticks(0);

// add the SVG element
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

var g = svg.append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// y-axis
g.append("g")
    .call(yAxis);

// x-axis
g.append("g")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis)

// x-axis Label
g.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom -5) + ")")
    .style("text-anchor", "middle")
    .text("Samples 250Hz");

//-------------data----------//
var height16 = height/16; //ajust lines from 0 middleline in y axis
// define the 1 line
var line = d3.line()
    .curve(d3.curveBasis)
    .x(function(d, i) { return x(i); })
    .y(function(d) { return y(d.volt); });


var eeg = g.selectAll(".eeg")
    .data(channels)
    .enter().append("g")
    .attr("class", "eeg");

eeg.append("path")
    .attr("class", "line")
    .attr("id", function(d) { return d.id; })
    .attr("active", true)
    .attr("d", function(d) { return line(d.values); })
    .style("stroke", function(d) { return d.stroke; });

//------update paths with new data-------//
function update() {
//TODO: fix update (dev no priority as working example exists)
    eeg.data(channels);
    //    .enter().append("g")
    //    .attr("class", "eeg");
    //
    // eeg.append("path")
    //     .attr("d", function(d) { return line(d.values); });
}

//-------------end of data----------//

// add a title
g.append("text")
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
g.append("g")
    .attr("class", "grid")
    .attr("transform", "translate(0," + height + ")")
    .call(make_x_gridlines()
        .tickSize(-height)
        .tickFormat("")
    )

// add the Y gridlines
g.append("g")
    .attr("class", "grid")
    .call(make_y_gridlines()
        .tickSize(-width)
        .tickFormat("")
    )

//show or hide channels
function toggleChannel(channel){
    // determine if current line is visible
    let active = d3.select("path#"+channel).attr("active")==='true';
    let newOpacity = (active) ? 0 : 1;
    // hide or show the elements
    d3.select("path#"+channel).style("opacity", newOpacity);
    // update whether or not the elements are active
    d3.select("path#"+channel).attr("active", !active);
}

// Connect to socket server
var socket = io.connect('http://localhost:3000');

socket.on('sample', function(data) {
    //delete first item of data
    shiftChannels()

    for (let c = 0; c<8; c++){
        //for every channel c 0-7
        channels[c].values.push(data.sample.channelData[c]*1000000);
    }
});

socket.on('error', console.error.bind(console));
socket.on('message', console.log.bind(console));

//update plot every second
setInterval(update, 250);
//log data every 5 sec.
function logChannels(){
    console.log(channels);
}
setInterval(logChannels, 5000);

