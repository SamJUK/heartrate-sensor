from pyqtgraph.Qt import QtGui, QtCore
from PyQt5 import QtWidgets  
import pyqtgraph as pg

import argparse
import collections
import random
import time
import math
import numpy as np

class DynamicPlotter():
    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=float)
        # PyQtGraph stuff
        self.app = QtWidgets.QApplication([])
        self.plt = pg.plot(title='Heart Rate')
        self.plt.setBackground(config.background)
        self.plt.resize(*size)
        
        self.plt.showGrid(x=config.hide_grid, y=config.hide_grid)
        
        self.plt.setLabel('left', 'HR', 'BPM')
        self.plt.setLabel('bottom', 'time', 's')

        if config.hide_axis:
            self.plt.hideAxis('bottom')
            self.plt.hideAxis('left')

        self.curve = self.plt.plot(self.x, self.y, pen=pg.mkPen((255,0,0), width=config.thickness))
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)
        # Set old data
        self.data = self.readFile()
        [self.databuffer.append(d) for d in self.data]
        print(f'Read HR Data into buffer')

    def readFile(self):
        with open(config.file, 'r') as file:
            return [l for l in file.read().splitlines()]

    def getdata(self):
        lines = self.readFile()
        newLinesCount = len(lines) - len(self.data)
        print(f'New Lines Count: {newLinesCount}')
        
        if newLinesCount < 0:
            self.data = lines
            return lines[-1]

        if len(lines) > len(self.data):
            newLines = lines[-newLinesCount:]
            self.data.extend(newLines)
            return newLines[-1]
        
        return self.databuffer[-1]

    def updateplot(self):
        self.databuffer.append( self.getdata() )
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)
        self.app.processEvents()

    def run(self):
        self.app.exec_()

def parseArguments():
    parser = argparse.ArgumentParser(description='Heart Rate Monitor')

    parser.add_argument('--interval', default=1, type=int, help='Refresh Interval (s)')
    parser.add_argument('--history', default=60, type=int, help='Historic Data to show (s)')

    parser.add_argument('--file', default='./out/hr.csv', help='File to parse HR Data from')

    parser.add_argument('--background', default='black', help='Background Colour')
    parser.add_argument('--thickness', default=1, type=int, help='Line Thickness')

    parser.add_argument('--hide_grid', action='store_false', help='Hide Grid')
    parser.add_argument('--hide_axis', action='store_true', help='Show Axis')

    parser.add_argument('--width', default=640, type=int, help='Window Width')
    parser.add_argument('--height', default=320, type=int, help='Window Height')

    return parser.parse_args()

if __name__ == '__main__':
    config = parseArguments()
    m = DynamicPlotter(sampleinterval=config.interval, timewindow=config.history, size=(config.width, config.height))
    m.run()