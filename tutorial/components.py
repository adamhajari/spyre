from spyre import server
import matplotlib.image as mpimg

class InputExample(server.Launch):

	templateVars = {"title" : "Inputs",
					"inputs" : [{	"input_type":'text',
									"label" : 'Text Box',
									"value" : 'text',
									"variable_name": 'text_box', 
								},
								{	"input_type":'radiobuttons',
									"label" : 'Radio Buttons',
									"options" : [
										{"label": "A", "value":1, "checked":True}, 
										{"label":"B", "value":2}
									],
									"variable_name": 'radio_buttons',
								},
								{	"input_type":'checkboxgroup',
									"label" : 'Checkboxes',
									"options" : [
										{"label": "red", "value":1, "checked":True}, 
										{"label":"blue", "value":2},
										{"label":"green", "value":3}
									],
									"variable_name": 'check_boxes', 
								},
								{	"input_type":'dropdown',
									"label" : 'Dropdown Menu',
									"options" : [{"label":"option 1", "value":1},
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
									"on_page_load" : False,
								}]
				}

	def getImage(self, params):
		img = mpimg.imread('spyre_outputs.png')
		return img

	def noOutput(self, input_params):
		pass

l = InputExample()
l.launch(port=9096)
