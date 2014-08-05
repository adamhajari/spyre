import os, os.path
import random
import string
import simplejson
import jinja2
import matplotlib.pyplot as plt

import model

import cherrypy

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )
templateEnv = jinja2.Environment( loader=templateLoader )



class Root(object):
	def __init__(self,templateVars=None, getDataFunction=None, getPlotFunction=None, getD3Function=None):
		self.templateVars = templateVars
		self.getData = getDataFunction
		self.getPlot = getPlotFunction
		self.getD3 = getD3Function
		d3 = self.getD3()
		self.templateVars['d3js'] = d3['js']
		self.templateVars['d3css'] = d3['css']
		print self.templateVars['d3css']

	@cherrypy.expose
	def index(self):
		template = templateEnv.get_template( "view.html" )
		return template.render( self.templateVars )

	def plot(self, **args):
		p = self.getPlot(args)
		d = model.Plot(ROOT_DIR)
		img_path = d.getPlotPath(p)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'img_path':img_path})
	plot.exposed = True

	def data(self, **args):
		data = self.getData(args)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'data':data,'args':args})
	data.exposed = True

class Launch:
	templateVars = {"shared_fields" : [
								{"label": 'Button 1', "value": 0, "variable_name": 'var1', "input_type":'text'},
						],
					"controls" : [
					{"output_type" : "image",
						"button_label" : "Make Bar Plot",
						"button_id" : "submit-plot",
						"text_fields" : []
					},
					{"output_type" : "table",
						"button_label" : "Load Table",
						"button_id" : "load-table",
						"text_fields" : []
					}
					]
				}
				
	def getData(self, params):
		var1 = int(params['var1'])
		x = [{'count': 620716, 'name': 'Musician'},{'count': 71294, 'name': 'Author'},{'count': 50807, 'name': 'Book'},{'count': 7834, 'name': 'Record Label'},{'count': 5237, 'name': 'Actor'}]
		return x[:var1]

	def getPlot(self, params):
		x = range(0,10)
		y = x
		fig = plt.figure()
		splt = fig.add_subplot(1,1,1)
		splt.plot(x,y)
		return fig

	def getD3(self):
		d3 = {}
		d3['css'] = ""
		d3['js'] = ""
		return d3

	def launch(self):
		self.conf = { 
			'/': {
				'tools.sessions.on':True,
				'tools.staticdir.root': ROOT_DIR
			},
			'/static': {
				'tools.staticdir.on':True,
				'tools.staticdir.dir':'./public'
			}
		}
		
		webapp = Root(templateVars=self.templateVars, getDataFunction=self.getData, getPlotFunction=self.getPlot, getD3Function=self.getD3)
		cherrypy.quickstart(webapp, '/', self.conf)

if __name__=='__main__':
	l = Launch()
	l.launch()
