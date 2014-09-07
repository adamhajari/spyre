import matplotlib.pyplot as plt
import matplotlib
import StringIO

class Plot:
	def getPlotPath(self, plt_obj):
		buffer = StringIO.StringIO()
		if type(plt_obj).__name__ == 'Figure':
			plt_obj.savefig(buffer,format='png',bbox_inches='tight')
		plt.close('all')
		return(buffer)

