Spyre
=========

Spyre is a Web Application Framework for providing a simple user interface for Python data projects.


Requirements
----
Spyre runs on the minimalist python web framework, **[cherrypy]**, with **[jinja2]** templating. At it's heart, spyre is about data and data visualization, so you'll also need **[pandas]** and **[matplotlib]**.


Installation
----
```
    $ pip install dataspyre
```


The Simplest of Examples
----
Here's a very simple spyre example to showcase the primary components of a spyre app
```
from spyre import server

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

class SimpleSineLaunch(server.Launch):
	templateVars = {"title" : "Simple Sine Wave",
					"inputs" : [{	"input_type":'text',
									"label": 'Frequency', 
									"value" : 5,
									"variable_name": 'freq', 
									"action_id" : "plot",
								}],
					"controls" : [{	"control_type" : "button",
									"control_id" : "button1",
									"label" : "plot",
								}],
					"outputs" : [{	"output_type" : "plot",
									"output_id" : "plot",
									"control_id" : "button1",
									"on_page_load" : True,
								}]
				}

	def getPlot(self, params):
		f = float(params['freq'])
		x = np.arange(0,6*pi,pi/50)
		y = np.sin(f*x)
		fig = plt.figure()
		splt1 = fig.add_subplot(1,1,1)
		splt1.plot(x,y)  # sine wave
		return fig

l = SimpleSineLaunch()
l.launch(port=9096)
```
The SimpleSineLauncher class inherits server.Launch which includes a few methods that you can override to generate outputs. In this case we want our app to display a Plot so we'll overide the getPlot method. This method should return a matplotlib figure.

We also need to define a dictionary named templateVars, which will be responsible for generating all of the html and javascript for our app.  All apps have three main user-facing components:
* inputs 
* controls
* outputs

which are all defined by the templateVars dictionary.

### inputs ###
This is a list of input dictionaries. In our simple example above, there's only one input, of type "text". We give it a label and initial value with the keys "label" and "value".  The value from this input will be used to generate an output (a plot in this case), so we need to also give it a variable_name. Finally, "action_id" is an optional variable that equals either an output_id from the list of outputs, or a control_id from the list of controls. When this variable is defined, a change in the input will result in an update to the referenced output, or a call to the function connected to the referenced control. 

### controls ###
Controls allow your app to update multiple outputs simultaneously. The output_id here can be referenced by either an input or an output. When outputs reference the output_id, executing the control updates that output. When an input references the controld_id, updating the input executes the control. In this case, the plot output references the control_id for our button controller, so pressing the button will update the plot using the parameters specified by the input. The two control_types are "button" and "hidden". "button" will add a button to the left panel. No control is added to the left-panel for control_types "hidden".

### outputs ###
output_types can be a "plot", "table", or "html". In addition to output_type, we also need to provide a unique output_id. If this output gets generated/updated on execution of one of the controls specified in the list of controls, we need to also specify the control_id of that controller. In the case of our simple example, pressing the button (with control_id="button1") generates our plot so we must reference that button's control_id. If we want this output to load on the page load, we can also set "on_page_load" to True (this is false by default).

### generating a plot ###
Let's get back to our getPlot method. Notice that it takes a single argument: params. params is a dictionary containing:

1. all of the input values (with key equal to the variable_name specified in the input dictionary)
2. the output_id for the output being created.

