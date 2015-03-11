#!/user/bin/env python

from spyre.server import Site


from simple_sine_example import SimpleSineApp
from stocks_w_bokeh_example import MyLaunch
from NBS_category_example import NBSCategoriesApp


site = Site(SimpleSineApp)
site.addApp(MyLaunch, '/mylaunch')
site.addApp(NBSCategoriesApp, '/nbs')


site.launch()
