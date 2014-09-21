# from spyre import server
import server

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

class MyLaunch(server.Launch):
	templateVars = {"title" : "Decaying Sine Wave",
					"inputs" : [
						{	"input_type":'slider',
							"label": 'Amplitude', 
							"min" : 0,
							"max" : 5,
							"value" : 1,
							"variable_name": 'amp', 
						},
						{	"input_type":'slider',
							"label": 'Frequency', 
							"min" : 0,
							"max" : 100,
							"value" : 50,
							"variable_name": 'freq', 
						},
						{	"input_type":'slider',
							"label": 'Decay Rate', 
							"min" : 0,
							"max" : 2,
							"step" : 0.01,
							"value" : 0.5,
							"variable_name": 'decay', 
						}
						],
					"controls" : [
						{	"control_type" : "button", 
							"control_name" : "button1",
							"label" : "plot",
							"control_id" : "submit_plot",
						}
					],
					"outputs" : [
						{	"output_type" : "image",
							"output_id" : "plot",
							"control_id" : "submit_plot",
							"on_page_load" : "true",
						}
					]
				}

	def getPlot(self, params):
		A = float(params['amp'])
		f = float(params['freq'])
		d = float(params['decay'])
		x = np.arange(0,6*pi,pi/50)
		y1 = A*np.sin(f*x/(2*pi))
		y2 = np.exp(-x*d)
		y3 = A*np.sin(f*x/(2*pi))*np.exp(-x*d)
		fig = plt.figure()
		splt1 = fig.add_subplot(3,1,1)
		splt1.plot(x,y1)  # sine wave
		splt1.axes.get_xaxis().set_visible(False)
		splt2 = fig.add_subplot(3,1,2)
		splt2.plot(x,y2)  # exponential decay
		splt2.axes.get_xaxis().set_visible(False)
		splt3 = fig.add_subplot(3,1,3)
		splt3.plot(x,y3)  #sine wave decay
		return fig

ml = MyLaunch()
ml.launch(port=9094)
