from spyre import server

import matplotlib.pyplot as plt
import numpy as np

class SimpleSineApp(server.App):
	title = "Simple Sine App"
	inputs = [{ "input_type":"text",
				"variable_name":"freq",
				"value":5,
				"action_id":"sine_wave_plot"}]

	outputs = [{"output_type":"plot",
				"output_id":"sine_wave_plot",
				"on_page_load":True }]

	def getPlot(self, params):
		f = float(params['freq'])
		x = np.arange(0,2*np.pi,np.pi/150)
		y = np.sin(f*x)
		fig = plt.figure()
		splt1 = fig.add_subplot(1,1,1)
		splt1.plot(x,y)
		return fig

app = SimpleSineApp()
app.launch()
