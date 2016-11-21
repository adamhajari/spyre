# from spyre import spyre
# import spyre
try:
	from . import server
except:
	import server
server.include_df_index = True

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import pi
import time

class TestApp2(server.App):
	title = "Test App 2"
	inputs = [{	"type":'slider',
				"label": 'frequency', 
				"key": 'freq', 
				"value":2, "min":1, "max":10,
				"action_id":"refresh",
			},
			{	"type":'multiple',
				"label": 'multiple', 
				"options" : [
					{"label": "a", "value":"A", "checked":True}, 
					{"label": "b", "value":"B"},
					{"label": "e", "value":"E", "checked":True},
					{"label": "f", "value":"F"},
					{"label": "g", "value":"G", "checked":True},
					{"label": "h", "value":"H"},
					{"label": "i", "value":"I"},
					{"label": "j", "value":"J"},
					{"label": "k", "value":"K"},
					{"label": "l", "value":"L"},
					{"label": "m", "value":"M"},
					{"label": "n", "value":"N"},
					{"label": "odfeweioufjkjoifdjiojoijfdsiojdfsfdsfefwfefsefwfwewfe", "value":"xoxo"},
					{"label": "c", "value":"C"}
				],
				"key": 'multi', 
				"action_id" : "refresh",
			},]

	controls = [{"type":"button", "id":"refresh", "label":"refresh"}]

	outputs = [ {"type":"html", "id":"htmlx", "control_id":"refresh"},
				{"type":"plot", "id":"plot1", "control_id":"refresh"},
				{"type":"table", "id":"table1", "control_id":"refresh"}]

	def getData(self,params):
		f = float(params['freq'])
		x = np.arange(0,6*pi,pi/50)
		y1 = np.cos(f*x)
		y2 = np.sin(f*x)
		df = pd.DataFrame({"cos":y1,"sin":y2},index=x)
		df.index.name = "t"
		return df

	def getHTML(self,params):
		multi = params['multi']
		if 'A' in multi:
			return "A's here"
		return multi

if __name__ == '__main__':
	app = TestApp2()
	app.launch(port=9095)
