# from spyre import spyre
# import spyre
import server
server.config.include_df_index = True

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import pi
import time

class SimpleSineApp(server.App):
	colors = [
	{"label":"Green", "value":'g'},
    {"label": "Red", "value":'r', "checked":True}, 
    {"label": "Blue", "value":'b'}, 
    {"label": "Yellow", "value":'y'},
    ]

	title = "Simple Sine Wave"
	inputs = [{	"input_type":'text',
				"label": 'Title', 
				"value" : 'Simple Sine Wave',
				"variable_name": 'title', 
				"action_id" : "refresh",
			},
			{	"input_type":'radiobuttons',
				"label": 'Function', 
				"options" : [
					{"label": "Sine", "value":"sin", "checked":True}, 
					{"label":"Cosine", "value":"cos"}
				],
				"variable_name": 'func_type', 
				"action_id" : "refresh",
			},
			{	"input_type":'checkboxgroup',
				"label": 'Axis Labels', 
				"options" : [
					{"label": "x-axis", "value":"x", "checked":True}, 
					{"label":"y-axis", "value":"y"}
				],
				"variable_name": 'axis_label', 
				"action_id" : "refresh",
			},
			{	"input_type":'dropdown',
				"label": 'Line Color', 
				"options" : colors,
				"variable_name": 'color', 
				"action_id" : "refresh",
			},
			{	"input_type":'slider',
				"label": 'frequency', 
				"variable_name": 'freq', 
				"value" : 2,
				"min" : 1, 
				"max" : 30,
				"action_id" : "refresh",
			}]
	controls = [{	"control_type" : "button",
					"control_id" : "refresh",
					"label" : "refresh",
				},
				{	"control_type" : "button",
					"control_id" : "button2",
					"label" : "download",
				}]
	tabs = ["Tab1", "Tab2"]
	controls = [{	"control_type" : "button",
					"control_id" : "refresh",
					"label" : "refresh",
				},
				{	"control_type" : "button",
					"control_id" : "button2",
					"label" : "download",
				}]
	outputs = [{	"output_type" : "html",
					"output_id" : "html1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"output_type" : "plot",
					"output_id" : "plot1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"output_type" : "table",
					"output_id" : "table1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"output_type" : "plot",
					"output_id" : "plot2",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"output_type" : "download",
					"output_id" : "download_id",
					"control_id" : "button2",
					"on_page_load" : False,
				},
				{	"output_type" : "html",
					"output_id" : "html2",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"output_type" : "plot",
					"output_id" : "plot3",
					"control_id" : "refresh",
					"tab" : "Tab2"
				},
				{	"output_type" : "table",
					"output_id" : "table2",
					"control_id" : "refresh",
					"sortable" : True,
					"tab" : "Tab2"
				}]

	def getJsonData(self,params):
		count = [1,4,3]
		name = ['<a href="http://adamhajari.com">A</a>','B','C']
		return {'name':name, 'count':count}

	# def getData(self,params):
	# 	return df
	
	def table1(self,params):
		data = self.getJsonData(params)
		df = pd.DataFrame(data)
		return df

	def table2(self,params):
		f = float(params['freq'])
		func_type = params['func_type']
		x = np.arange(0,6*pi,pi/50)
		y1 = np.cos(f*x)
		y2 = np.sin(f*x)
		df = pd.DataFrame({"cos":y1,"sin":y2},index=x)
		df.index.name = "t"
		return df

	
	def plot3(self,params):
		axis_label = params['axis_label']
		color = params['color']
		df = self.table2(params)
		ax = df.plot(title=params['title'])
		ax.set_ylabel('y axis')
		ax.set_xlabel('x axis')
		return ax
	
	def plot1(self,params):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)

		f = float(params['freq'])
		title = params['title']
		axis_label = params['axis_label']
		color = params['color']
		func_type = params['func_type']

		x = np.arange(0,6*pi,pi/50)
		splt.set_title(title)
		for axis in axis_label:
			if axis=="x":
				splt.set_xlabel('x axis')
			if axis=="y":
				splt.set_ylabel('y axis')
		if func_type=='cos':
			y = np.cos(f*x)
		else:
			y = np.sin(f*x)
		splt.plot(x,y,color=color)  # sine wave
		return fig

	def plot2(self,params):
		data = self.table1(params)
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['name']))
		width = 0.85  
		splt.bar(ind,data['count'], width)
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(["A","B","C"])
		return fig

	def html1(self,params):
		return "hello world"

	def html2(self,params):
		func_type = params['func_type']
		axis_label = params['axis_label']
		color = params['color']
		freq = params['freq']
		html = "function type: {} <br>axis label: {}<br>color: {}<br>frequency: {}".format(func_type, axis_label, color, freq)
		return html

	def noOutput(self, input_params):
		return 0

if __name__ == '__main__':
	app = SimpleSineApp()
	app.launch(port=9096)
