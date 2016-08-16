import matplotlib
matplotlib.use('Agg')

import os, os.path
import json
import jinja2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

try:
	import StringIO as io  	# python2
except:
	import io 				# python3

try:
	from . import model
except:
	import model

try:
	from . import View
except:
	try:
		import View
	except:
		from . import view as View

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.lib.static import serve_fileobj

# Settings
include_df_index = False

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )
templateEnv = jinja2.Environment( loader=templateLoader )



class Root(object):
	def __init__(self,templateVars=None, 
		title="", 
		inputs=[], 
		outputs=[], 
		controls=[], 
		tabs=None,
		spinnerFile=None,
		getJsonDataFunction=None, 
		getDataFunction=None, 
		getTableFunction=None, 
		getPlotFunction=None, 
		getImageFunction=None, 
		getD3Function=None, 
		getCustomCSSFunction=None, 
		getCustomJSFunction=None,
		getCustomHeadFunction=None, 
		getHTMLFunction=None,  
		getDownloadFunction=None, 
		noOutputFunction=None,
		storeUploadFunction=None,
		prefix='/'):

		# populate template dictionary for creating input,controler, and output HTML and javascript
		if templateVars is not None:
			self.templateVars = templateVars
		else:
			self.templateVars = {}
			self.templateVars['title'] = title
			if prefix[-1] == '/':
				self.templateVars['prefix'] = prefix[:-1]
			else:
				self.templateVars['prefix'] = prefix
			# necessary to ensure that spyre apps prior to version 0.2.0 still work
			for input in inputs:
				if 'input_type' in input:
					input['type'] = input['input_type']
				if 'variable_name' in input:
					input['key'] = input['variable_name']
				if 'linked_variable_name' in input:
					input['linked_key'] = input['linked_variable_name']
				if 'linked_variable_type' in input:
					input['linked_type'] = input['linked_variable_type']
			self.templateVars['inputs'] = inputs
			for control in controls:
				if 'control_type' in control:
					control['type'] = control['control_type']
				if 'control_id' in control:
					control['id'] = control['control_id']
			self.templateVars['controls'] = controls
			for output in outputs:
				if 'output_type' in output:
					output['type'] = output['output_type']
				if 'output_id' in output:
					output['id'] = output['output_id']
			self.templateVars['outputs'] = outputs
			if tabs is not None:
				self.templateVars['tabs'] = tabs
			if spinnerFile is not None:
				self.templateVars['spinnerFile'] = spinnerFile
		self.defaultTemplateVars = self.templateVars

		self.getJsonData = getJsonDataFunction
		self.getData = getDataFunction
		self.getTable = getTableFunction
		self.getPlot = getPlotFunction
		self.getImage = getImageFunction
		self.getD3 = getD3Function
		self.getCustomJS = getCustomJSFunction
		self.getCustomCSS = getCustomCSSFunction
		self.getCustomHead = getCustomHeadFunction
		self.getHTML = getHTMLFunction
		self.noOutput = noOutputFunction
		self.getDownload = getDownloadFunction
		self.storeUpload = storeUploadFunction
		d3 = self.getD3()
		custom_js = self.getCustomJS()
		custom_css = self.getCustomCSS()
		custom_head = self.getCustomHead()

		self.templateVars['d3js'] = d3['js']
		self.templateVars['d3css'] = d3['css']
		self.templateVars['custom_js'] = custom_js
		self.templateVars['custom_css'] = custom_css
		self.templateVars['custom_head'] = custom_head

		v = View.View()
		self.templateVars['document_ready_js'] = ""
		self.templateVars['js'] = v.getJS()
		self.templateVars['css'] = v.getCSS()

		self.upload_file = None

	@cherrypy.expose
	def index(self, **args):
		self.templateVars = copy.deepcopy(self.defaultTemplateVars)  # create a deepcopy so other people's changes aren't cached
		clean_args = self.clean_args(args)
		self.use_custom_input_values(clean_args)

		v = View.View()
		template = jinja2.Template(v.getHTML())
		return template.render( self.templateVars )

	def use_custom_input_values(self, args):
		input_registration = {}
		index = 0
		for input in self.templateVars['inputs']:
			input_key = input['key']
			# register inputs to be so we can look them up by their variable name later
			if 'action_id' in input:
				input_registration[input_key] = {"type":input['type'], "action_id":input['action_id']}
			else:
				input_registration[input_key] = {"type":input['type'], "action_id":None}


			if input_key in args.keys():
				# use value from request
				input_value = args[input_key]
			elif 'value' in input:
				# use value from template
				input_value = input['value']
			else:
				# no value specified
				index+=1
				continue

			# use the params passed in with the url switch out the default input values
			if input['type'] in ['text','slider','searchbox']:
				self.templateVars['inputs'][index]['value'] = input_value
			if input['type'] in ['radiobuttons', 'dropdown']:
				for option in input['options']:
					option['checked'] = (str(option['value']) == input_value)
			if input['type'] == 'checkboxgroup':
				index2 = 0
				for option in input['options']:
					if str(option['value']) in input_value:
						self.templateVars['inputs'][index]['options'][index2]['checked'] = True
					else:
						self.templateVars['inputs'][index]['options'][index2]['checked'] = False
					index2+=1
			index+=1


	@cherrypy.expose
	def plot(self, **args):
		args = self.clean_args(args)
		p = self.getPlot(args)
		if p is None:
			return None
		d = model.Plot()
		buffer = d.getPlotPath(p)
		cherrypy.response.headers['Content-Type'] = 'image/png'
		return buffer.getvalue()

	@cherrypy.expose
	def image(self, **args):
		args = self.clean_args(args)
		img = self.getImage(args)
		if img is None:
			return None
		d = model.Image()
		buffer = d.getImagePath(img)
		cherrypy.response.headers['Content-Type'] = 'image/jpg'
		return buffer.getvalue()

	@cherrypy.expose
	def data(self, **args):
		args = self.clean_args(args)
		data = self.getJsonData(args)
		if data is None:
			return None
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({'data':data,'args':args}).encode('utf8')

	@cherrypy.expose
	def table(self, **args):
		args = self.clean_args(args)
		df = self.getTable(args)
		if df is None:
			return ""
		html = df.to_html(index=include_df_index, escape=False)
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
		if html is None:
			return ""
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
	def upload(self, xfile):
		self.storeUpload(xfile.file)

	@cherrypy.expose
	def no_output(self, **args):
		args = self.clean_args(args)
		self.noOutput(args)
		return ''

	@cherrypy.expose
	def spinning_wheel(self, **args):
		v = View.View()
		spinnerFile = self.templateVars.get('spinnerFile')
		buffer = v.getSpinningWheel(spinnerFile)
		cherrypy.response.headers['Content-Type'] = 'image/gif'
		return buffer.getvalue()

	def clean_args(self,args):
		for k,v in args.items():
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


