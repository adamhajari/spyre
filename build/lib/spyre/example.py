# from spyre import server
import server
import numpy as np
import pandas as pd
import d3py
import matplotlib.pyplot as plt

class MyLaunch(server.Launch):
	templateVars = {"title" : "Spyre Example",
					"shared_fields" : [
								{"label": 'Exclude First', "value": 0, "variable_name": 'ex_first', "input_type":'text'},
								{"label": 'Max Return', "value": 15, "variable_name": 'max_incl', "input_type":'text'},
						],
					"controls" : [
						{"output_type" : "d3",
							"control_type" : "button",
							"control_name" : "button1",
							"button_label" : "Make d3 Bar Plot",
							"button_id" : "submit-d3",
							"text_fields" : []
						},
						{"output_type" : "image",
							"control_type" : "button",
							"control_name" : "button2",
							"output_name" : "image",
							"button_label" : "Make Matplotlib Graph",
							"button_id" : "submit-plot",
							"on_page_load" : "true",
							"text_fields" : []
						},
						{"output_type" : "image",
							"control_type" : "button",
							"control_name" : "button3",
							"output_name" : "image2",
							"button_label" : "Make Matplotlib Graph 2",
							"button_id" : "submit-plot2",
							"text_fields" : []
						},
						{"output_type" : "table",
							"control_type" : "button",
							"control_name" : "button4",
							"button_label" : "Load Table",
							"button_id" : "load-table",
							"text_fields" : []
						}
					]
				}

	# cache values within the Launch object to avoid reloading the data each time
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
			self.data = df[ex_first:max_incl]
			self.data_params = input_params
		return self.data

	def getPlot(self, input_params):
		data = self.getData(input_params)  # get data
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['name']))
		width = 0.85  
		splt.bar(ind,data['count'], width)
		splt.set_ylabel('Count')
		splt.set_title('NBS Category Count')
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(data['name'])
		fig.autofmt_xdate(rotation=45)
		return fig


	def getD3(self, xlabel="name", ylabel="count"):
		df = pd.DataFrame({xlabel:[],ylabel:[]})
		p = d3py.PandasFigure(df)
		p += d3py.Bar(x = xlabel, y=ylabel)
		# p += d3py.Line(x = xlabel, y=ylabel)
		p += d3py.xAxis(x = xlabel)
		p += d3py.yAxis(y = ylabel)
		p.update()
		p.js.merge(p.js_geoms)
		d3 = {}
		d3['js'] = p.js
		d3['css'] = "%s\n%s"%(p.css, p.css_geoms)
		return d3

ml = MyLaunch()
ml.launch(port=9090)
# input_params = {'ex_first':0,'max_incl':15}

