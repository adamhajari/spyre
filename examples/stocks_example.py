# tested with python2.7
from spyre import server
from googlefinance.client import get_price_data

server.include_df_index = True


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
            {"label": "Amazon", "value": "AMZN"},
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
            df = df.drop(['Volume'], axis=1)

            self.data_cache = df        # caching layer
            self.params_cache = params  # caching layer
        return self.data_cache


if __name__ == '__main__':
    app = StockExample()
    app.launch(port=9093)
