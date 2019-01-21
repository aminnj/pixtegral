import time
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def pixtegrate(func,bounds,npoints=10000,sleep=-1.):
    """
    Args:
        func (function): Function to integrate
        bounds (tuple): 2-tuple for lower and upper bounds of range
        npoints (int): Number of points used to sample the function

    Returns:
        integral (float)
    """
    xmin, xmax = bounds
    xvals = np.linspace(xmin,xmax,npoints)
    try:
        # First assume the function operates on arrays
        yvals = func(xvals)
    except:
        # Then assume it operates on a single element
        yvals = np.vectorize(func)(xvals)
    ymin, ymax = yvals.min(), yvals.max()

    # Make a figure with no padding/margins and a black background
    fig,ax = plt.subplots()
    canvas = FigureCanvas(fig)
    fig.subplots_adjust(left=0,bottom=0,right=1,top=1)
    fig.set_facecolor("black")
    ax.set_xmargin(0.)
    ax.set_ymargin(0.)
    ax.axis("off")

    # Color y>=0 red and y<0 blue
    ax.fill_between(xvals,yvals,where=(yvals>=0.),edgecolor="r",facecolor="r",linewidth=0.)
    ax.fill_between(xvals,yvals,where=(yvals<0.),edgecolor="b",facecolor="b",linewidth=0.)

    # Draw and count red/blue pixels
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    img = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
    nred = (img[:,:,0] > 254).sum()
    nblue = (img[:,:,2] > 254).sum()

    # Count filled fraction of image (red-blue), and normalize to actual bounding box
    integral = (nred-nblue)/(width*height)*((ymax-ymin)*(xmax-xmin))

    # Figure garbage collection
    plt.close()

    if sleep > 0.:
        time.sleep(sleep)

    return integral
