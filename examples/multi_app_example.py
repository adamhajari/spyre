#!/user/bin/env python

from spyre.server import Site, App


from sliders_examples import SlidersApp
from stocks_example import StockExample
from image_editor import ImageEditor


class Index(App):
    def getHTML(self, params):
        return "Title Page Here"


site = Site(SlidersApp)

site.addApp(StockExample, '/app2')
site.addApp(ImageEditor, '/app2/app3')


site.launch()
