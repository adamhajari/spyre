# tested with python2.7 and 3.4
from spyre import server

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi


class SlidersApp(server.App):
    title = "Decaying Sine Wave"

    inputs = [
        {
            "type": 'slider',
            "label": 'Frequency',
            "min": 1, "max": 100, "value": 50,
            "key": 'freq',
            "action_id": 'plot'
        }, {
            "type": 'slider',
            "label": 'Decay Rate',
            "min": 0, "max": 2, "step": 0.01, "value": 0.5,
            "key": 'decay',
            "action_id": 'plot'
        }
    ]

    outputs = [{
        "type": "plot",
        "id": "plot"
    }]

    def getPlot(self, params):
        f = float(params['freq'])
        d = float(params['decay'])
        x = np.arange(0, 6 * pi, pi / 50)
        y1 = np.sin(f * x / (2 * pi))
        y2 = np.exp(-x * d)
        y3 = np.sin(f * x / (2 * pi)) * np.exp(-x * d)
        fig = plt.figure()
        splt1 = fig.add_subplot(3, 1, 1)
        splt1.plot(x, y1)  # sine wave
        splt1.axes.get_xaxis().set_visible(False)
        splt2 = fig.add_subplot(3, 1, 2)
        splt2.plot(x, y2)  # exponential decay
        splt2.axes.get_xaxis().set_visible(False)
        splt3 = fig.add_subplot(3, 1, 3)
        splt3.plot(x, y3)  # sine wave decay
        return fig


if __name__ == '__main__':
    app = SlidersApp()
    app.launch(port=9094)
