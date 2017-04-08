# tested with python2.7 and 3.4
from spyre import server

import pandas as pd
import numpy as np

from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.sampledata import us_counties, unemployment
from bokeh import plotting
from collections import OrderedDict
try:
    from bokeh.objects import HoverTool
except ImportError:
    from bokeh.models import HoverTool


class UnemploymentApp(server.App):
    def __init__(self):
        colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
        stuff = []
        for key in us_counties.data:
            stuff.append(us_counties.data[key])
        shapes = pd.DataFrame(stuff, index=us_counties.data.keys())
        unemp = pd.DataFrame(
            list(unemployment.data.values()),
            index=list(unemployment.data.keys()),
            columns=['rate']
        )
        unemp['idx'] = (unemp['rate'] // 2).astype('i8')
        unemp[unemp['idx'] > 5] = 5
        unemp['color'] = [colors[idx] for idx in unemp['idx'].tolist()]
        data = unemp.join(shapes)
        data['mlong'] = list(map(np.mean, data['lons']))
        data['mlats'] = list(map(np.mean, data['lats']))
        data = data[(data['mlong'] > -130) & (data['mlong'] < -65)]
        data = data[(data['mlats'] > 25) & (data['mlats'] < 50)]
        self.data = data

    title = "US Unemployment"

    controls = [{
        "control_type": "hidden",
        "label": "get historical stock prices",
        "control_id": "update_data"
    }]

    outputs = [{
        "output_type": "html",
        "output_id": "html_id",
        "control_id": "update_data",
        "on_page_load": True
    }]

    def getHTML(self, params):
        state = params['state']
        if state == 'all':
            data = self.data
        else:
            data = self.data[self.data['state'] == state]

        TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,previewsave"

        try:
            fig = plotting.patches(
                data['lons'], data['lats'], fill_color=data['color'], fill_alpha=0.7, tools=TOOLS,
                line_color="white", line_width=0.5, title=state.upper() + " Unemployment 2009"
            )
        except Exception:
            fig = plotting.figure(title=state.upper() + " Unemployment 2009", tools=TOOLS)
            fig.patches(
                data['lons'], data['lats'], fill_color=data['color'],
                fill_alpha=0.7, line_color="white", line_width=0.5
            )

        hover = fig.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("index", "$index")
        ])

        script, div = components(fig, CDN)
        html = "%s\n%s" % (script, div)
        return html

    def getCustomJS(self):
        return INLINE.js_raw[0]

    def getCustomCSS(self):
        return INLINE.css_raw[0]


if __name__ == '__main__':
    app = UnemploymentApp()

    states = pd.unique(app.data['state'].dropna())
    states.sort()
    options = [{"label": "all", "value": "all"}]
    states_opts = [{"label": x.upper(), "value": x} for x in states.tolist()]
    options.extend(states_opts)
    app.inputs = [{
        "input_type": 'dropdown',
        "label": 'State',
        "options": options,
        "variable_name": 'state',
        "action_id": "update_data"
    }]
    app.launch(port=9097)
