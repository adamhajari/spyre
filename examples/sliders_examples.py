# tested with python2.7 and 3.4
from spyre import server

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
import sys


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
        fig = plt.figure()

        # sine wave
        splt1 = fig.add_subplot(3, 1, 1)
        y1 = np.sin(f * x / (2 * pi))
        splt1.plot(x, y1)
        splt1.axes.get_xaxis().set_visible(False)

        # exponential decay
        splt2 = fig.add_subplot(3, 1, 2)
        y2 = np.exp(-x * d)
        splt2.plot(x, y2)
        splt2.axes.get_xaxis().set_visible(False)

        # sine wave decay
        splt3 = fig.add_subplot(3, 1, 3)
        y3 = np.sin(f * x / (2 * pi)) * np.exp(-x * d)
        splt3.plot(x, y3)
        return fig


if __name__ == "__main__":
    app = SlidersApp()
    args = sys.argv[1:]
    if len(args) == 1:
        app.launch(host=args[0])
    elif len(args) == 2:
        app.launch(host=args[0], port=int(args[1]))
    else:
        app.launch()
