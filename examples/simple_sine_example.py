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
								}],
					"controls" : [{	"control_type" : "button",
									"control_id" : "button1",
									"label" : "plot",
								}],
					"outputs" : [{	"output_type" : "image",
									"output_id" : "plot",
									"control_id" : "button1",
									"on_page_load" : "true",
								}]
				}

	def getPlot(self, params):
		f = float(params['freq'])
		x = np.arange(0,6*pi,pi/50)
		y = np.sin(f*x/(2*pi))
		fig = plt.figure()
		splt1 = fig.add_subplot(1,1,1)
		splt1.plot(x,y)  # sine wave
		return fig

l = SimpleSineLaunch()
l.launch(port=9095)
