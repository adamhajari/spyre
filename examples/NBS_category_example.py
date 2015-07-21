# tested with python2.7 and 3.4
from spyre import server

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NBSCategoriesApp(server.App):
	title = "Spyre Example"

	inputs = [{	'type' : 'slider',
				"label": 'Exclude First', 
				"min" : 0,"max" : 14,"value": 0, 
				"key": 'ex_first' }]

	controls = [{"type" : "button",
					"label" : "Make Matplotlib Graph",
					"id" : "submit_plot"},
				{"type" : "button",
					"label" : "Load Table",
					"id" : "load_table"}]

	outputs = [{"type" : "plot",
					"id" : "plot1",
					"control_id" : "submit_plot",
					"tab" : "Plot"},
				{"type" : "table",
					"id" : "table_id",
					"control_id" : "load_table",
					"tab" : "Table"},
				{"type" : "html",
					"id" : "custom_html",
					"tab" : "text"}]

	tabs = ["Plot", "Table", "text"]

	def getData(self, params):
		# cache values within the Launch object to avoid reloading the data each time
		ex_first = int(params['ex_first'])
		count = [620716,71294,50807,7834,5237,3278,2533,2042,1266,1165,980,962,747,712,679]
		name = ['Musician','Author','Book','Record Label','Actor','Public Figure ','Comedian','Producer','News/Media','Entertainer','Radio Station ','TV Show','Company','Local Business','Apparel']
		df = pd.DataFrame({'name':name, 'count':count})
		df = df[['name','count']]
		return df[ex_first:]

	def getPlot(self, params):
		output_id = params['output_id']
		data = self.getData(params)  # get data
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['name']))
		width = 0.85  
		splt.bar(ind,data['count'], width)
		splt.set_ylabel('Count')
		splt.set_title('NBS Category Count Plot 1')
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(data['name'].tolist())
		fig.autofmt_xdate(rotation=45)
		return fig

	def getHTML(self, params):
		return "<b>App Description: </b> <i>This</i> is where you could describe your app."

if __name__ == '__main__':
	app = NBSCategoriesApp()
	app.launch(port=9091)

