
/**
 * 
 * Initialize the X and Y scale of the data.
 * @param {*} data 
 * @param {*} dimensions 
 * 
 */
function initializeScale(data, dimensions){
    var x = d3.scaleLinear()
              .domain(d3.extent(data, function(d) { return d.year; }))
              .range([ 0, dimensions.width ]);

    var y = d3.scaleLinear()
              .domain([0, 200000])
              .range([ dimensions.height, 0 ]);

    return {xScale: x, yScale: y}
}

/**
 * Add the x and y axis of the SVG canvas
 * 
 * @param {} svg The DOM element representing an SVG.
 * @param {} dimensions the dimensions of the canvas.
 * @param {} xScale The D3 scale function for the x-axis
 * @param {} yScale The scale function for the y-axis
 * 
 */
function addXYAxis(svg, dimensions, xScale, yScale){

    svg.append("g")
        .attr("transform", "translate(0," + dimensions.height + ")")
        .call(d3.axisBottom(xScale).ticks(5));

    // Add Y axis
    svg.append("g")
       .call(d3.axisLeft(yScale));
}


/**
 * Initialize the SVG element for drawing the chart
 * 
 * @param {} dimensions The object storing the dimensions of the SVG canvas
 * @param {} margin The object storing the margin of the SVG canvas
 * 
 */
function initializeSVG(margin, dimensions){
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", dimensions.width + margin.left + margin.right)
        .attr("height", dimensions.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
    return svg;
}


/**
 * Stack the data 
 * 
 * @param {} data The data that we want to stack 
 * @param {} keys The keys of the data, (e.g. the column of the CSV)
 * @return The properly stacked data, 
 * 
 */
function stackData(data, keys){
    var stacker = d3.stack().keys(keys);
    var stackedDataTemp = stacker(data);
    var stackedData = []
    for (const singleStackTemp of stackedDataTemp){
        var singleStack = []; // a single "stack" of the data.
        for (const element of singleStackTemp){
            singleStack.push({
            year: element.data.year, 
            name: singleStackTemp.key,
            value: element.slice(0,3)});
        }
        stackedData.push(singleStack);
    }
    return stackedData;
}


/**
 * Display the are chart using the stacked data
 * 
 * @param {*} stackedData The stacked data ready to be processed (i.e. data that went throught the stackData function)
 * @param {*} color The function representing the color pallet. It takes in a key and return the color it should be
 * 
 */
function displayArea(stackedData, color, xScale, yScale){
    var areaGenerator = d3.area()
        .x(function(d) { return xScale(d.year)})
        .y0(function(d) { return yScale(d.value[0]) })
        .y1(function(d) { return yScale(d.value[1]) });
    
    // Show the areas
    svg
    .selectAll("mylayers")
    .data(stackedData)
    .enter()
    .append("path") 
        .style("fill", function(d) { return color(d[0].name)})
        .attr("d", d => areaGenerator(d))
}


// set the dimensions and margins of the graph
var dimensions = {height: 666, width: 1000};
var margin = {top: 20, right: 30, bottom: 30, left: 60};
var csvPath = "https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/5_OneCatSevNumOrdered_wide.csv";

// append the svg object to the body of the page
var svg = initializeSVG(margin, dimensions);

//Read the data
d3.csv(csvPath, function(data) {
    var keys = data.columns.slice(1);
    // color palette
    var color = d3.scaleOrdinal()
        .domain(keys)
        .range(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999']);
    var scales = initializeScale(data, dimensions);
    addXYAxis(svg, dimensions, scales.xScale, scales.yScale);

    var stackedData = stackData(data, keys)
    displayArea(stackedData, color, scales.xScale, scales.yScale)
})