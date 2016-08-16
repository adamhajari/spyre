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
import requests
import json

from bokeh.resources import INLINE

class TestApp1(server.App):
	colors = [	{"label":"Green", "value":'g'},
			    {"label": "Red", "value":'r', "checked":True}, 
			    {"label": "Blue", "value":'b'}, 
			    {"label": "Yellow", "value":'y'}]

	states = {	"Alabama":"AL", 
				"Arkansas":"AR",
				"Alaska":"AK",
				"Nevada":"NV",
				"New York":"NY",
				"New Jersey":"NJ",}

	title = "Test App 1"
	inputs = [{	"type":'text',
				"label": 'Title', 
				"value" : 'Simple Sine Wave',
				"key": 'title', 
				"action_id" : "refresh",
			},
			{	"type":'searchbox',
				"label": 'Frontend Search', 
				"options" : states.keys(),
				"key": 'state', 
				"action_id" : "refresh",
			},
			{	"type":'searchbox',
				"label": 'Backend Search', 
				"value": 'Foo Fighters',
				"output_id" : "backend_search",
				"key": 'results', 
				"action_id" : "refresh",
			},
			{	"type":'radiobuttons',
				"label": 'Function', 
				"options" : [
					{"label": "Sine", "value":"sin", "checked":True}, 
					{"label":"Cosine", "value":"cos"}
				],
				"key": 'func_type', 
				"action_id" : "refresh",
			},
			{	"type":'checkboxgroup',
				"label": 'Axis Labels', 
				"options" : [
					{"label": "x-axis", "value":"x", "checked":True}, 
					{"label":"y-axis", "value":"y"}
				],
				"key": 'axis_label', 
				"action_id" : "refresh",
			},
			{	"type":'dropdown',
				"label": 'Line Color', 
				"options" : colors,
				"key": 'color', 
				"action_id" : "refresh",
				"linked_key": 'title', 
				"linked_type": 'text', 
				"linked_value":"hey"
			},
			{	"type":'slider',
				"label": 'frequency', 
				"key": 'freq', 
				"value" : 2,
				"min" : 1, 
				"max" : 30,
				"action_id" : "refresh",
				"linked_key": 'title', 
				"linked_type": 'text', 
			}]
	tabs = ["Tab1", "Tab2"]
	controls = [{	"type" : "upload",
					"id" : "button3",
					"label" : "upload"
				},
				{	"type" : "button",
					"id" : "refresh",
					"label" : "refresh",
				},
				{	"type" : "button",
					"id" : "button2",
					"label" : "download",
				},
				]
	outputs = [{	"type" : "html",
					"id" : "html1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"type" : "plot",
					"id" : "plot1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"type" : "table",
					"id" : "table1",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"type" : "plot",
					"id" : "plot2",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"type" : "download",
					"id" : "download_id",
					"control_id" : "button2",
					"on_page_load" : False,
				},
				{	"type" : "html",
					"id" : "html_out",
					"control_id" : "refresh",
					"tab" : "Tab1"
				},
				{	"type" : "plot",
					"id" : "plot3",
					"control_id" : "refresh",
					"tab" : "Tab2"
				},
				{	"type" : "table",
					"id" : "table2",
					"control_id" : "refresh",
					"sortable" : True,
					"tab" : "Tab2"
				},
				{	"type" : "json",
					"id" : "backend_search",
					"control_id" : "refresh",
				}]
	def __init__(self):
		self.upload_data = None

	def html1(self,params):
		text = ""
		if self.upload_data is not None:
			text += self.upload_data
		return text

	def backend_search(self,params):
		# the searchbox input will automatically add the query to 'params' as q
		q = params.get('q', params['results'])

		url="https://api.nextbigsound.com/search/v1/artists/?fields=id,name,category&limit=15&query=%s" % q
		resp = requests.get(url)
		data = json.loads(resp.text)
		artists = []
		for artist in data['artists']:
			artists.append({'label':artist['name'], 'value':artist['id']})
		return artists
		


	def storeUpload(self,file):
		self.upload_file = file
		self.upload_data = file.read()
		file.close()

	def getTable1Data(self,params):
		count = [1,4,3]
		name = ['<a href="http://adamhajari.com">A</a>','B','C']
		return {'name':name, 'count':count}

	def table1(self,params):
		data = self.getTable1Data(params)
		df = pd.DataFrame(data)
		return df

	def table2(self,params):
		f = float(params['freq'])
		func_type = params['func_type']
		x = np.arange(0,6*pi,pi/50)
		y1 = np.cos(f*x)
		y2 = np.sin(f*x)
		df = pd.DataFrame({"cos":y1,"sin":y2},index=x)
		df.index.name = "t"
		return df

	
	def plot3(self,params):
		axis_label = params['axis_label']
		color = params['color']
		df = self.table2(params)
		ax = df.plot(title=params['title'])
		ax.set_ylabel('y axis')
		ax.set_xlabel('x axis')
		return ax
	
	def plot1(self,params):
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)

		f = float(params['freq'])
		title = "%s: %s" % (params['title'],params['state'])
		axis_label = params['axis_label']
		color = params['color']
		func_type = params['func_type']

		x = np.arange(0,6*pi,pi/50)
		splt.set_title(title)
		for axis in axis_label:
			if axis=="x":
				splt.set_xlabel('x axis')
			if axis=="y":
				splt.set_ylabel('y axis')
		if func_type=='cos':
			y = np.cos(f*x)
		else:
			y = np.sin(f*x)
		splt.plot(x,y,color=color)  # sine wave
		return fig

	def plot2(self,params):
		title = params['results']
		data = self.table1(params)
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		splt.set_title(title)
		ind = np.arange(len(data['name']))
		width = 0.85  
		splt.bar(ind,data['count'], width)
		xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(["A","B","C"])
		return fig

	def html_out(self,params):
		func_type = params['func_type']
		axis_label = params['axis_label']
		color = params['color']
		freq = params['freq']
		html = "function type: {} <br>axis label: {}<br>color: {}<br>frequency: {}".format(func_type, axis_label, color, freq)
		return html

	def download_id(self,params):
		return self.table2(params)

	def noOutput(self, input_params):
		return 0

	def getCustomCSS(self):
		return INLINE.css_raw[0]

if __name__ == '__main__':
	app = TestApp1()
	app.launch(port=9096)
