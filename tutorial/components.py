from spyre import server
import matplotlib.image as mpimg

class InputExample(server.Launch):

	templateVars = {"title" : "Inputs",
					"inputs" : [{	"input_type":'text',
									"value" : 'Text Box',
									"variable_name": 'text_box', 
								},
								{	"input_type":'radiobuttons',
									"options" : [
										{"label": "Radio", "value":1, "checked":True}, 
										{"label":"Buttons", "value":2}
									],
									"variable_name": 'radio_buttons',
								},
								{	"input_type":'checkboxgroup',
									"options" : [
										{"label": "check", "value":1, "checked":True}, 
										{"label":"boxes", "value":2}
									],
									"variable_name": 'check_boxes', 
								},
								{	"input_type":'dropdown',
									"options" : [{"label":"Dropdown Menu", "value":1},
    											 {"label": "option 2", "value":2} ],
									"variable_name": 'dd_menu', 
									"action_id" : "html_output",
								},
								{	"input_type":'slider',
									"label": 'Slider', 
									"variable_name": 'slider_input', 
									"value" : 5,
									"min" : 1, 
									"max" : 30,
									"action_id" : "html_output",
								}],
					"controls" : [{	"control_type" : "button",
									"control_id" : "button1",
									"label" : "Button",
								}],
					"outputs" : [{	"output_type" : "image",
									"output_id" : "image_output",
									"control_id" : "button1",
									"on_page_load" : True,
								},
								{	"output_type" : "no_output",
									"output_id" : "make_alert",
									"alert_message" : "you pressed a button",
									"control_id" : "button1",
								}]
				}

	def getImage(self, params):
		img = mpimg.imread('spyre_outputs.png')
		return img

	def noOutput(self, input_params):
		pass

l = InputExample()
l.launch(port=9096)
