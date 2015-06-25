# requires d3py
# only tested with python 2.7
from spyre import server

import numpy as np
import pandas as pd
import d3py
import matplotlib.pyplot as plt

class FruitInventoryApp(server.App):
	title = "Spyre Example With d3"

	inputs = [{	"input_type":'dropdown',
				"label": 'Type', 
				"options" : [	{"label": "Fruits", "value":"frt"},
								{"label": "Vegetables", "value":"veg"},
								{"label": "All", "value":"all"}],
				"variable_name": 'type',
	            "value": "all",
				"action_id":"submit_plot"}]

	controls = [{	"control_type" : "hidden",
					"label" : "show inventory",
					"control_id" : "submit_plot"}]

	outputs = [{	"output_type" : "plot",
					"output_id" : "plot1",
					"control_id" : "submit_plot",
					"tab" : "Matplotlib_Plot",
					"on_page_load" : True},
				{	"output_type" : "d3",
					"control_id" : "submit_plot",
					"output_id" : "d3_output",
					"tab" : "d3_Plot",
					"on_page_load" : True}]

	tabs = ["d3_Plot", "Matplotlib_Plot"]

	def getData(self, params):
		type_var = params['type']
		if type_var=="frt":
			count = [6,7,5,2]
			item = ['Apples','Oranges','Bananas','Watermelons']
		elif type_var=="veg":
			count = [3,1,7,8,2]
			item = ['Carrots','Spinach','Squash','Asparagus','Brocolli']
		else:
			count = [3,1,7,8,2,6,7,5,2]
			item = ['Carrots','Spinach','Squash','Asparagus','Brocolli','Apples','Oranges','Bananas','Watermelons']
		df = pd.DataFrame({'item':item, 'count':count})
		df = df[['item','count']]
		return df

	def getPlot(self, params):
		data = self.getData(params)  # get data
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['item']))
		width = 0.85  
		splt.bar(ind,data['count'], width)
		splt.set_ylabel('Count')
		splt.set_title('NBS Category Count')
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(data['item'].tolist())
		fig.autofmt_xdate(rotation=45)
		return fig

	def getD3(self, xlabel="item", ylabel="count"):
		df = pd.DataFrame({xlabel:[],ylabel:[]})
		p = d3py.PandasFigure(df)
		p += d3py.Bar(x = xlabel, y=ylabel)
		# p += d3py.Line(x = xlabel, y=ylabel)
		p += d3py.xAxis(x = xlabel)
		p += d3py.yAxis(y = ylabel)
		p.update()
		p.js.merge(p.js_geoms)
		d3 = {}
		d3['js'] = p.js
		d3['css'] = "%s\n%s"%(p.css, p.css_geoms)
		return d3

if __name__ == '__main__':
	app = FruitInventoryApp()
	app.launch(port=9092)
