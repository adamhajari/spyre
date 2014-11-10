from spyre import server
import matplotlib.image as mpimg

class InputExample(server.Launch):

	templateVars = {"title" : "Inputs",
					"inputs" : [{	"input_type":'radiobuttons',
									"options" : [
										{"label": "Simple App", "value":1, "checked":True}, 
										{"label":"Multiple Outputs", "value":2},
										{"label":"Inputs with actions 1", "value":3},
										{"label":"Inputs with actions 2", "value":4},
									],
									"variable_name": 'slide_selector',
								}],
					"controls" : [{	"control_type" : "hidden",
									"control_id" : "button1",
									"label" : "Button",
								}],
					"outputs" : [{	"output_type" : "image",
									"output_id" : "image_output",
									"control_id" : "button1",
									"on_page_load" : True,
								}]
				}

	def getImage(self, params):
		slide_selector = params['slide_selector']
		absolut_path = '/Users/adamhajari/Projects/python/cherrypy/dataspyre/tutorial/'
		if slide_selector==2:
			img = mpimg.imread(absolute_path+'slide2.png')
		elif slide_selector==3:
			img = mpimg.imread(absolute_path+'slide3.png')
		elif slide_selector==3:
			img = mpimg.imread(absolute_path+'slide4.png')
		else:
			img = mpimg.imread(absolute_path+'slide1.png')
		
		return img

	def noOutput(self, input_params):
		pass

l = InputExample()
l.launch(port=9096)
