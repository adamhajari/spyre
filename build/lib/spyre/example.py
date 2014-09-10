# from spyre import server
import server

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MyLaunch(server.Launch):
	templateVars = {"title" : "Spyre Example",
					"inputs" : [
						{	'input_type' : 'text',
							"label": 'Exclude First', 
							"value": 0, 
							"variable_name": 'ex_first', 
						},
						{	"input_type" :'text',
							"label": 'Max Categories To Show', 
							"value": 15, 
							"variable_name": 'max_incl', 
						},
						],
					"controls" : [
						{	"control_type" : "button",
							"control_name" : "button1",
							"label" : "Make Matplotlib Graph",
							"button_id" : "submit_plot",
							"text_fields" : []
						},
						{	
							"control_type" : "button",
							"control_name" : "button2",
							"label" : "Make Matplotlib Graph 2",
							"button_id" : "submit_plot2",
							"text_fields" : []
						},
						{	"control_type" : "button",
							"control_name" : "table_button",
							"label" : "Load Table",
							"button_id" : "load_table",
							"text_fields" : []
						}
					],
					"tabs" : ["Plot1", "Plot2", "Table", "html"],
					"outputs" : [
						{	"output_type" : "image",
							"output_id" : "image1",
							"control_name" : "button1",
							"tab" : "Plot1",
							"on_page_load" : "true",
						},
						{	"output_type" : "image",
							"output_id" : "image2",
							"control_name" : "button2",
							"tab" : "Plot2",
						},
						{	"output_type" : "table",
							"output_id" : "table_id",
							"control_name" : "table_button",
							"tab" : "Table",
						},
						{	"output_type" : "html",
							"output_id" : "custom_html",
							"control_name" : "button1",
							"tab" : "html",
							"on_page_load" : "true",
						}
					]
				}

	# cache values to avoid reloading the data each time
	data_params = None
	data = pd.DataFrame()

	def getData(self, input_params):
		# cache values within the Launch object to avoid reloading the data each time
		if input_params != self.data_params:
			ex_first = int(input_params['ex_first'])
			max_incl = int(input_params['max_incl'])
			count = [620716,71294,50807,7834,5237,3278,2533,2042,1266,1165,980,962,747,712,679]
			name = ['Musician','Author','Book','Record Label','Actor','Public Figure ','Comedian','Producer','News/Media','Entertainer','Radio Station ','TV Show','Company','Local Business','Apparel']
			df = pd.DataFrame({'name':name, 'count':count})
			df = df[['name','count']]
			self.data = df[ex_first:max_incl]
			self.data_params = input_params
		return self.data

	def getPlot(self, input_params):
		output_id = input_params['output_id']
		data = self.getData(input_params)  # get data
		if output_id=="image1":
			return self.getPlot1(data)
		else:
			return self.getPlot2(data)

	def getPlot1(self, data):
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

	def getPlot2(self, data):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['name']))
		width = 0.85  
		splt.bar(ind,data['count'], width, color='orange')
		splt.set_ylabel('Count')
		splt.set_title('NBS Category Count Plot 2')
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(data['name'].tolist())
		fig.autofmt_xdate(rotation=45)
		return fig

	def getHTML(self, input_params):
		return "<b>App Description: </b> <i>This</i> is where you could describe your app."

ml = MyLaunch()
ml.launch(port=9091)

