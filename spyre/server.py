import matplotlib
matplotlib.use('Agg')

import os, os.path
import json
import jinja2
import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import model
try:
	import View
except:
	import view as View

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.lib.static import serve_fileobj

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )
templateEnv = jinja2.Environment( loader=templateLoader )



class Root(object):
	def __init__(self,templateVars=None, title=None, inputs=None, outputs=None, controls=None, tabs=None, getJsonDataFunction=None, getDataFunction=None, getTableFunction=None, getPlotFunction=None, getImageFunction=None, getD3Function=None, getCustomCSSFunction=None, getCustomJSFunction=None, getHTMLFunction=None,  getDownloadFunction=None, noOutputFunction=None):
		# populate template dictionary for creating input,controler, and output HTML and javascript
		if templateVars is not None:
			self.templateVars = templateVars
		else:
			self.templateVars = {}
			if title is not None:
				self.templateVars['title'] = title
			if inputs is not None:
				self.templateVars['inputs'] = inputs
			if controls is not None:
				self.templateVars['controls'] = controls
			if outputs is not None:
				self.templateVars['outputs'] = outputs
			if tabs is not None:
				self.templateVars['tabs'] = tabs

		self.getJsonData = getJsonDataFunction
		self.getData = getDataFunction
		self.getTable = getTableFunction
		self.getPlot = getPlotFunction
		self.getImage = getImageFunction
		self.getD3 = getD3Function
		self.getCustomJS = getCustomJSFunction
		self.getCustomCSS = getCustomCSSFunction
		self.getHTML = getHTMLFunction
		self.noOutput = noOutputFunction
		self.getDownload = getDownloadFunction
		d3 = self.getD3()
		custom_js = self.getCustomJS()
		custom_css = self.getCustomCSS()

		self.templateVars['d3js'] = d3['js']
		self.templateVars['d3css'] = d3['css']
		self.templateVars['custom_js'] = custom_js
		self.templateVars['custom_css'] = custom_css

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
	def image(self, **args):
		args = self.clean_args(args)
		img = self.getImage(args)
		d = model.Image()
		buffer = d.getImagePath(img)
		cherrypy.response.headers['Content-Type'] = 'image/jpg'
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
		df = self.getTable(args)
		html = df.to_html(index=False, escape=False)
		i = 0
		for col in df.columns:
			html = html.replace('<th>{}'.format(col),'<th><a onclick="sortTable({},"table0");"><b>{}</b></a>'.format(i,col))
			i += 1
		html = html.replace('border="1" class="dataframe"','class="sortable" id="sortable"')
		html = html.replace('style="text-align: right;"','')
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return html

	@cherrypy.expose
	def html(self, **args):
		args = self.clean_args(args)
		html = self.getHTML(args)
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return html

	@cherrypy.expose
	def download(self, **args):
		args = self.clean_args(args)
		filepath = self.getDownload(args)
		if type(filepath).__name__=="str":
			return serve_file(filepath, "application/x-download", "attachment", name='data.csv')
		if type(filepath).__name__=="instance":
			return serve_fileobj(filepath.getvalue(), "application/x-download", "attachment", name='data.csv')
		else:
			return "error downloading file. filepath must be string of buffer"

	@cherrypy.expose
	def no_output(self, **args):
		args = self.clean_args(args)
		self.noOutput(args)
		return ''

	@cherrypy.expose
	def spinning_wheel(self, **args):
		v = View.View()
		buffer = v.getSpinningWheel()
		cherrypy.response.headers['Content-Type'] = 'image/gif'
		return buffer.getvalue()

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


