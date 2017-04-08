# from spyre import server
from spyre import server

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import pi


class TestApp(server.App):
    colors = [
        {"label": "Green", "value": 'g'},
        {"label": "Red", "value": 'r'},
        {"label": "Blue", "value": 'b'},
        {"label": "Yellow", "value": 'y'},
    ]

    on_demand_streaming_services = [
        {"label": "Spotify", "value": 's'},
        {"label": "Apple Music", "value": 'a'},
    ]

    title = "Simple Sine Wave"
    inputs = [
        {
            "input_type": 'text',
            "label": 'Title',
            "value": 'Simple Sine Wave',
            "variable_name": 'title',
            "action_id": "plot",
        }, {
            "input_type": 'radiobuttons',
            "label": 'Function',
            "options": [
                {"label": "Sine", "value": "sin", "checked": True},
                {"label": "Cosine", "value": "cos"}
            ],
            "variable_name": 'func_type',
            "action_id": "plot",
        }, {
            "input_type": 'checkboxgroup',
            "label": 'Axis Labels',
            "options": [
                {"label": "x-axis", "value": 1, "checked": True},
                {"label": "y-axis", "value": 2}
            ],
            "variable_name": 'axis_label',
            "action_id": "plot",
        }, {
            "input_type": 'dropdown',
            "label": 'Line Color',
            "options": colors,
            "variable_name": 'color',
            "value": "b",
            "action_id": "plot",
        }, {
            "input_type": 'dropdown',
            "label": 'On-Demand Streaming Service',
            "options": on_demand_streaming_services,
            "variable_name": 'on_demand_streaming_service',
            "action_id": "plot",
        }, {
            "input_type": 'slider',
            "label": 'frequency',
            "variable_name": 'freq',
            "value": 2,
            "min": 1,
            "max": 30,
            "action_id": "plot",
        }
    ]
    controls = [
        {
            "control_type": "button",
            "control_id": "button1",
            "label": "plot",
        }, {
            "control_type": "button",
            "control_id": "button2",
            "label": "download",
        }
    ]
    outputs = [
        {
            "output_type": "html",
            "output_id": "html_id",
            "control_id": "button1",
            "on_page_load": True,
        }, {
            "output_type": "plot",
            "output_id": "plot",
            "control_id": "button1",
            "on_page_load": True,
        }, {
            "output_type": "plot",
            "output_id": "plot2",
            "control_id": "button1",
            "on_page_load": True,
        }, {
            "output_type": "table",
            "output_id": "table_id",
            "control_id": "button1",
            "sortable": True,
            "on_page_load": True,
        }, {
            "output_type": "download",
            "output_id": "download_id",
            "control_id": "button2",
        }
    ]

    def plot1(self, params):
        fig = plt.figure()  # make figure object
        splt = fig.add_subplot(1, 1, 1)

        f = float(params['freq'])
        title = params['title']
        axis_label = map(int, params['axis_label'])
        color = params['color']
        func_type = params['func_type']

        x = np.arange(0, 6 * pi, pi / 50)
        splt.set_title(title)
        for axis in axis_label:
            if axis == 1:
                splt.set_xlabel('x axis')
            if axis == 2:
                splt.set_ylabel('y axis')
        if func_type == 'cos':
            y = np.cos(f * x)
        else:
            y = np.sin(f * x)
        splt.plot(x, y, color=color)  # sine wave
        return fig

    def plot2(self, params):
        data = self.getData(params)
        fig = plt.figure()  # make figure object
        splt = fig.add_subplot(1, 1, 1)
        ind = np.arange(len(data['name']))
        width = 0.85
        splt.bar(ind, data['count'], width)
        splt.set_xticks(ind + width / 2)
        splt.set_xticklabels(["A", "B", "C"])
        return fig

    def html1(self, params):
        return "hello world"

    def html2(self, params):
        func_type = params['func_type']
        axis_label = params['axis_label']
        color = params['color']
        freq = params['freq']
        html = (
            "function type: {} <br>axis label: {}<br>color: {}<br>frequency: {}"
            .format(func_type, axis_label, color, freq)
        )
        return html

    def getJsonData(self, params):
        count = [1, 4, 3]
        name = ['<a href="http://adamhajari.com">A</a>', 'B', 'C']
        return {'name': name, 'count': count}

    def getData(self, params):
        data = self.getJsonData(params)
        df = pd.DataFrame(data)
        return df

    def noOutput(self, input_params):
        return 0
