import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
# from StringIO import StringIO
import io

class Plot:
	def getPlotPath(self, plt_obj):
		buffer = io.BytesIO()
		if isinstance(plt_obj, plt.Figure):
			plt_obj.savefig(buffer,format='png',bbox_inches='tight')
		if isinstance(plt_obj, matplotlib.axes.Axes):
			plt_obj.get_figure().savefig(buffer,format='png',bbox_inches='tight')
		else:
			print("Error: getPlot method must return an pyplot figure or matplotlib Axes object")
		plt.close('all')
		return(buffer)

class Image:
	def getImagePath(self, img_obj):
		buffer = io.BytesIO()
		mpimg.imsave(buffer,img_obj)
		try:
			mpimg.imsave(buffer,img_obj)
		except:
			print("Error: getImage method must return an image object")
		return(buffer)
