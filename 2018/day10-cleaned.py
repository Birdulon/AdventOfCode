with open('day10-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

numbers = np.array([[int(s) for s in re.findall(r'-?\d+', d)] for d in data], dtype=np.int64)
start_positions = numbers[:,:2]
velocities = numbers[:,2:]

max_t = 11000
positions = np.empty((*start_positions.shape, max_t))
for t in range(max_t):
  positions[:,:,t] = start_positions + t*velocities

heights = positions[:,1,:].max(0)-positions[:,1,:].min(0)
t = np.argmin(heights)


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget()
win.resize(2000,600)
win.setWindowTitle('Scatter Plot')
win.show()

plot = win.addPlot(title=f't={t}')
plot.plot(positions[:,:,t], pen=None, symbol='s', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 250))
plot.getViewBox().invertY(True)

if __name__ == '__main__':
  import sys
  if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
