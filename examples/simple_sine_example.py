from spyre import server

import matplotlib.pyplot as plt
import numpy as np

class SimpleSineApp(server.App):
	title = "Simple Sine App"
	inputs = [{ "type":"slider",
				"key":"freq",
				"value":5, "max":10,
				"action_id":"sine_wave_plot"},
			{ "type":"text",
				"key":"text",
				"value":"hello world",
				"action_id":"sine_wave_plot"}]

	outputs = [{"type":"plot",
				"id":"sine_wave_plot"}]

	def getPlot(self, params):
		f = float(params['freq'])
		x = np.arange(0,2*np.pi,np.pi/150)
		y = np.sin(f*x)
		fig = plt.figure()
		splt1 = fig.add_subplot(1,1,1)
		splt1.plot(x,y)
		return fig

if __name__ == '__main__':
	app = SimpleSineApp()
	app.launch()
