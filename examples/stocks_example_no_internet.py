# tested with python2.7 and 3.4
# must be run from same directory as stock_data.json (in spyre examples directory)
from spyre import server

import pandas as pd
import json


class StockExample(server.App):
    title = "Historical Stock Prices"

    inputs = [{
        "type": 'dropdown',
        "label": 'Company',
        "options": [
            {"label": "Google", "value": "GOOG"},
            {"label": "Yahoo", "value": "YHOO"},
            {"label": "Apple", "value": "AAPL"}
        ],
        "value": 'GOOG',
        "key": 'ticker',
        "action_id": "update_data"
    }]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Plot", "Table"]

    outputs = [{
        "type": "plot",
        "id": "plot",
        "control_id": "update_data",
        "tab": "Plot"
    }, {
        "type": "table",
        "id": "table_id",
        "control_id": "update_data",
        "tab": "Table",
        "on_page_load": True
    }]

    def getData(self, params):
        ticker = params['ticker']
        with open('stock_data.json', 'r') as f:
            data = json.loads(f.read())[ticker]
        self.company_name = data['meta']['Company-Name']
        df = pd.DataFrame.from_records(data['series'])
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.set_index('Date').drop(['volume'], axis=1).plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title(self.company_name)
        fig = plt_obj.get_figure()
        return fig


if __name__ == '__main__':
    app = StockExample()
    app.launch(port=9093)
