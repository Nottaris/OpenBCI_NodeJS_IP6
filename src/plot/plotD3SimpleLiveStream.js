/**
 * plot file data with d3js
 */
//data to plot - default start values before samples are coming in
var plotdata = [{"accelData":[0,0,0],"channelData":[0.000004,0.000003,0.000002,0.000001,-0.000001,-0.000002,-0.000003,-0.000004],"auxData":{"type":"Buffer","data":[0,0,0,0,0,0]},"sampleNumber":0,"startByte":160,"stopByte":192,"valid":true,"timestamp":1523041989391,"boardTime":0,"_count":0}];
var itemnull = tweakData(plotdata[0]);
//create start array
for (let index = 1; index < 1000; index++) {
     plotdata.push(itemnull);
}

//tweak data - ajust Volts
function tweakData(sample){
        // channelData is Volts V, for microvolts µV
        sample.channel1 = sample.channelData[0] * 1000000;
        sample.channel2 = sample.channelData[1] * 1000000;
        sample.channel3 = sample.channelData[2] * 1000000;
        sample.channel4 = sample.channelData[3] * 1000000;
        sample.channel5 = sample.channelData[4] * 1000000;
        sample.channel6 = sample.channelData[5] * 1000000;
        sample.channel7 = sample.channelData[6] * 1000000;
        sample.channel8 = sample.channelData[7] * 1000000;
        return sample;
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
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// y-axis
svg.append("g")
    .call(yAxis);
    
// x-axis
svg.append("g")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis)

// x-axis Label
svg.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom -5) + ")")
    .style("text-anchor", "middle")
    .text("Samples 250Hz");

//-------------data----------//
var height16 = height/16; //ajust lines from 0 middleline in y axis
// define the 1 line
var valueline1 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel1)-7*height16; });
// define the 2nd line
var valueline2 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel2)-5*height16; });
// define the 3nd line
var valueline3 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel3)-3*height16; });
// define the 4nd line
var valueline4 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel4)-height16; });                    
// define the 5nd line
var valueline5 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel5)+height16; });

// define the 6nd line
var valueline6 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel6)+3*height16; });
// define the 7nd line
var valueline7 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel7)+5*height16; });
// define the 8nd line
var valueline8 = d3.line()
                    .x(function(d, index) { return x(index); })
                    .y(function(d) { return y(d.channel8)+7*height16; });



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

//------update paths with new data-------//
function update() {
    path1.data([plotdata])
         .attr("d", valueline1);
    path2.data([plotdata])
         .attr("d", valueline2);
    path3.data([plotdata])
         .attr("d", valueline3);
    path4.data([plotdata])
         .attr("d", valueline4);
    path5.data([plotdata])
         .attr("d", valueline5);
    path6.data([plotdata])
         .attr("d", valueline6);
    path7.data([plotdata])
         .attr("d", valueline7);
    path8.data([plotdata])
         .attr("d", valueline8);
  }
//-------------end of data----------//

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
    //tweak data (ajust volts)
    var tweakedData = tweakData(data.sample);
    //delete first item of data
    plotdata.shift();
    //add new sample to data
    plotdata.push(tweakedData);
});

socket.on('error', console.error.bind(console));
socket.on('message', console.log.bind(console));

//update plot every second
setInterval(update, 250);