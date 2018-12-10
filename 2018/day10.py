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

for t in range(max_t):
  positions[:,:,t] = curr_pos + t*vels

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget(show=True)
win.resize(2000,600)
win.setWindowTitle('Scatter Plot')

p5 = win.addPlot(title="Scatter Plot")
p5.plot(positions[:,:,0], pen=None, symbol='s', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 250))


def mouseMoved(evt):
  pos = evt[0]  ## using signal proxy turns original arguments into a tuple
  if p5.sceneBoundingRect().contains(pos):
    x = pos.x()
    # between 1000 and 1100
    x = min(x, 2000)//5 + 10300  # 10558

    print(x)
    if 0 <= x < max_t:
      p5.clear()
      p5.plot(positions[:, :, int(x)], pen=None, symbol='s', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 250))

proxy = pg.SignalProxy(p5.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
  import sys
  if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