For this simple example you can ignore the output_id (it'll be useful when defining multiple outputs of the same type). The value of each of the params is a string. In this example our one input variable represents a frequency, which is a number, so we'll need to cast it as a float before we use it.  The matplotlib figure returned by getPlot will be displayed in the right panel of our Spyre app.

### launching the app ###
To launch our app we just need to create an instance of our SimpleSineLaunch class and call the launch method. The launch method takes to optional parameters: host and port. By default, apps are served locally on port 8080. Set host='0.0.0.0' to serve your app to external traffic.

Assuming you name this file "simple_sine_example.py" you can launch this app from the command line with:
```
    $ python simple_sine_example.py
```
The output will indicate where the app is being served (usually something like http://127.0.0.1:9096)

If all goes smoothly your spyre app should look like this:

![simple sine example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/simple_sine_screenshot.png)

Example 2: Tabs and Tables
----
Let's look at another example to introduce tabs and a second output type, tables. Many apps will require multiple outputs. In these cases, it's often cleaner to put each output in a separte tab. In the example below we'll show historical stock data in a line graph and a table, each in it's own tab. Here's the code:

```
from spyre import server

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import urllib2
import json
from datetime import datetime

class MyLaunch(server.Launch):
	templateVars = {"title" : "Historical Stock Prices",
					"inputs" : [
						{	"input_type":'dropdown',
							"label": 'Company', 
							"options" : [
								{"label": "Google", "value":"GOOG"},
								{"label": "Yahoo", "value":"YHOO"},
								{"label": "Apple", "value":"AAPL"}
							],
							"variable_name": 'ticker', 
							"action_id": "update_data"
						}
						],
					"controls" : [
						{	"control_type" : "hidden",
							"label" : "get historical stock prices",
							"control_id" : "update_data",
						}
					],
					"tabs" : ["Plot", "Table"],
					"outputs" : [
						{	"output_type" : "plot",
							"output_id" : "plot",
							"control_id" : "update_data",
							"tab" : "Plot",
							"on_page_load" : True,
						},
						{	"output_type" : "table",
							"output_id" : "table_id",
							"control_id" : "update_data",
							"tab" : "Table",
							"on_page_load" : True,
						}
					]
				}

	# cache values within the Launch object to avoid reloading the data each time
	data_params = None
	data = pd.DataFrame()

	def getData(self, params):
		if params != self.data_params:
			ticker = params['ticker']
			# make call to yahoo finance api to get historical stock data
			api_url = 'https://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=3m/json'.format(ticker)
			result = urllib2.urlopen(api_url)
			r = result.read()
			data = json.loads(r.replace('finance_charts_json_callback( ','')[:-1])  # strip away the javascript and load json
			# make call to yahoo finance api to get historical stock data
			self.company_name = data['meta']['Company-Name']
			df = pd.DataFrame.from_records(data['series'])
			df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
			self.data = df
			self.data_params = ticker
		return self.data

	def getPlot(self, params):
		df = self.getData(params)  # get data
		dates = pd.DatetimeIndex(df['Date'])
		fig = plt.figure()
		splt = fig.add_subplot(1,1,1)
		splt.plot_date(dates, df['close'], fmt='-', label="close")
		splt.plot_date(dates, df['high'], fmt='-', label="high")
		splt.plot_date(dates, df['low'], fmt='-', label="low")
		splt.set_ylabel('Price')
		splt.set_xlabel('Date')
		splt.set_title(self.company_name)
		splt.legend(loc=2)
		splt.xaxis.set_major_formatter( DateFormatter('%m-%d-%Y') )
		fig.autofmt_xdate()
		return fig

ml = MyLaunch()
ml.launch(port=9093)

```
There's a few things to point out here. Let's start by looking at templateVars:

1. This app uses a dropdown input type. It still has a label and variable_name (that's common to all input types), but you now also need to enumerate all of the options for the dropdown menu. For each of the options, "label" is displayed in the menu and "value" is value of the vairable that gets passed around with the params when that option is selected.
2. The values for the "tabs" key is a list of tab names. These names are used as labels for the tabs as well as html ids so they can't contain any spaces.
3. Theres a "table" output type that requires all of the same parameters as the plot output type.
4. Additionally, we need to specify a "tabs" parameter for the outputs. This should match the name of one of the items listed in the tabs list.

We're also overriding getData, a method which should fetch or generate the data that will go into the table.  Just like getPlot, it takes a params argument which is a dictionary containing all of our input params. getData should return a pandas DataFrame.


> **Note:** getData makes a call to a yahoo finance api. We're also going to plot this same data, so we'll just have getPlot call getData. Since we don't want to have to make two calls to the yahoo api, we cache the data the first time we call getData and use the cached version unless the input params change. 

Launch the app just as you did in the previous example. The app now has two tabs.

### Plot tab ###
![stocks graph tab example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/stocks_graph_screenshot.png)


### Table tab ###
![stocks table tab example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/stocks_table_screenshot.png)




License
----

MIT


[cherrypy]:http://docs.cherrypy.org/en/latest/install.html
[jinja2]:http://jinja.pocoo.org/docs/dev/intro/#installation
[pandas]:http://pandas.pydata.org/pandas-docs/stable/install.html#recommended-dependencies
[matplotlib]:http://matplotlib.org/users/installing.html
[simple sine example screenshot]:https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/simple_sine_screenshot.png
