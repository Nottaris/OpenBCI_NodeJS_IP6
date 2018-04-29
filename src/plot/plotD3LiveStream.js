/**
 * plot live data with d3js streaming
 */
'use strict';

// create the real time chart
var chart = realTimeChartMulti()
    .title("")
    .yTitle("")
    .xTitle("Time")
    .yDomain(["Channel1"]) // initial y domain (note array)
    .border(true)
    .width(600)
    .height(600);

// invoke the chart
var chartDiv = d3.select("#viewDiv").append("div")
    .attr("id", "chartDiv")
    .call(chart);

// event handler for debug checkbox
d3.select("#debug").on("change", function () {
    var state = d3.select(this).property("checked")
    chart.debug(state);
})

// event handler for halt checkbox
d3.select("#halt").on("change", function () {
    var state = d3.select(this).property("checked")
    chart.halt(state);
})

// configure the data generator

// mean and deviation for generation of time intervals
var tX = 5; // time constant, multiple of one second

// define time scale
var timeScale = d3.scale.linear()
    .domain([300 * tX, 1700 * tX])
    .range([300 * tX, 1700 * tX])
    .clamp(true);

// define colors
var channelColors = ["#999999", "#663399", "#6600ff", "#336633", "#ffcc66", "#ff9933", "#ff0000", "#663300"];

var shapes = ["rect", "circle"];
var timeout = 0;
//var channelSelection = ["Channel1", "Channel2", "Channel3", "Channel4", "Channel5", "Channel6", "Channel7", "Channel8"];
var channelSelection = ["Channel1"];
channelSelection.reverse();

function addChannel(channel) {
    channelSelection.push("Channel"+channel);
    channelSelection.sort().reverse();
}

function removeChannel(channel) {
    var index = channelSelection.indexOf("Channel"+channel);
    if (index > -1) {
        channelSelection.splice(index, 1);
    }
}

function toggleChannel(channel){
    var index = channelSelection.indexOf("Channel"+channel);
    if (index > -1) {
        removeChannel(channel);
    }else{
        addChannel(channel);
    }
}

// define data generator
function dataGenerator(sample) {

        // add categories dynamically
        chart.yDomain(channelSelection);
      
        // output a sample for each category, each interval (0.004 seconds == 250Hz)
        chart.yDomain().forEach(function (cat, i) {
            // create new data item
            var obj = {
                // complex data item; four attributes (type, color, opacity and size) are changing dynamically with each iteration (as an example)
                time: sample.timestamp,   // new Date(sample.timestamp),   for playback of file, but as this is in the past, you will see nothing!
                color: channelColors[i] || "#000033",
                category: cat,
                type: "circle",
                size: 1,
                channel: sample.channelData[i] * 1000000 // channelData is Volts V, for microvolts µV
            }
            // send the datum to the chart
            chart.datum(obj);
        });
}

// Connect to socket server
var socket = io.connect('http://localhost:3000');

socket.on('sample', function(data) {
    //plot sample
   dataGenerator(data.sample);
});

socket.on('error', console.error.bind(console));
socket.on('message', console.log.bind(console));