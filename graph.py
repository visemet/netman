import numpy
import matplotlib.pyplot as plt
from collections import defaultdict

class Graph:

    def __init__(self, name, ytitle):
        self._name = name
        self._ytitle = ytitle
        self._data_sets = defaultdict(list) #dictionary of data sets. name:datalist

    def add_data_set(self, name, new_list):
        self._data_sets[name] = new_list

    def generate_single_graphs(self):
        for n in self._data_sets.keys():
            d = self._data_sets[n]
            self.generate_graph(d, n, n)

    def generate_total_graph(self):
        p = plt.figure()
        p.suptitle(self._name)
        ax = p.add_subplot(111)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel(self._ytitle)
        set_count = 0
        color_count = 0
        colors = ["r", "b", "y"]
        #init to first value
        legend_colors = ()
        legend_labels = ()
        for n in self._data_sets.keys():
            d = self._data_sets[n]
            if d == None:
                continue
            prevpoint = (0,0)
            color = colors[color_count] + '-'
            for x,y in d:
                # plot x1,x2 y1,y2
                ax.plot([prevpoint[0], x], [prevpoint[1], y], color)
                prevpoint = (x,y)
            # add the legend values
            legend_colors += (plt.Rectangle((0, 0), 1, 1, fc=colors[color_count]),)
            legend_labels += (n,)
            color_count += 1
        p.legend(legend_colors, legend_labels)
        p.savefig('gen_graphs/' + self._name + '_all.png')

    '''
    @param
        points = list[] of (x,y) where x is the x-coordinate and y is the y-coordinate
            chose dictionary for purposes of aggregating data at a single point so it's
            easier for the data-collecting function--change?
        filename: ex. windowSize.
        ytitle - technically we could just use the filename, but this allows us
            to specify units. xtitle is always going to be time

    File will be saved as <filename>.png

    '''
    def generate_graph(self,points, filename, ytitle):
        p = plt.figure()
        p.suptitle(filename)
        ax = p.add_subplot(111)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(ytitle)
        #graph the line between the previous point and the current point.
        #Always start the previous point at the origin TODO: is this okay?
        #After every iteration, update the previous point to be the current point
        prevpoint = (0,0)
        for x,y in points:
            # plot x1,x2 y1,y2
            ax.plot([prevpoint[0], x], [prevpoint[1], y], 'r-')
            prevpoint = (x,y)
        p.savefig(filename + '.png')

    '''
    @param
        points1, points2 are the two (related) data sets that will be graphed
        filename: ex. windowSize.
        ytitle - technically we could just use the filename, but this allows us
            to specify units. xtitle is always going to be time
        label1, label2 are the labels in the legend
    File will be saved as <filename>.png

    '''
    def generate_twograph(self, points1, points2, filename, ytitle, label1, label2):
        p = plt.figure()
        p.suptitle(filename)
        ax = p.add_subplot(111)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(ytitle)
        #graph the line between the previous point and the current point.
        #Always start the previous point at the origin TODO: is this okay?
        #After every iteration, update the previous point to be the current point
        prevpoint = (0,0)
        for x,y in points1:
            # plot x1,x2 y1,y2
            ax.plot([prevpoint[0], x], [prevpoint[1], y], 'r-')
            prevpoint = (x,y)
        prevpoint = (0,0)
        for x,y in points2:
            # plot x1,x2 y1,y2
            ax.plot([prevpoint[0], x], [prevpoint[1], y], 'b-')
            prevpoint = (x,y)
        # add the legend
        p1 = plt.Rectangle((0, 0), 1, 1, fc="r")
        p2 = plt.Rectangle((0, 0), 1, 1, fc="b")
        p.legend((p1, p2), (label1, label2))
        p.savefig(filename + '.png')
