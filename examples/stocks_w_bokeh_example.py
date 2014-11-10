from spyre import server

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import urllib2
import json
from datetime import datetime

from bokeh import resources as r
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.plotting import line

class MyLaunch(server.Launch):
	templateVars = {"title" : "Historical Stock Prices",
					"inputs" : [
						{	"input_type":'dropdown',
							"label": 'Company', 
							"options" : [
								{"label": "Google", "value":"GOOG"},
								{"label": "Yahoo", "value":"YHOO"},
								{"label": "Apple", "value":"AAPL"}
							],
							"variable_name": 'ticker', 
							"action_id": "update_data"
						}
						],
					"controls" : [
						{	"control_type" : "hidden",
							"label" : "get historical stock prices",
							"control_id" : "update_data",
						}
					],
					"tabs" : ["Plot", "Table", "Bokeh"],
					"outputs" : [
						{	"output_type" : "plot",
							"output_id" : "plot",
							"control_id" : "update_data",
							"tab" : "Plot",
							"on_page_load" : True,
						},
						{	"output_type" : "table",
							"output_id" : "table_id",
							"control_id" : "update_data",
							"tab" : "Table",
							"on_page_load" : True,
						},
						{	"output_type" : "html",
							"output_id" : "html_id",
							"control_id" : "update_data",
							"tab" : "Bokeh",
							"on_page_load" : True,
						}
					]
				}

	# cache values within the Launch object to avoid reloading the data each time
	data_params = None
	data = pd.DataFrame()

	def getData(self, params):
		if params != self.data_params:
			ticker = params['ticker']
			# make call to yahoo finance api to get historical stock data
			api_url = 'https://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=3m/json'.format(ticker)
			result = urllib2.urlopen(api_url)
			r = result.read()
			data = json.loads(r.replace('finance_charts_json_callback( ','')[:-1])  # strip away the javascript and load json
			# make call to yahoo finance api to get historical stock data
			self.company_name = data['meta']['Company-Name']
			df = pd.DataFrame.from_records(data['series'])
			df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
			self.data = df
			self.data_params = ticker
		return self.data

	def getPlot(self, params):
		df = self.getData(params)  # get data
		dates = pd.DatetimeIndex(df['Date'])
		fig = plt.figure()
		splt = fig.add_subplot(1,1,1)
		splt.plot_date(dates, df['close'], fmt='-', label="close")
		splt.plot_date(dates, df['high'], fmt='-', label="high")
		splt.plot_date(dates, df['low'], fmt='-', label="low")
		splt.set_ylabel('Price')
		splt.set_xlabel('Date')
		splt.set_title(self.company_name)
		splt.legend(loc=2)
		splt.xaxis.set_major_formatter( DateFormatter('%m-%d-%Y') )
		fig.autofmt_xdate()
		return fig

	def getHTML(self,params):
		df = self.getData(params)  # get data
		bokeh_plot = line(df['Date'],df['close'], color='#1c2980', legend="close", x_axis_type = "datetime", title=self.company_name)
		bokeh_plot.line(df['Date'],df['high'], color='#80641c', legend="high")
		bokeh_plot.line(df['Date'],df['low'], color='#80321c', legend="low")

		script, div = components(bokeh_plot, CDN)
		html = "%s\n%s"%(script, div)
		return html

	def getCustomJS(self):
		return r.INLINE.js_raw[0]

	def getCustomCSS(self):
		return r.INLINE.css_raw[0]

ml = MyLaunch()
ml.launch(port=9093)