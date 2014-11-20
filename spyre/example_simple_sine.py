# from spyre import server
import server

import numpy as np
from matplotlib import pyplot as plt

class SimpleApp(server.App):
	title = "Simple App"
	inputs = [{	"input_type":"text",
				"variable_name":"freq",
				"value":5,
				"acion_id":"sine_wave_plot"}]

	outputs = [{"output_type":"plot",
				"output_id":"sine_wave_plot",
				"control_id"
				"on_page_load":True }]

	def getPlot(self,params):
		f = int(params['freq'])
		x = np.arange(1,6,0.01)
		y = np.sin(f*x)
		plt.plot(x,y)
		return plt.gcf()  # Note: if you have more that one plot output, don't use the gcf method.


app = SimpleApp()
app.launch()