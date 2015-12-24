import __main__
import os
import codecs
import sys
import matplotlib.image as mpimg
import io
from imp import reload
reload(sys)

ENCODING = 'utf-8'
try:
	sys.setdefaultencoding(ENCODING)
except:
	print("Warning: unable to set defaultencoding to utf-8")

class View:
	def __init__(self):
		self.ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
		self.JS_PATH = os.path.join(self.ROOT_DIR, 'public', 'js')
		self.CSS_PATH = os.path.join(self.ROOT_DIR, 'public', 'css')
		self.APP_PATH = os.path.dirname(os.path.realpath(__main__.__file__))

	def getHTML(self):
		file_path = os.path.join(self.ROOT_DIR, 'view.html')
		f = codecs.open(file_path, 'r', ENCODING)
		html = f.read()
		f.close()
		return html

	def getJS(self):
		self.JS = ""
		for file in os.listdir(self.JS_PATH):
			if file.find('.js')>0:
				file_path = os.path.join(self.JS_PATH, file) 
				f = codecs.open(file_path, 'rb')
				content = f.read()
				f.close()
				self.JS += content.decode('utf-8')
				self.JS += "\n"
		return self.JS

	def getCSS(self):
		self.CSS = ""
		for file in os.listdir(self.CSS_PATH):
			if file.find('.css')>0:
				file_path = os.path.join(self.CSS_PATH, file) 
				f = open(file_path, 'rb')
				content = f.read()
				f.close()
				self.CSS += content.decode('utf-8')
				self.CSS += "\n"
		return self.CSS

	def getSpinningWheel(self, spinnerFile=None):
		buffer = io.BytesIO()
		if spinnerFile is None:
			path = os.path.join(self.ROOT_DIR, 'public', 'images', "loading_wheel.gif")
		else:
			path = os.path.join(self.APP_PATH, spinnerFile)
		f = open( path,'rb' )
		buffer.write(f.read())
		f.close()
		return(buffer)
