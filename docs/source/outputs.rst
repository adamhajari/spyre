Outputs
=========

The attributes for the outputs for a spyre app are defined as a list of dictionaries. Each element in the outputs list should have a corresponding method which generates that output. The output dictionary should specify the type and provide and id. The id must be alphanumeric and cannot start with a number. Outputs can also have a control_id key, which references an id from the controls list.  

By default the outputs load on page load using the default values for each of the inputs. If an output should not load on page load, set the 'on_page_load' attribute to False (see example for Download output type)

Generating outputs
-------------------
There are a few options for generating an output's content.

Overriding the method from the server.App class
+++++++++++++++++++++++++++++++++++++++++++++++++

Each output type has a corresponding method in the server.App class that gets called whenever an instance of that output get displayed in the app. For instance, if an html output is included in your list of outputs, server.App's getHTML() method gets called everytime that block of html gets loaded. 

You can override the methods for each of the output types. For instance, if an app had an html output that was suppose to display the string `Be <b>bold</b>`, you could include this method in your app's class::

    getHTML(self, params):
        return "be <b>bold</b>"

Matching the method name to the output id
++++++++++++++++++++++++++++++++++++++++++

If server.App's built-in output method isn't overridden for an output in the app's outputs list, the built-in method will look for a method with a name matching the output id. Suppose, for instance, our app only has one output::

    outputs = [{ 'type':'html',
                 'id':'aphorism1'}]

If we do not overide the getHTML method, server.App's getHTML method will look for a method named "aphorism1". We can generate output then by creating an output that matches that name::

    def aphorism1(self, params):
        return "if it ain't broke, don't fix it."

If we have more than one output of the same type, we can use the method naming convention to generate outputs for both of them::

    outputs = [{ 'type':'html',
                 'id':'aphorism1'},
                 { 'type':'html',
                 'id':'aphorism2'},
                 { 'type':'html',
                 'id':'aphorism3'},]
    
    def aphorism1(self, params):
        return "if it ain't broke, don't fix it."

    def aphorism2(self, params):
        return "The art of prophecy is very difficult - especially with respect to the future."

    def aphorism3(self, params):
        return "All you need in this life is ignorance and confidence, and then success is sure. "

Including a getData method
+++++++++++++++++++++++++++

The getData method can be used to generate the output for tables, plots, or downloads. The getData method should return a pandas dataframe and will be converted into the approriate output. Using getData, an app can generate up to three outputs with a single method.


Output types
--------------

Table
+++++++++++++
::

    { 
        'type':'table',
        'id':'average_rainfall_table'
    }


Plot
+++++++++++++
::

    { 
        'type':'plot',
        'id':'average_rainfall_linegraph'
    }


HTML
++++++++++++++++++
::

    { 
        'type':'html',
        'id':'readme'
    }


Image
++++++++++++++++++
::

    { 
        'type':'image',
        'id':'cat_photo'
    }


Download
++++++++++++++++++
::

    { 
        'type':'download',
        'id':'results_csv',
        'on_page_load':False
    }
