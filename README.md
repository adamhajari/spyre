Secure Spyre
=========

Spyre is a Web Application Framework for providing a simple user interface for Python data projects.


Requirements
----
Spyre runs on the minimalist python web framework, **[cherrypy]**, with **[jinja2]** templating. Spyre is all about data and data visualization, so you'll also need **[pandas]** and **[matplotlib]**.


Installation
----
```bash
    $ pip install git+https://github.com/Dana-Farber/spyre
```


The Simplest of Examples, with User Authentication (Login)
----
Here's a very simple spyre example that shows the primary components of a spyre app
```python
from spyre import server

class SimpleApp(server.App):
	title = "Simple App"
	inputs = [{
		"type": "text",
		"key": "words",
		"label": "write words here",
		"value": "hello world",
		"action_id": "simple_html_output"
	}]

	outputs = [{
		"type": "html",
		"id": "simple_html_output"
	}]

	def getHTML(self, params):
		words = params["words"]
		return "Here's what you wrote in the textbox: <b>%s</b>" % words

USERS={"alice":"secret"}

from cherrypy.lib import auth_digest #must import this to compute ha1 digest
digest_auth = {'/': {'tools.auth_digest.on': True,
               'tools.auth_digest.realm': 'wonderland',
               'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
               'tools.auth_digest.key': 'a565c27146791cfb',
}}

app = SimpleApp()
app.launch(config=digest_auth)
```

The SimpleApp class inherits server.App which includes a few methods that you can override to generate outputs. In this case we want our app to display HTML (just text for now) so we'll overide the getHTML method. This method should return a string.

We also need to specify the attributes of our inputs and outputs which we can do by defining the App's inputs and outputs variables.

### inputs ###
This is a list of dictionaries, one dictionary for each input element. In our simple example above, there's only one input, of type "text". We give it a label and initial value with the keys "label" and "value".  The value from this input will be used as an input parameter when generating the outputs (html in this case), so we need to also give it a key that we can reference in the getHTML method. "action_id" is an optional variable that equals id from either an output or a control element (we'll get to controls in the next example). When action_id is defined, a change in the input will result in either an update to the referenced output or a call to the functions connected to the referenced control. 

### outputs ###
An output's `type` can be "plot", "image", "table", "html", or "download". In addition to the type, we also need to provide a unique id (must start with a letter). If this output is suppose to get updated on execution of one of the controls specified in the list of controls, we need to also specify the control_id of that controller (which we'll see in the next example). All outputs get generated on page load by default. If we want an output *not* to load on the page load, we can also specify an "on_page_load" attribute and set it to False.

### controls ###
Controls are one mechanism by which a spyre app can update its outputs. A control's `id` can be referenced by either an input or an output. When an output references the control's id, executing the control updates that output. When an input references the controld's id (via the "action_id"), updating the input executes the control. The two control `type` options are "button" and "hidden". "button" will add a button to the left panel. No control is added to the left-panel for control_types "hidden" (this is useful for linking a single input action to multiple outputs).

### generating an output ###
Let's get back to our getHTML method. Notice that it takes a single argument: params. params is a dictionary containing:

1. all of the input values (where the key is specified in the input dictionary)
2. the output_id for the output that needs to get created. You usually don't need to do anything with this.

With the exception of the input type "checkboxgroup", the value of each of the params elements is a string. The string returned by getHTML will be displayed in the right panel of our Spyre app.

