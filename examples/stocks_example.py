# tested with python2.7 and 3.4
from spyre import server

import pandas as pd
import json

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2


class StockExample(server.App):

    def __init__(self):
        # implements a simple caching mechanism to avoid multiple calls to the yahoo finance api
        self.data_cache = None
        self.params_cache = None

    title = "Historical Stock Prices"

    inputs = [{
        "type": 'dropdown',
        "label": 'Company',
        "options": [
            {"label": "Google", "value": "GOOG"},
            {"label": "Yahoo", "value": "YHOO"},
            {"label": "Apple", "value": "AAPL"}],
        "value": 'GOOG',
        "key": 'ticker',
        "action_id": "update_data"
    }]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        params.pop("output_id", None)    # caching layer
        if self.params_cache != params:   # caching layer
            ticker = params['ticker']
            # make call to yahoo finance api to get historical stock data
            api_url = (
                'https://chartapi.finance.yahoo.com/instrument'
                '/1.0/{}/chartdata;type=quote;range=3m/json'
                .format(ticker)
            )
            result = urllib2.urlopen(api_url).read()
            # strip away the javascript and load json
            data = json.loads(
                result.decode('utf-8').replace('finance_charts_json_callback( ', '')[:-1]
            )
            self.company_name = data['meta']['Company-Name']
            df = pd.DataFrame.from_records(data['series']).drop(['volume'], axis=1)
            df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
            self.data_cache = df        # caching layer
            self.params_cache = params  # caching layer
        return self.data_cache


if __name__ == '__main__':
    app = StockExample()
    app.launch(port=9093)
