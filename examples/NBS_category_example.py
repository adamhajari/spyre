from spyre import server

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NBSCategoriesApp(server.App):
    title = "Spyre Example"

    inputs = [{    'input_type' : 'slider',
                "label": 'Exclude First', 
                "min" : 0,
                "max" : 14,
                "value": 0, 
                "variable_name": 'ex_first' }]

    controls = [{"control_type" : "button",
                    "label" : "Make Matplotlib Graph",
                    "control_id" : "submit_plot"},
                {"control_type" : "button",
                    "label" : "Make Matplotlib Graph 2",
                    "control_id" : "submit_plot2"},
                {"control_type" : "button",
                    "label" : "Load Table",
                    "control_id" : "load_table"}]

    outputs = [{"output_type" : "plot",
                    "output_id" : "plot1",
                    "control_id" : "submit_plot",
                    "tab" : "Plot1",
                    "on_page_load" : True},
                {"output_type" : "plot",
                    "output_id" : "plot2",
                    "control_id" : "submit_plot2",
                    "tab" : "Plot2"},
                {"output_type" : "table",
                    "output_id" : "table_id",
                    "control_id" : "load_table",
                    "tab" : "Table"},
                {"output_type" : "html",
                    "output_id" : "custom_html",
                    "tab" : "text",
                    "on_page_load" : True}]

    tabs = ["Plot1", "Plot2", "Table", "text"]

    def getData(self, params):
        # cache values within the Launch object to avoid reloading the data each time
        ex_first = int(params['ex_first'])
        count = [620716,71294,50807,7834,5237,3278,2533,2042,1266,1165,980,962,747,712,679]
        name = ['Musician','Author','Book','Record Label','Actor','Public Figure ','Comedian','Producer','News/Media','Entertainer','Radio Station ','TV Show','Company','Local Business','Apparel']
        df = pd.DataFrame({'name':name, 'count':count})
        df = df[['name','count']]
        return df[ex_first:]

    def getPlot(self, params):
        output_id = params['output_id']
        data = self.getData(params)  # get data
        if output_id=="plot1":
            return self.getPlot1(data)
        else:
            return self.getPlot2(data)

    def getPlot1(self, data):
        fig = plt.figure()  # make figure object
        splt = fig.add_subplot(1,1,1)
        ind = np.arange(len(data['name']))
        width = 0.85  
        splt.bar(ind,data['count'], width)
        splt.set_ylabel('Count')
        splt.set_title('NBS Category Count Plot 1')
        xTickMarks = ['Group'+str(i) for i in range(1,6)]
        splt.set_xticks(ind+width/2)
        splt.set_xticklabels(data['name'].tolist())
        fig.autofmt_xdate(rotation=45)
        return fig

    def getPlot2(self, data):
        fig = plt.figure()  # make figure object
        splt = fig.add_subplot(1,1,1)
        ind = np.arange(len(data['name']))
        width = 0.85  
        splt.bar(ind,data['count'], width, color='orange')
        splt.set_ylabel('Count')
        splt.set_title('NBS Category Count Plot 2')
        xTickMarks = ['Group'+str(i) for i in range(1,6)]
        splt.set_xticks(ind+width/2)
        splt.set_xticklabels(data['name'].tolist())
        fig.autofmt_xdate(rotation=45)
        return fig

    def getHTML(self, params):
        return "<b>App Description: </b> <i>This</i> is where you could describe your app."

if __name__ == '__main__':
    app = NBSCategoriesApp()
    app.launch(port=9091)

