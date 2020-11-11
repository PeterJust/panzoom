# panzoom.py
Intuitively pan and zoom a plot using drag-n-drop and the mouse-wheel in python matplotlib.

### Usage:
1) place panzoom.py in your python path (or os.chdir to the folder containing it before import) and import it.
2) Pass the figure instance while instantiating the Panzoom class. It then connects to all the necessary callback functions of the figure. *Optional argument:* base_scale = *scale* -> the factor by which the figure is zoomed each step.
3) Pan by clicking and dragging. Zoom using the mouswheel. Shift key: x-axis only zoom. Control key: y-axis only zoom. Simple as that.

### Example:
    import matplotlib.pyplot as plt
    from panzoom import Panzoom

    fig1 = plt.figure()
    plt.plot([0, 1, 3, 6, 7, 4, 2, 0])
    panzoomer = Panzoom(fig1)
    print("drag-n-drop panning and mouswheel zooming awesomeness. Now: at your fingertips!")

Python and Matlab seem to share clumsy plot interaction. The python class is a port of my original panzoom.m matlab function:
# panzoom.m
The awesome original from my graphical data segmentation software only documented in German.
To use this in Matlab, place panzoom.m in the same folder as your script (or use addpath).
Then in your script go for:

    allfigures = findall(0, 'type','figure');
    allaxes = findall(0, 'type', 'axes');
    for ii = 1:size(allfigures, 1)
        allfigures(ii).WindowButtonMotionFcn = @panzoom;
        allfigures(ii).WindowButtonUpFcn = @panzoom;
        allfigures(ii).WindowScrollWheelFcn = @panzoom;
        allfigures(ii).WindowKeyPressFcn = @panzoom;
        allfigures(ii).WindowKeyReleaseFcn = @panzoom;
    end
    for ii = 1:size(allaxes,1)
        allaxes(ii).ButtonDownFcn = @panzoom;
    end
Keys for x- and y-axis zoom are also 'ctrl' and 'shift'.
I haven't checked if panzoom.m also works in Octave and the like. Octave is still missing some figure() functionality.

*Keywords: python, matplotlib, mpl, Matlab, intuitive, interactive, agile, pan, panning, drag, dragging, drag'n'drop, zoom, zooming, mouse, mousewheel, mouse-wheel, figure, diagram, axis, axes, chart, plot*
