from spyre import server

import yfinance as yf

from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh import plotting

server.include_df_index = True


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
        df = yf.download(ticker, period="3mo", interval="1d", auto_adjust=True)
        return df

    def getPlot(self, params):
        ticker = params['ticker']
        if ticker == 'empty':
            ticker = params['custom_ticker'].upper()
        df = self.getData(params)
        plt_obj = df.drop(columns=['Volume']).plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title(ticker)
        return plt_obj.get_figure()

    def getHTML(self, params):
        ticker = params['ticker']
        if ticker == 'empty':
            ticker = params['custom_ticker'].upper()
        df = self.getData(params)
        bokeh_plot = plotting.figure(x_axis_type='datetime', title=ticker)
        bokeh_plot.line(df.index, df['Close'], color='#1c2980', legend_label="Close")
        bokeh_plot.line(df.index, df['High'], color='#80641c', legend_label="High")
        bokeh_plot.line(df.index, df['Low'], color='#80321c', legend_label="Low")
        script, div = components(bokeh_plot, CDN)
        return "%s\n%s" % (script, div)

    def getCustomJS(self):
        return INLINE.js_raw[0]

    def getCustomCSS(self):
        return INLINE.css_raw[0] if INLINE.css_raw else ""


if __name__ == '__main__':
    ml = StocksWithBokeh()
    ml.launch(port=9097)
