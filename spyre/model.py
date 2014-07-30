# import matplotlib.pyplot as plt
# import matplotlib
import ggplot

from time import sleep
import string
import random
import os 

class Plot:
	def __init__(self,root_dir):
		self.ROOT_DIR = root_dir

	def generateRandomString(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	def clearOutTmpDir(self):
		folder = self.ROOT_DIR+'/public/images/tmp/'
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception, e:
				print e

	def getPlotPath(self, plt_obj):
		self.clearOutTmpDir()
		tmp_name = self.generateRandomString(16)
		img_path = self.ROOT_DIR+'/public/images/tmp/'+tmp_name+'.png'
		rel_img_path = '/static/images/tmp/'+tmp_name+'.png'
		if type(plt_obj).__name__ == 'Figure':
			plt_obj.savefig(img_path)
		if type(plt_obj).__name__ == 'ggplot':
			ggplot.ggsave(plt_obj,img_path)
		return(rel_img_path)

