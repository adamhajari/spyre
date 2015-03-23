#!/user/bin/env python

from spyre.server import Site, App


from simple_sine_example import SimpleSineApp
from stocks_w_bokeh_example import MyLaunch
from NBS_category_example import NBSCategoriesApp



class Index(App):
    def getHTML(self, params):
        return "Title Page Here"


#site = Site(Index)

site = Site(SimpleSineApp)

site.addApp(MyLaunch, '/sineapp')
site.addApp(NBSCategoriesApp, '/sineapp/mylaunch')


site.launch()






