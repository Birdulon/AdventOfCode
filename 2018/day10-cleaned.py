with open('day10-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np

positions = []
velocities = []

for line in data:
  pos = [int(line[10:16]), -int(line[18:24])]  # Invert Y for graphing purposes
  vel = [int(line[36:38]), -int(line[39:42])]  # Invert Y for graphing purposes
  positions.append(pos)
  velocities.append(vel)

max_t = 11000
curr_pos = np.vstack(positions)
vels = np.vstack(velocities)
positions = np.empty((385,2,max_t))
heights = np.empty(max_t, dtype=np.int64)

for t in range(max_t):
  positions[:,:,t] = curr_pos + t*vels
  heights[t] = positions[:,1,t].max() - positions[:,1,t].min()
t = np.argmin(heights)

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget()
win.resize(2000,600)
win.setWindowTitle('Scatter Plot')
win.show()

p5 = win.addPlot(title=f't={t}')
p5.plot(positions[:,:,t], pen=None, symbol='s', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 250))

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
  import sys
  if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
