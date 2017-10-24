import cPickle as pickle
# import _pickle as pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


SmallInFn = "pickles/Small_In_Degree_Distribution.pickle"
SmallOutFn = 'pickles/Small_Out_Degree_Distribution.pickle'


def graph(opts):
	fig = plt.figure()

	axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

	axes.set_xlabel(opts['xlabel'])
	axes.set_ylabel(opts['ylabel'])
	if opts['log']: axes.set_yscale('log')
	axes.set_title(opts['title'])
	fig.savefig(opts['filename'])

def main():
	small = pickle.load(open(SmallOutFn, 'rb'))

	x_values = []
	
	for i in range(len(small)):
		x_values += [i]

	x = np.array(x_values)

	y = np.array(small)

	options = {}

	options['x'] = x
	options['xlabel'] = 'In degrees'
	options['ylabel'] = 'F'
	options['title'] = 'In degree'
	options['filename'] = 'diagrams/Small_Out_Degree_Distribution.png'
	options['log'] = True

	graph(options)


if __name__ == '__main__':
	main()





