Inputs
=========

- The inputs to spyre are a list of dictionaries. 
- Each element in the list represents an input type (for example text box) Other types are documented below
- Each element has some mandatory attributes: (type, key) and some optional attributes (label, value, actionid)


Types
=========

TextBox
+++++++++++++

This is an example of the text input element
::

    { 
        "type":'text',
        "label": 'Title', 
        "value" : 'Simple Sine Wave',
        "key": 'title', 
        "action_id" : "refresh",
    }


RadioButton
+++++++++++++


This is an example of the RadioButton input element
::

    {   
        "type":'radiobuttons',
        "label": 'Function', 
        "options" : [
            {"label": "Sine", "value":"sin", "checked":True}, 
            {"label":"Cosine", "value":"cos"}
        ],
        "key": 'func_type', 
        "action_id" : "refresh",
    },

Checkbox Group 
++++++++++++++++++

This is an example of the Checkbox Group input element
::

    {   
        "type":'checkboxgroup',
        "label": 'Axis Labels', 
        "options" : [
            {"label": "x-axis", "value":"x", "checked":True}, 
            {"label":"y-axis", "value":"y"}
        ],
        "key": 'axis_label', 
        "action_id" : "refresh",
    }

Dropdown
++++++++++++++++++

This is an example of the Dropdown input element
::
    {   
        "type":'dropdown',
        "label": 'Line Color', 
        "options" : colors,
        "key": 'color', 
        "action_id" : "refresh",
        "linked_key": 'title', 
        "linked_type": 'text', 
        "linked_value":"hey"
    }

Slider Input
++++++++++++++++++

This is an example of the Slider input element
::

    {   
        "type":'slider',
        "label": 'frequency', 
        "key": 'freq', 
        "value" : 2,
        "min" : 1, 
        "max" : 30,
        "action_id" : "refresh",
        "linked_key": 'title', 
        "linked_type": 'text', 
    }