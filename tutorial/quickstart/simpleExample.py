from spyre import server
import matplotlib.pyplot as plt
import numpy as np


class SimpleExample(server.Launch):

    title = "Simple Example"
    inputs = [{
        "input_type": 'checkboxgroup',
        "label": 'features',
        "options": [
            {"label": "slope", "value": "slope", "checked": True},
            {"label": "intercept", "value": "intercept"},
            {"label": "noise", "value": "noise"}
        ],
        "variable_name": 'features',
        "action_id": "make_plot"
    }]
    outputs = [{
        "output_type": "plot",
        "output_id": "make_plot",
    }]

    def getPlot(self, params):
        features = params['features']
        y = np.repeat(0.0, 100.0)
        if 'slope' in features:
            y = np.arange(100.0)
        if 'intercept' in features:
            y += 10.0
        if 'noise' in features:
            y += np.random.normal(0, 10, 100)
        fig = plt.figure()  # make figure object
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(y)
        return fig


app = SimpleExample()
app.launch(host='local', port=8080)
