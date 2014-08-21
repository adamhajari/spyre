function getPlot(container, entity_id, metric_id, callback){
	var margin = {top: 30, right: 20, bottom: 30, left: 70},
		width = 800 - margin.left - margin.right,
		height = 350 - margin.top - margin.bottom;

	var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

	var x = d3.time.scale().range([0, width]);

	var y = d3.scale.linear().range([height, 0]);

	var xAxis = d3.svg.axis().scale(x)
		.orient("bottom").ticks(5);

	var yAxis = d3.svg.axis().scale(y)
		.orient("left").ticks(5);

	var valueline = d3.svg.line()
		.x(function(d) { return x(d.datetime); })
		.y(function(d) { return y(d.value); });

	var svg = d3.select(container)
		.append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	console.log("hey")
	// Get the data
	var load = "arg1="+entity_id+"&arg2="+metric_id;
	d3.xhr("/data")
	.header("Content-Type","application/x-www-form-urlencoded")
	.send("POST",load, function(error, respone_data){
		console.log(load)
		data_pre = JSON.parse(respone_data['response']);
		data = data_pre['data']
		console.log(data_pre)
		data.forEach(function(d) {
			d.datetime = parseDate(d.datetime);
			d.value = +d.value;
		});

		// console.log(data);

		// Scale the range of the data
		x.domain(d3.extent(data, function(d) { return d.datetime; }));
		y.domain([0, d3.max(data, function(d) { return d.value; })]);
		svg.append("path") // Add the valueline path.
			.attr("class", "line")
			.attr("d", valueline(data));
		// console.log(svg);

		svg.append("g") // Add the X Axis
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);

		svg.append("g") // Add the Y Axis
			.attr("class", "y axis")
			.call(yAxis);
		callback(1);
	});
};


function loadtable(datax) {
	data = datax;
	var first_key = Object.keys(data[0])[0]
	transform(first_key);
}

function transform(attrName) {
	console.log(data);
    d3.select("tbody").selectAll("tr").remove();

    data.forEach(function(d) {
		d[attrName] = d[attrName]+'';
	});

// Header
    var th = d3.select("thead").selectAll("th")
            .data(jsonToArray(data[0]))
          .enter().append("th")
            .attr("onclick", function (d) { return "transform('" + d[0] + "');";})
            .text(function(d) { return d[0]; })

// Rows
    var tr = d3.select("tbody").selectAll("tr")
            .data(data)
          .enter().append("tr")
            .sort(function (a, b) { return a == null || b == null ? 0 : stringCompare(a[attrName], b[attrName]); });

// Cells
    var td = tr.selectAll("td")
            .data(function(d) { return jsonToArray(d); })
          .enter().append("td")
            .attr("onclick", function (d) { return "transform('" + d[0] + "');";})
            .text(function(d) { return d[1]; });
}

function stringCompare(a, b) {
    a = a.toLowerCase();
    b = b.toLowerCase();
    return a > b ? 1 : a == b ? 0 : -1;
}

function jsonKeyValueToArray(k, v) {return [k, v];}

function jsonToArray(json) {
    var ret = new Array();
    var key;
    for (key in json) {
        if (json.hasOwnProperty(key)) {
            ret.push(jsonKeyValueToArray(key, json[key]));
        }
    }
    return ret;
};