class App:

	title = None
	inputs = [{		"input_type":'text',
					"label": 'Variable', 
					"value" : "Value Here",
					"variable_name": 'var1'}]

	controls = None

	outputs = [{	"output_type" : "plot",
					"output_id" : "plot",
					"control_id" : "button1",
					"on_page_load" : "true"}]
	outputs = None
	inputs = None
	tabs = None
	templateVars = None
				
	def getJsonData(self, params):
		"""turns the DataFrame returned by getData into a dictionary

		arguments:
		the params passed used for table or d3 outputs are forwarded on to getData
		"""
		df = self.getData(params)
		return df.to_dict(outtype='records')

	def getData(self, params):
		"""Override this function

		arguments:
		params (dict)

		returns:
		DataFrame
		"""
		try:
			return eval("self."+str(params['output_id'])+"()")
		except:
			return pd.DataFrame({'name':['Override','getData() method','to generate tables'], 'count':[1,4,3]})

	def getTable(self, params):
		"""Used to create html table. Uses dataframe returned by getData by default
		override to return a different dataframe.

		arguments: params (dict)
		returns: html table
		"""
		return self.getData(params)

	def getDownload(self, params):
		"""Override this function

		arguments: params (dict)
		returns: path to file or buffer to be downloaded (string or buffer)
		"""
		df = self.getData(params)
		buffer = StringIO.StringIO()
		df.to_csv(buffer, index=False)
		filepath = buffer
		return filepath

	def getPlot(self, params):
		"""Override this function

		arguments:
		params (dict)

		returns:
		matplotlib.pyplot figure
		"""
		try:
			return eval("self."+str(params['output_id'])+"()")
		except:
			plt.title("Override getPlot() method to generate figures")
			return plt.gcf()

	def getImage(self, params):
		"""Override this function

		arguments: params (dict)
		returns: matplotlib.image (figure)
		"""
		try:
			return eval("self."+str(params['output_id'])+"()")
		except:
			return np.array([[0,0,0]])

	def getHTML(self, params):
		"""Override this function

		arguments: params (dict)
		returns: html (string)
		"""
		try:
			return eval("self."+str(params['output_id'])+"()")
		except:
			return "<b>Override</b> the getHTML method to insert your own HTML <i>here</i>"

	def noOutput(self, params):
		"""Override this function
		A method for doing stuff that doesn't reququire an output (refreshing data,
			updating variables, etc.)

		arguments:
		params (dict)
		"""
		try:
			return eval("self."+str(params['output_id'])+"()")
		except:
			pass

	def getD3(self):
		d3 = {}
		d3['css'] = ""
		d3['js'] = ""
		return d3

	def getCustomJS(self):
		"""Override this function

		returns:
		string of javascript to insert on page load
		"""
		return ""

	def getCustomCSS(self):
		"""Override this function

		returns:
		string of css to insert on page load
		"""
		return ""

	def launch(self,host="local",port=8080):
		webapp = self.getRoot()
		if host!="local":
			cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.server.socket_port = port
		cherrypy.quickstart(webapp)

	def launch_in_notebook(self, port=9095, width=900, height=600):
		"""launch the app within an iframe in ipython notebook"""
		from IPython.lib import backgroundjobs as bg
		from IPython.display import HTML

		jobs = bg.BackgroundJobManager()
		jobs.new(self.launch, kw=dict(port=port))
		return HTML('<iframe src=http://localhost:{} width={} height={}></iframe>'.format(port,width,height))

	def getRoot(self):
		webapp = Root(templateVars=self.templateVars, title=self.title, inputs=self.inputs, outputs=self.outputs, controls=self.controls, tabs=self.tabs, getJsonDataFunction=self.getJsonData, getDataFunction=self.getData, getTableFunction=self.getTable, getPlotFunction=self.getPlot, getImageFunction=self.getImage, getD3Function=self.getD3, getCustomJSFunction=self.getCustomJS, getCustomCSSFunction=self.getCustomCSS, getHTMLFunction=self.getHTML, getDownloadFunction=self.getDownload, noOutputFunction=self.noOutput)
		return webapp

class Launch(App):
	"""Warning: This class is depricated. Use App instead"""
 
if __name__=='__main__':
	app = App()
	app.launch()
