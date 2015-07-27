# Outputs
All outputs are displayed to the right of the control panel. The order of outputs and which tabs each output is displayed in (if using tabs) is defined in the [output dictionary](inputs_outputs_controls.md). For each output type there is a corresponding method that must be defined in order to define how the output is generated. You saw in the [Getting Started](index.md) section that the output type `plot` requires a `getPlot` method to generate a matplotlib figure.  The other three output type -> method name mappings are

1. `table` -> `getTable`
2. `html` -> `getHtml`
3. `image` -> `getImage`
4. `download` -> `getDownload`

There is also a `get


The output_id defined in the output dictionary can be used as the method name fo the method that generates

## Generating an Output
xoxo

## Input Parameters
xoxo

## Output Types
### plots
xoxo

### tables

### html

### images

### downloads

## generating a plot
Let's get back to our getPlot method. Notice that it takes a single argument: params. params is a dictionary containing:

1. all of the input values (with key equal to the variable_name specified in the input dictionary)
2. the output_id for the output that needs to get created.

For this simple example you can ignore the output_id. With the exception of the input type "checkboxgroup", the value of each of the params is a string. In this example our one input variable represents a frequency, which is a number, so we'll need to cast it as a float before we use it.  The matplotlib figure returned by getPlot will be displayed in the right panel of our Spyre app.