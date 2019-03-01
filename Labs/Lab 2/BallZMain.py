import viz
import math
from BallZUtil import *

viz.window.setSize(1000,1000)
window = viz.MainWindow
window.ortho(-100, 100, -100 ,100, -1, 1)

viz.eyeheight(0)
#b = Block(50,[.7, 0, 0], 0, 0)
l = Launcher(45, 50)
#ball = Ball(25, 0, 0)

viz.go()