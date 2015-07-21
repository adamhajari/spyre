# tested with python2.7 and 3.4
from spyre import server

import pickle
import pandas as pd
import json

try:
	import urllib2
except ImportError:
	import urllib.request as urllib2

class StockExample(server.App):

	title = "Historical Stock Prices"

	inputs = [{		"input_type":'text',
					"label": 'Company',
					"value": 'GOOG',
					"variable_name": 'ticker', 
					"action_id": "update_data" }]

	controls = [{	"control_type" : "hidden",
					"control_id" : "update_data"}]

	tabs = ["Plot", "Table"]

	outputs = [{	"output_type" : "plot",
					"output_id" : "plot",
					"control_id" : "update_data",
					"tab" : "Plot"},
				{	"output_type" : "table",
					"output_id" : "table_id",
					"control_id" : "update_data",
					"tab" : "Table"}]

	def getData(self, params):
		dfs = pickle.load((open( "stocks.pkl", "rb" )))
		ticker = params['ticker']
		return dfs[ticker]

	def getPlot(self, params):
		df = self.getData(params)
		plt_obj = df.set_index('Date').drop(['volume'],axis=1).plot()
		plt_obj.set_ylabel("Price")
		fig = plt_obj.get_figure()
		return fig

if __name__ == '__main__':
	app = StockExample()
	app.launch(port=9093)
