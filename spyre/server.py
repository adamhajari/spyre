import os, os.path
import json
import jinja2
import StringIO
import matplotlib.pyplot as plt
import pandas as pd

import model
import View

import cherrypy

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )
templateEnv = jinja2.Environment( loader=templateLoader )



class Root(object):
	def __init__(self,templateVars=None, getJsonDataFunction=None, getDataFunction=None, getPlotFunction=None, getD3Function=None, getHTMLFunction=None):
		self.templateVars = templateVars
		self.getJsonData = getJsonDataFunction
		self.getData = getDataFunction
		self.getPlot = getPlotFunction
		self.getD3 = getD3Function
		self.getHTML = getHTMLFunction
		d3 = self.getD3()
		self.templateVars['d3js'] = d3['js']
		self.templateVars['d3css'] = d3['css']

		v = View.View()
		self.templateVars['js'] = v.getJS()
		self.templateVars['css'] = v.getCSS()
		print self.templateVars['d3css']

	@cherrypy.expose
	def index(self):
		v = View.View()
		template = jinja2.Template(v.getHTML())
		return template.render( self.templateVars )

	@cherrypy.expose
	def plot(self, **args):
		p = self.getPlot(args)
		d = model.Plot()
		buffer = d.getPlotPath(p)
		cherrypy.response.headers['Content-Type'] = 'image/png'
		return buffer.getvalue()

	@cherrypy.expose
	def data(self, **args):
		data = self.getJsonData(args)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({'data':data,'args':args})

	@cherrypy.expose
	def table(self, **args):
		df = self.getData(args)
		cherrypy.response.headers['Content-Type'] = 'text/html'
		html = df.to_html(index=False)
		html = df.to_html(index=False)
		i = 0
		for col in df.columns:
			html = html.replace('<th>{}'.format(col),'<th><a onclick="sortTable({},"table0");"><b>{}</b></a>'.format(i,col))
			i += 1
		html = html.replace('border="1" class="dataframe"','class="sortable" id="sortable"')
		html = html.replace('style="text-align: right;"','')
		return html

	@cherrypy.expose
	def html(self, **args):
		html = self.getHTML(args)
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return html

class Launch:
	templateVars = {"title" : "Title",
					"html" : "",
					"shared_fields" : [
								{"label": 'Title', "value": 'Graph Title', "variable_name": 'var1', "input_type":'text'},
						],
					"controls" : [
					{"output_type" : "image",
						"control_type" : "button",
						"control_name" : "load_image",
						"button_label" : "Make Line Graph",
						"button_id" : "submit-plot",
					},
					{"output_type" : "table",
						"control_type" : "button",
						"control_name" : "load_table",
						"button_label" : "Load Table",
						"button_id" : "load-table",
						"on_page_load" : "true",
					},
					{"output_type" : "html",
						"control_type" : "button",
						"control_name" : "load_html",
						"button_label" : "show html",
						"button_id" : "show-html",
					},
					]
				}
				
	def getJsonData(self, input_params):
		"""turns the DataFrame returned by getData into a dictionary

		arguments:
		the input_params passed used for table or d3 outputs are forwarded on to getData
		"""
		df = self.getData(input_params)
		return df.to_dict(outtype='records')

	def getData(self, input_params):
		"""Override this function

		arguments:
		input_params (dict)

		returns:
		DataFrame
		"""
		count = [1,4,3]
		name = ['Red','Green','Blue']
		df = pd.DataFrame({'name':name, 'count':count})
		return df

	def getPlot(self, input_params):
		"""Override this function

		arguments:
		input_params (dict)

		returns:
		matplotlib.pyplot figure
		"""
		print input_params
		title = input_params['var1']
		x = range(0,10)
		fig = plt.figure()
		splt = fig.add_subplot(1,1,1)
		splt.set_title(title)
		splt.plot(x,x)
		return fig

	def getD3(self):
		d3 = {}
		d3['css'] = ""
		d3['js'] = ""
		return d3

	def getHTML(self, input_params):
		return "<b>hello</b> <i>world</i>"

	def launch(self,host="local",port=8080):
		webapp = Root(templateVars=self.templateVars, getJsonDataFunction=self.getJsonData, getDataFunction=self.getData, getPlotFunction=self.getPlot, getD3Function=self.getD3, getHTMLFunction=self.getHTML)
		if host!="local":
			cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.server.socket_port = port
		cherrypy.quickstart(webapp)

if __name__=='__main__':
	l = Launch()
	l.launch()