### launching the app ###
To launch our app we just need to create an instance of our SimpleApp class and call the launch method. Assuming you name this file "simple_app_example.py" you can launch this app from the command line with:
```bash
    $ python simple_app_example.py
```
The output will indicate where the app is being served (http://127.0.0.1:8080 by default)

If all goes smoothly your spyre app should look like this:

![simple app example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/simple_app_screenshot.png)



Example 2: Tabs and Tables
----
Let's look at another example to introduce controls, tabs, and a second output type, tables. Many apps will require multiple outputs. In these cases, it's often cleaner to put each output in a separte tab. 

In the example below we'll show historical stock data in a line graph and a table, each in it's own tab.  Since inputs can only have a single action_id (and we have two outputs), we'll need to introduce a button control in order to update both outputs.


   >*Note to python 3 users:* Replace `from urllib2 import urlopen` with `from urllib.request import urlopen`


```python
from spyre import server

import pandas as pd
from urllib2 import urlopen
import json

class StockExample(server.App):
	title = "Historical Stock Prices"

	inputs = [{
		"type": 'dropdown',
		"label": 'Company', 
		"options": [
			{"label": "Google", "value": "GOOG"},
			{"label": "Yahoo", "value": "YHOO"},
			{"label": "Apple", "value": "AAPL"}
		],
		"key": 'ticker', 
		"action_id": "update_data"
	}]

	controls = [{
		"type": "hidden",
		"id": "update_data"
	}]

	tabs = ["Plot", "Table"]

	outputs = [
		{
			"type": "plot",
			"id": "plot",
			"control_id": "update_data",
			"tab": "Plot"
		}, { 
			"type": "table",
			"id": "table_id",
			"control_id": "update_data",
			"tab": "Table",
			"on_page_load": True
		}
	]

	def getData(self, params):
		ticker = params['ticker']
		# make call to yahoo finance api to get historical stock data
		api_url = 'https://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=3m/json'.format(ticker)
		result = urlopen(api_url).read()
		data = json.loads(result.decode("utf8").replace('finance_charts_json_callback( ','')[:-1])  # strip away the javascript and load json
		self.company_name = data['meta']['Company-Name']
		df = pd.DataFrame.from_records(data['series'])
		df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
		return df

	def getPlot(self, params):
		df = self.getData(params).set_index('Date').drop(['volume'],axis=1)
		plt_obj = df.plot()
		plt_obj.set_ylabel("Price")
		plt_obj.set_title(self.company_name)
		fig = plt_obj.get_figure()
		return fig

app = StockExample()
app.launch(port=9093)

```
There's a few things to point out here:

1. This app uses a dropdown input type. It still has a label and variable_name (that's common to all input types), but you now also need to enumerate all of the options for the dropdown menu. For each of the options, "label" is displayed in the menu and "value" is value of that input variable when that option is selected.
2. The tabs variable is a list of tab names. These names are used as labels for the tabs as well as html ids so they can't contain any spaces.
3. There's a "table" output type that requires all of the same attribute types as the plot output type.
4. Additionally, we need to specify a "tabs" attribute for each output. This should match the name of one of the items listed in the tabs list.
5. The control variable has control_type, label, and control_id attributes. Each output has an optional control_id attribute which can be used to reference a control. When a control action is taken (such as clicking a button), every output that references that control will be updated.

We're also overriding getData, a method which should fetch or generate the data that will go into the table.  Just like getPlot, it takes a params argument which is a dictionary containing all of our input variables. getData should return a pandas DataFrame.

Launch the app just as you did in the previous example. The app now has two tabs.

### Plot tab ###
![stocks graph tab example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/stocks_graph_screenshot.png)


### Table tab ###
![stocks table tab example screenshot](https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/stocks_table_screenshot.png)




License
----

MIT


Acknowledgements
----

Much of the work that went into creating Spyre happened during hack weeks at **[Next Big Sound]**. If you're a talented engineer or data scientist looking for a great place to work, check out their about page for job openings!


[cherrypy]:http://docs.cherrypy.org/en/latest/install.html
[jinja2]:http://jinja.pocoo.org/docs/dev/intro/#installation
[pandas]:http://pandas.pydata.org/pandas-docs/stable/install.html#recommended-dependencies
[matplotlib]:http://matplotlib.org/users/installing.html
[simple sine example screenshot]:https://raw.githubusercontent.com/adamhajari/spyre/master/examples/screenshots/simple_sine_screenshot.png
[Next Big Sound]: https://www.nextbigsound.com/about
