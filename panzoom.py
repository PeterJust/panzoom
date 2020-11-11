#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020-11-11

@author: Peter Jüstel
https://github.com/PeterJust/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import matplotlib.pyplot as plt

class Panzoom():
    '''
    Panzoom Class: Intuitively pan and zoom a plot using dragging and
                    mouse-wheel in python matplotlib.

    Usage: Pass the figure instance to the class while instantiating the class.
            It then connects to all the necessary callback functions of the
            figure (overwriting pre-existing connections!). Pan by clicking and
            dragging. Zoom using the mouswheel. Shift key: x-axis-only zoom.
            Control key: y-axis only zoom.
            Optional argument: base_scale = <scale> -> the factor by which the
            figure is zoomed at one mousewheel event.

    Example usage:
        import matplotlib.pyplot as plt
        from panzoom import Panzoom
        fig1 = plt.figure()
        plt.plot([0, 1, 3, 6, 7, 4, 2, 0])
        panzoomer = Panzoom(fig1)
        print("drag-n-drop panning and mouswheel zooming awesomeness.
                Now: at your fingertips!")

    Keywords: python, matplotlib, mpl, intuitive, interactive, agile, pan,
            panning, drag, dragging, drag'n'drop, zoom, zooming, mouse,
            mousewheel, mouse-wheel, figure, diagram, axis, axes, chart, plot
    '''
    # TODO: callbacks should probably check matplotlib.axes.Axes.can_zoom() and matplotlib.axes.Axes.can_pan()
    # TODO: check input for sanity.
    # TODO: 'ctrl' key on Apple?

    def __init__(self, fig, base_scale=1.3, **kwargs):
        #https://matplotlib.org/3.1.1/users/event_handling.html
        #https://matplotlib.org/3.2.0/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        self.fig = fig
        self.ax = None
        self.panningflag = 0
        self.xzoom = 1
        self.yzoom = 1
        self.oldxy = [0, 0]
        self.base_scale = base_scale

        self.fig.canvas.mpl_connect('button_press_event', self.buttonZemaphore)
        self.fig.canvas.mpl_connect('button_release_event', self.buttonZemaphore)
        self.fig.canvas.mpl_connect('motion_notify_event', self.pan_fun)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom_fun)
        self.fig.canvas.mpl_connect('key_press_event', self.keyZemaphore)
        self.fig.canvas.mpl_connect('key_release_event', self.keyZemaphore)
        self.fig.canvas.mpl_connect('figure_leave_event', self.reset_fun)


    def keyZemaphore(self, event):
        # changing the flags for zooming
        # https://matplotlib.org/3.2.0/api/backend_bases_api.html#matplotlib.backend_bases.KeyEvent

        # xaxis zoom
        if (event.key == 'shift') and (event.name == 'key_press_event'):
            self.yzoom = 0
        elif (event.key == 'shift') and (event.name == 'key_release_event'):
            self.yzoom = 1

        # yaxis zoom
        elif (event.key == 'control') and (event.name == 'key_press_event'):
            self.xzoom = 0
        elif (event.key == 'control') and (event.name == 'key_release_event'):
            self.xzoom = 1


    def buttonZemaphore(self, event):
        # changing the flags for panning
        if (event.name == 'button_press_event') and (event.button.numerator == 1):
            # left-mouse button press: activate pan
            self.oldxy = [event.xdata, event.ydata]
            self.panningflag = 1

        elif (event.name == 'button_release_event') and (event.button.numerator == 1):
            # left-mouse button release: deactivate pan
            self.panningflag = 0


    def pan_fun(self, event):
        # drag-panning the axis
        # This function has to be efficient, as it is polled often.
        if (self.panningflag == 1) and (event.inaxes != None):
            # do pan
            self.ax = event.inaxes # set the axis to work on

            x, y = event.xdata, event.ydata
            self.ax.set_xlim(self.ax.get_xlim() + self.oldxy[0] - x) # set new axes limits
            self.ax.set_ylim(self.ax.get_ylim() + self.oldxy[1] - y)

            self.ax.figure.canvas.draw() # force re-draw


    def zoom_fun(self, event):
        #zooming the axis
        if event.inaxes != None:
            # zooming makes only sense, when pointing at an axis
            self.ax = event.inaxes # set the axis to work on

            # get the current x and y limits
            cur_xlim = self.ax.get_xlim() # tuple: (low, high)
            cur_ylim = self.ax.get_ylim()
            # set the range
            x = event.xdata # get event x location
            y = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1/self.base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = self.base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print("Zoom: Button sends strange signal: " + event.button)
            # set new limits
            if self.xzoom == 1:
                # if 'control' is NOT pressed, zoom the x-axis
                lower = cur_xlim[0] * scale_factor + (1-scale_factor) * x
                upper = cur_xlim[1] * scale_factor + (1-scale_factor) * x
                self.ax.set_xlim([lower, upper])
                #self.ax.set_xlim(np.array(cur_xlim) * scale_factor + (1-scale_factor) * x) # ->more elegant, but uses numpy
            if self.yzoom == 1:
                # if 'shift' is NOT pressed, zoom the y-axis
                lower = cur_ylim[0] * scale_factor + (1-scale_factor) * y
                upper = cur_ylim[1] * scale_factor + (1-scale_factor) * y
                self.ax.set_ylim([lower, upper])

            self.ax.figure.canvas.draw() # force re-draw


    def reset_fun(self, event):
        # reset all flags
        self.ax = None
        self.panningflag = 0
        self.xzoom = 1
        self.yzoom = 1
        self.oldxy = [0, 0]