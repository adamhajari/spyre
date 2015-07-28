Inputs
=========

Inputs for a spyre app are defined as a list of dictionaries. Each element in the list represents a different input and the attributes for each input are defined in these dictionaries.  Each input type has some mandatory attributes: (i.e. type, key) and some optional attributes (i.e. label, value, action_id)


Types
-------

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