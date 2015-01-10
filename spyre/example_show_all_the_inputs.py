# from spyre import spyre
# import spyre
import server

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import pi
import time

class SimpleSineApp(server.App):
	colors = [
	{"label":"Green", "value":'g'},
    {"label": "Red", "value":'r'}, 
    {"label": "Blue", "value":'b'}, 
    {"label": "Yellow", "value":'y'},
    ]

	title = "Simple Sine Wave"
	inputs = [{	"input_type":'text',
				"label": 'Title', 
				"value" : 'Simple Sine Wave',
				"variable_name": 'title', 
				"action_id" : "plot",
			},
			{	"input_type":'radiobuttons',
				"label": 'Function', 
				"options" : [
					{"label": "Sine", "value":"sin", "checked":True}, 
					{"label":"Cosine", "value":"cos"}
				],
				"variable_name": 'func_type', 
				"action_id" : "plot",
			},
			{	"input_type":'checkboxgroup',
				"label": 'Axis Labels', 
				"options" : [
					{"label": "x-axis", "value":1, "checked":True}, 
					{"label":"y-axis", "value":2}
				],
				"variable_name": 'axis_label', 
				"action_id" : "plot",
			},
			{	"input_type":'dropdown',
				"label": 'Line Color', 
				"options" : colors,
				"variable_name": 'color', 
				"action_id" : "plot",
			},
			{	"input_type":'slider',
				"label": 'frequency', 
				"variable_name": 'freq', 
				"value" : 2,
				"min" : 1, 
				"max" : 30,
				"action_id" : "plot",
			}]
	controls = [{	"control_type" : "button",
					"control_id" : "button1",
					"label" : "plot",
				},
				{	"control_type" : "button",
					"control_id" : "button2",
					"label" : "download",
				}]
	outputs = [{	"output_type" : "html",
					"output_id" : "html_id",
					"control_id" : "button1",
					"on_page_load" : True,
				},
				{	"output_type" : "plot",
					"output_id" : "plot",
					"control_id" : "button1",
					"on_page_load" : True,
				},
				{	"output_type" : "plot",
					"output_id" : "plot2",
					"control_id" : "button1",
					"on_page_load" : True,
				},
				{	"output_type" : "table",
					"output_id" : "table_id",
					"control_id" : "button1",
					"sortable" : True,
					"on_page_load" : True,
				},
				{	"output_type" : "download",
					"output_id" : "download_id",
					"control_id" : "button2",
				}]

	def getPlot(self, params):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)

		f = float(params['freq'])
		title = params['title']
		axis_label = map( int, params['axis_label'] )
		color = params['color']
		func_type = params['func_type']

		x = np.arange(0,6*pi,pi/50)
		splt.set_title(title)
		for axis in axis_label:
			if axis==1:
				splt.set_xlabel('x axis')
			if axis==2:
				splt.set_ylabel('y axis')
		if func_type=='cos':
			y = np.cos(f*x)
		else:
			y = np.sin(f*x)
		splt.plot(x,y,color=color)  # sine wave
		return fig

	# def getHTML(self,params):
	# 	f = int(params['freq'])
	# 	time.sleep(f)
	# 	return "hello world"
	
	def plot(self):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)

		f = float(params['freq'])
		title = params['title']
		axis_label = map( int, params['axis_label'] )
		color = params['color']
		func_type = params['func_type']

		x = np.arange(0,6*pi,pi/50)
		splt.set_title(title)
		for axis in axis_label:
			if axis==1:
				splt.set_xlabel('x axis')
			if axis==2:
				splt.set_ylabel('y axis')
		if func_type=='cos':
			y = np.cos(f*x)
		else:
			y = np.sin(f*x)
		splt.plot(x,y,color=color)  # sine wave
		return fig

	def plot2(self):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		x = np.arange(0,6*pi,pi/50)
		y = np.sin(f*x)
		splt.plot(x,y)  # sine wave
		return fig

	def html_id(self):
		return "hello world"

	def getData(self,params):
		count = [1,4,3]
		name = ['<a href="http://adamhajari.com">A</a>','B','C']
		df = pd.DataFrame({'name':name, 'count':count})
		time.sleep(2)
		return df

	def noOutput(self, input_params):
		return 0

app = SimpleSineApp()
app.launch(port=9096)
