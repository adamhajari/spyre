from spyre import server

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import urllib2
import json
from datetime import datetime

class StockExample(server.App):
	title = "Historical Stock Prices"

	inputs = [{		"input_type":'dropdown',
					"label": 'Company', 
					"options" : [ {"label": "Google", "value":"GOOG"},
								  {"label": "Yahoo", "value":"YHOO"},
								  {"label": "Apple", "value":"AAPL"}],
					"variable_name": 'ticker', 
					"action_id": "update_data" }]

	controls = [{	"control_type" : "hidden",
					"label" : "get historical stock prices",
					"control_id" : "update_data"}]

	tabs = ["Plot", "Table"]

	outputs = [{	"output_type" : "plot",
					"output_id" : "plot",
					"control_id" : "update_data",
					"tab" : "Plot",
					"on_page_load" : True },
				{	"output_type" : "table",
					"output_id" : "table_id",
					"control_id" : "update_data",
					"tab" : "Table",
					"on_page_load" : True }]

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
		fig = df.set_index('Date').drop(['volume'],axis=1).plot().get_figure()
		return fig

app = StockExample()
app.launch(port=9093)
