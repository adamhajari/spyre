# tested with python2.7
from spyre import server

import pandas as pd
from googlefinance.client import get_price_data

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
            {"label": "Amazon", "value": "AMZN"},
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
            ticker = params['custom_ticker'].upper()

        xchng = "NASD"

        param = {
            'q': ticker,  # Stock symbol (ex: "AAPL")
            'i': "86400",  # Interval size in seconds ("86400" = 1 day intervals)
            'x': xchng,  # Stock exchange symbol on which stock is traded (ex: "NASD")
            'p': "3M"  # Period (Ex: "1Y" = 1 year)
        }
        # get price data (return pandas dataframe)
        df = get_price_data(param)

        df['Date'] = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%s')
        return df

    def getPlot(self, params):
        ticker = params['ticker']
        if ticker == 'empty':
            ticker = params['custom_ticker'].upper()
        df = self.getData(params)
        plt_obj = df.set_index('Date').drop(['Volume'], axis=1).plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title(ticker)
        fig = plt_obj.get_figure()
        return fig

    def getHTML(self, params):
        ticker = params['ticker']
        if ticker == 'empty':
            ticker = params['custom_ticker'].upper()
        df = self.getData(params)  # get data
        try:
            bokeh_plot = plotting.line(
                df['Date'], df['Close'], color='#1c2980',
                legend="Close", x_axis_type="datetime", title=ticker
            )
        except AttributeError:
            bokeh_plot = plotting.figure(x_axis_type='datetime', title=ticker)
            bokeh_plot.line(df['Date'], df['Close'], color='#1c2980', legend="Close")
        bokeh_plot.line(df['Date'], df['High'], color='#80641c', legend="High")
        bokeh_plot.line(df['Date'], df['Low'], color='#80321c', legend="Low")

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
