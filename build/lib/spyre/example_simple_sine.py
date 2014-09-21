# from spyre import server
import server

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
