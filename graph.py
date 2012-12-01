import numpy
import matplotlib.pyplot as plt
 
class Graph:
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
    def generate_graph(points, filename, ytitle):
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
    def generate_twograph(points1, points2, filename, ytitle, label1, label2):
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