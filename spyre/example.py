from server import Launch
import numpy as np
import pandas as pd
import d3py
import os
import simplejson as json
import matplotlib.pyplot as plt
from ggplot import *

class MyLaunch(Launch):
	templateVars = {"shared_fields" : [
								{"label": 'Exclude First', "value": 0, "variable_name": 'ex_first', "input_type":'text'},
								{"label": 'Max Return', "value": 15, "variable_name": 'max_incl', "input_type":'text'},
						],
					"controls" : [
					{"output_type" : "d3",
						"button_label" : "Make d3 Bar Plot",
						"button_id" : "submit-d3",
						"text_fields" : []
					},
					{"output_type" : "image",
						"button_label" : "Make Matplotlib Graph",
						"button_id" : "submit-plot",
						"text_fields" : []
					},
					{"output_type" : "table",
						"button_label" : "Load Table",
						"button_id" : "load-table",
						"text_fields" : []
					}
					]
				}
	def getData(self, params):
		ex_first = int(params['ex_first'])
		max_incl = int(params['max_incl'])
		x = [{'count': 7834, 'name': 'Record Label'},{'count': 5237, 'name': 'Actor'},{'count': 3278, 'name': 'Public Figure '},{'count': 2533, 'name': 'Comedian'},{'count': 2042, 'name': 'Producer'},{'count': 1266, 'name': 'News/Media'},{'count': 1165, 'name': 'Entertainer'},{'count': 980, 'name': 'Radio Station '},{'count': 962, 'name': 'TV Show'},{'count': 747, 'name': 'Company'},{'count': 712, 'name': 'Local Business'},{'count': 679, 'name': 'Apparel'}]
		return x[ex_first:max_incl]

	# def getPlot(self, params):
	# 	data = self.getData(params)
	# 	fig = plt.figure()
	# 	splt = fig.add_subplot(1,1,1)
	# 	x = pd.DataFrame(data)['name'].tolist()
	# 	y = pd.DataFrame(data)['count'].tolist()
	# 	ind = np.arange(len(x))
	# 	width = 0.85  
	# 	splt.bar(ind,y, width)
	# 	splt.set_ylabel('Count')
	# 	splt.set_title('NBS Category Count')
	# 	xTickMarks = ['Group'+str(i) for i in range(1,6)]
	# 	splt.set_xticks(ind+width/2)
	# 	splt.set_xticklabels(x)
	# 	fig.autofmt_xdate(rotation=45)
	# 	return fig

	def getPlot(self, params):
		data = pd.DataFrame(self.getData(params))
		fig = ggplot(data, aes(x='name')) + geom_bar(aes(weight='count')) + theme(axis_text_x=element_text(angle=30,hjust=1))
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
ml.launch()
# params = {'ex_first':0,'max_incl':15}