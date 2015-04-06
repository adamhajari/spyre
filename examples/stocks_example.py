# tested with python2.7 and 3.4
from spyre import server

import pandas as pd
import json

try:
	import urllib2
except ImportError:
	import urllib.request as urllib2

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

	def getData(self, params):
		ticker = params['ticker']
		# make call to yahoo finance api to get historical stock data
		api_url = 'https://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=3m/json'.format(ticker)
		result = urllib2.urlopen(api_url).read()
		data = json.loads(result.decode('utf-8').replace('finance_charts_json_callback( ','')[:-1])  # strip away the javascript and load json
		self.company_name = data['meta']['Company-Name']
		df = pd.DataFrame.from_records(data['series'])
		df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
		return df

	def getPlot(self, params):
		df = self.getData(params)
		plt_obj = df.set_index('Date').drop(['volume'],axis=1).plot()
		plt_obj.set_ylabel("Price")
		plt_obj.set_title(self.company_name)
		fig = plt_obj.get_figure()
		return fig
if __name__ == '__main__':
	app = StockExample()
	app.launch(port=9093)
