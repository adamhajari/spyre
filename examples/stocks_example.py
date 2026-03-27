from spyre import server
import yfinance as yf

server.include_df_index = True


class StockExample(server.App):

    def __init__(self):
        # simple caching to avoid redundant API calls
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
        params.pop("output_id", None)
        if self.params_cache != params:
            ticker = params['ticker']
            df = yf.download(ticker, period="3mo", interval="1d", auto_adjust=True)
            df = df.drop(columns=['Volume'])
            self.data_cache = df
            self.params_cache = params
        return self.data_cache


if __name__ == '__main__':
    app = StockExample()
    app.launch(port=9093)
