# tested with python2.7 and 3.4
from spyre import server

import pandas as pd
import json
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh import plotting


class StocksWithBokeh(server.App):
    title = "Historical Stock Prices"

    inputs = [{
        "type": 'dropdown',
        "label": 'Company',
        "options": [
            {"label": "Choose A Company", "value": "empty"},
            {"label": "Google", "value": "GOOG", "checked": True},
            {"label": "Yahoo", "value": "YHOO"},
            {"label": "Apple", "value": "AAPL"}],
        "key": 'ticker',
        "action_id": "update_data",
        "linked_key": 'custom_ticker',
        "linked_type": 'text',
    }, {
        "type": 'text',
        "label": 'or enter a ticker symbol',
        "key": 'custom_ticker',
        "action_id": "update_data",
        "linked_key": 'ticker',
        "linked_type": 'dropdown',
        "linked_value": 'empty'
    }]

    controls = [{
        "type": "hidden",
        "label": "get historical stock prices",
        "id": "update_data"
    }]

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
        "sortable": True
    }, {
        "type": "html",
        "id": "html_id",
        "control_id": "update_data",
        "tab": "Bokeh"
    }]

    tabs = ["Plot", "Table", "Bokeh"]

    def getData(self, params):
        ticker = params['ticker']
        if ticker == 'empty':
            ticker = params['custom_ticker']
        # make call to yahoo finance api to get historical stock data
        api_url = (
            'https://chartapi.finance.yahoo.com/instrument/1.0/{}/'
            'chartdata;type=quote;range=3m/json'.format(ticker)
        )
        result = urllib2.urlopen(api_url).read()
        # strip away the javascript and load json
        data = json.loads(result.decode('utf-8').replace('finance_charts_json_callback( ', '')[:-1])
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

    def getHTML(self, params):
        df = self.getData(params)  # get data
        try:
            bokeh_plot = plotting.line(
                df['Date'], df['close'],
                color='#1c2980', legend="close",
                x_axis_type="datetime", title=self.company_name
            )
        except AttributeError:
            bokeh_plot = plotting.figure(x_axis_type='datetime', title=self.company_name)
            bokeh_plot.line(df['Date'], df['close'], color='#1c2980', legend="close")
        bokeh_plot.line(df['Date'], df['high'], color='#80641c', legend="high")
        bokeh_plot.line(df['Date'], df['low'], color='#80321c', legend="low")

        script, div = components(bokeh_plot, CDN)
        html = "%s\n%s" % (script, div)
        return html

    def getCustomJS(self):
        return INLINE.js_raw[0]

    def getCustomCSS(self):
        return INLINE.css_raw[0]


if __name__ == '__main__':
    ml = StocksWithBokeh()
    ml.launch(port=9097)
