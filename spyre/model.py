import matplotlib.pyplot as plt
import matplotlib
# import ggplot
import StringIO

class Plot:
	def getPlotPath(self, plt_obj):
		buffer = StringIO.StringIO()
		if type(plt_obj).__name__ == 'Figure':
			plt_obj.savefig(buffer,format='png',bbox_inches='tight')
		# if type(plt_obj).__name__ == 'ggplot':
		# 	ggplot.ggsave(plt_obj,filename=buffer,format='png')
		return(buffer)

