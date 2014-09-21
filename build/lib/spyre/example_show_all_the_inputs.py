# from spyre import server
import server

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

class SimpleSineLaunch(server.Launch):
	colors = [
	{"label":"Green", "value":'g'},
    {"label": "Red", "value":'r'}, 
    {"label": "Blue", "value":'b'}, 
    {"label": "Yellow", "value":'y'},
    ]

	templateVars = {"title" : "Simple Sine Wave",
					"inputs" : [{	"input_type":'text',
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
									"value" : 5,
									"min" : 1, 
									"max" : 30,
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
								},
								{	"output_type" : "no_output",
									"output_id" : "make_alert",
									"alert_message" : "you pressed a button",
									"control_id" : "button1",
								}]
				}

	def getPlot(self, params):
		f = params['freq']
		title = params['title']
		axis_label = map( int, params['axis_label'] )
		color = params['color']
		func_type = params['func_type']

		x = np.arange(0,6*pi,pi/50)
		plt.title(title)
		for axis in axis_label:
			if axis==1:
				plt.xlabel('x axis')
			if axis==2:
				plt.ylabel('y axis')
		if func_type=='cos':
			y = np.cos(f*x)
		else:
			y = np.sin(f*x)
		plt.plot(x,y,color=color)  # sine wave
		return plt.gcf()

	def noOutput(self, input_params):
		return 0

l = SimpleSineLaunch()
l.launch(port=9096)
