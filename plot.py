# prints thermo graphic of image and pixel likelihood
import matplotlib.pyplot as plt

def printPlot(array):
	fig, ax = plt.subplots()

	cax = ax.imshow(array, interpolation='nearest', cmap='jet')

	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	cbar = fig.colorbar(cax, ticks=[-1,0,1])
	cbar.ax.set_yticklabels(['', '', ''])  # vertically oriented colorbar

	plt.show()

arr = [[0 for row in range(2)] for col in range(2)]
arr = [[68.95,31.05], [32.27,67.73]]

printPlot(arr)
