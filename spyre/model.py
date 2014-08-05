import matplotlib.pyplot as plt
import matplotlib
import ggplot

from time import sleep
import string
import random
import os 
import tempfile

class Plot:
	def getPlotPath(self, plt_obj):
		temp_file  = tempfile.NamedTemporaryFile()
		img_path = temp_file.name+'.png'
		if type(plt_obj).__name__ == 'Figure':
			plt_obj.savefig(img_path)
		if type(plt_obj).__name__ == 'ggplot':
			ggplot.ggsave(plt_obj,img_path)
		return(img_path)