class App(object):

	title = ""

	#Will be used when there are more than one app in a site
	app_bar_html = None
	outputs = []
	inputs = []
	controls = []
	tabs = None
	spinnerFile = None
	templateVars = None
	prefix = '/'

	def getJsonData(self, params):
		"""turns the DataFrame returned by getData into a dictionary

		arguments:
		the params passed used for table or d3 outputs are forwarded on to getData
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
			df = self.getData(params)
			if df is None:
				return None
			return df.to_dict(orient='records')

	def getData(self, params):
		"""Override this function

		arguments:
		params (dict)

		returns:
		DataFrame
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
			return pd.DataFrame({'name':['Override','getData() method','to generate tables'], 'count':[1,4,3]})

	def getTable(self, params):
		"""Used to create html table. Uses dataframe returned by getData by default
		override to return a different dataframe.

		arguments: params (dict)
		returns: html table
		"""
		df = self.getData(params)
		if df is None:
			return None
		return df

	def getDownload(self, params):
		"""Override this function

		arguments: params (dict)
		returns: path to file or buffer to be downloaded (string or buffer)
		"""
		df = self.getData(params)
		buffer = io.StringIO()
		df.to_csv(buffer, index=False, encoding='utf-8')
		filepath = buffer
		return filepath

	def storeUpload(self, file):
		"""Override this function

		arguments: params (dict)
		returns: path to file or buffer to be downloaded (string or buffer)
		"""
		pass

	def getPlot(self, params):
		"""Override this function

		arguments:
		params (dict)

		returns:
		matplotlib.pyplot figure
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
			try:
				df = self.getData(params)
				if df is None:
					return None
				return df.plot()
			except:
				fig = plt.figure()  # make figure object
				splt = fig.add_subplot(1,1,1)
				splt.set_title("Override getPlot() method to generate figures")
				return fig

	def getImage(self, params):
		"""Override this function

		arguments: params (dict)
		returns: matplotlib.image (figure)
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
			return np.array([[0,0,0]])

	def getHTML(self, params):
		"""Override this function

		arguments: params (dict)
		returns: html (string)
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
			return "<b>Override</b> the getHTML method to insert your own HTML <i>here</i>"

	def noOutput(self, params):
		"""Override this function
		A method for doing stuff that doesn't reququire an output (refreshing data,
			updating variables, etc.)

		arguments:
		params (dict)
		"""
		try:
			return eval("self."+str(params['output_id'])+"(params)")
		except AttributeError:
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

	def getCustomHead(self):
		"""Override this function

		returns:
		html to put in html header
		"""
		return ""

	def launch(self,host="local",port=8080,prefix='/'):
		self.prefix = prefix
		webapp = self.getRoot()
		if host!="local":
			cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.server.socket_port = port
		cherrypy.tree.mount(webapp,prefix)
		cherrypy.quickstart(webapp)



	def launch_in_notebook(self, port=9095, width=900, height=600):
		"""launch the app within an iframe in ipython notebook"""
		from IPython.lib import backgroundjobs as bg
		from IPython.display import HTML

		jobs = bg.BackgroundJobManager()
		jobs.new(self.launch, kw=dict(port=port))
		return HTML('<iframe src=http://localhost:{} width={} height={}></iframe>'.format(port,width,height))

	def getRoot(self):
		webapp = Root(templateVars=self.templateVars, 
			title=self.title, 
			inputs=self.inputs, 
			outputs=self.outputs, 
			controls=self.controls,
			tabs=self.tabs,
			spinnerFile=self.spinnerFile,
			getJsonDataFunction=self.getJsonData, 
			getDataFunction=self.getData, 
			getTableFunction=self.getTable, 
			getPlotFunction=self.getPlot, 
			getImageFunction=self.getImage, 
			getD3Function=self.getD3, 
			getCustomJSFunction=self.getCustomJS, 
			getCustomCSSFunction=self.getCustomCSS, 
			getCustomHeadFunction=self.getCustomHead, 
			getHTMLFunction=self.getHTML, 
			getDownloadFunction=self.getDownload, 
			noOutputFunction=self.noOutput,
			storeUploadFunction=self.storeUpload,
			prefix=self.prefix)

		return webapp
class Site(object):
	"""Creates a 'tree' of cherrypy 'Root' objects that allow for the
		creation of multiple apps with routes to different 'apps.'
	Calling the launch method will return
	"""

	def __init__(self, appobj):
		self.site_app_bar = list()
		self.addIndex(appobj)

	def addIndex(self, appobj):
		self.site_app_bar.append(("/",
							appobj.app_bar_html or appobj.title or "/"))
		self.root = appobj().getRoot()



	def get_route(self, fullRoute):

		routeSplit = fullRoute.split('/')
		routeSplit.remove('')
		parent = self.root
		for route in routeSplit[:-1]:
			parent = getattr(parent, route)
		return parent, routeSplit[-1]

	def addApp(self, appobj, fullRoute):

		parent, route = self.get_route(fullRoute)

		self.site_app_bar.append((fullRoute,
						appobj.app_bar_html or appobj.title or route))

		setattr(parent, route, appobj().getRoot())

	def getRoot(self):
		"""A convenience method to make the site API similar to the app API,
			in terms of how the cherrypy Root object is retrieved"""
		return self.root

	def launch(self, host="local", port=8080):
		"""Calling the Launch method on a Site object will serve the top
			node of the cherrypy Root object tree"""

		#Need to add in the appbar if many apps
		self.root.templateVars['app_bar'] = self.site_app_bar
		for fullRoute, _ in self.site_app_bar[1:]:
			parent, route = self.get_route(fullRoute)
			parent.__dict__[route].templateVars['app_bar'] = self.site_app_bar


		if host != "local":
			cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.server.socket_port = port
		cherrypy.quickstart(self.root)

class Launch(App):
	"""Warning: This class is depricated. Use App instead"""

if __name__=='__main__':
	app = App()
	app.launch()
