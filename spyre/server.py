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
	def __init__(self,templateVars=None, getJsonDataFunction=None, getDataFunction=None, getPlotFunction=None, getD3Function=None, getHTMLFunction=None, noOutputFunction=None):
		self.templateVars = templateVars
		self.getJsonData = getJsonDataFunction
		self.getData = getDataFunction
		self.getPlot = getPlotFunction
		self.getD3 = getD3Function
		self.getHTML = getHTMLFunction
		self.noOutput = noOutputFunction
		d3 = self.getD3()
		self.templateVars['d3js'] = d3['js']
		self.templateVars['d3css'] = d3['css']

		v = View.View()
		self.templateVars['js'] = v.getJS()
		self.templateVars['css'] = v.getCSS()

	@cherrypy.expose
	def index(self):
		v = View.View()
		template = jinja2.Template(v.getHTML())
		return template.render( self.templateVars )

	@cherrypy.expose
	def plot(self, **args):
		args = self.clean_args(args)
		p = self.getPlot(args)
		d = model.Plot()
		buffer = d.getPlotPath(p)
		cherrypy.response.headers['Content-Type'] = 'image/png'
		return buffer.getvalue()

	@cherrypy.expose
	def data(self, **args):
		args = self.clean_args(args)
		data = self.getJsonData(args)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({'data':data,'args':args})

	@cherrypy.expose
	def table(self, **args):
		args = self.clean_args(args)
		df = self.getData(args)
		cherrypy.response.headers['Content-Type'] = 'text/html'
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
		args = self.clean_args(args)
		html = self.getHTML(args)
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return html

	@cherrypy.expose
	def no_output(self, **args):
		args = self.clean_args(args)
		self.noOutput(args)
		return ''

	def clean_args(self,args):
		for k,v in args.iteritems():
			# turn checkbox group string into a list
			if v.rfind("__list__") == 0:
				tmp = v.split(',')
				if len(tmp)>1:
					args[k] = tmp[1:]
				else:
					args[k] = []
			# convert to a number
			if v.rfind("__float__") == 0:
				args[k] = float(v[9:])
		return args


class Launch:
	templateVars = templateVars = {"title" : "Title Here",
					"inputs" : [{	"input_type":'text',
									"label": 'Variable', 
									"value" : "Value Here",
									"variable_name": 'var1', 
								}],
					"controls" : [{	"control_type" : "button",
									"control_id" : "button1",
									"label" : "Button Label Here",
								}],
					"outputs" : [{	"output_type" : "plot",
									"output_id" : "plot",
									"control_id" : "button1",
									"on_page_load" : "true",
								}]
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
		plt.title("Override getPlot() method to generate figures")
		plt.xlabel(input_params['var1'])
		return plt.gcf()

	def getHTML(self, input_params):
		"""Override this function

		arguments:
		input_params (dict)

		returns:
		html string
		"""
		return "<b>hello</b> <i>world</i>"

	def noOutput(self, input_params):
		"""Override this function
		A method for doing stuff that doesn't reququire an output (refreshing data,
			updating variables, etc.)

		arguments:
		input_params (dict)
		"""
		pass

	def getD3(self):
		d3 = {}
		d3['css'] = ""
		d3['js'] = ""
		return d3

	def launch(self,host="local",port=8080):
		webapp = Root(templateVars=self.templateVars, getJsonDataFunction=self.getJsonData, getDataFunction=self.getData, getPlotFunction=self.getPlot, getD3Function=self.getD3, getHTMLFunction=self.getHTML, noOutputFunction=self.noOutput)
		if host!="local":
			cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.server.socket_port = port
		cherrypy.quickstart(webapp)

if __name__=='__main__':
	l = Launch()
	l.launch()
