from spyre import server

import pickle


class StockExample(server.App):

    title = "Historical Stock Prices"

    inputs = [{
        "input_type": 'dropdown',
        "label": 'Company',
        "options": [
            {"label": "Google", "value": "GOOG"},
            {"label": "Yahoo", "value": "YHOO"},
            {"label": "Apple", "value": "AAPL"}],
        "variable_name": 'ticker',
        "action_id": "plot"
    }]

    outputs = [
        {"output_type": "plot", "output_id": "plot"},
        {"output_type": "table", "output_id": "table"}
    ]

    def getData(self, params):
        dfs = pickle.load((open("stocks.pkl", "rb")))
        ticker = params['ticker']
        return dfs[ticker]

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.set_index('Date').drop(['volume'], axis=1).plot()
        plt_obj.set_ylabel("Price")
        fig = plt_obj.get_figure()
        return fig


if __name__ == '__main__':
    app = StockExample()
    app.launch(port=9093)
