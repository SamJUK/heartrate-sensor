from pyqtgraph.Qt import QtGui, QtCore
from PyQt5 import QtWidgets  
import pyqtgraph as pg

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
        # self.plt.setBackground((0, 255, 0))
        self.plt.resize(*size)
        self.plt.showGrid(x=False, y=False)
        # self.plt.setLabel('left', 'HR', 'BPM')
        # self.plt.setLabel('bottom', 'time', 's')
        self.plt.hideAxis('bottom')
        self.plt.hideAxis('left')
        self.curve = self.plt.plot(self.x, self.y, pen=pg.mkPen((255,0,0), width=5))
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)
        # Set old data
        self.data = self.readFile()
        [self.databuffer.append(d) for d in self.data]
        print(f'Read HR Data into buffer')

    def readFile(self):
        with open('./out/hr.csv', 'r') as file:
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

if __name__ == '__main__':
    m = DynamicPlotter(sampleinterval=1, timewindow=60*1, size=(640,120))
    m.run()