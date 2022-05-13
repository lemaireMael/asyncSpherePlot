import random
import sys
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

matplotlib.use('Qt5agg')

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection="3d")
        super().__init__(fig)  #


# * args permet de passer un tuple de longueur non définie tandis que **kwargs permet de passer un dictionnaire
# args et kwargs sont juste des convention, c'est * qui est important
# on aurait pu écrire *tuple et **dictionnaire

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        power = 1

        max_az = 360
        max_el = 180
        angle_step = 10

        self.el, self.az = np.mgrid[0:max_el:angle_step, 0:max_az:angle_step]

        self.el = self.el * np.pi / 180
        self.az = self.az * np.pi / 180

        x = np.cos(self.az) * np.sin(self.el)
        y = np.sin(self.az) * np.sin(self.el)
        z = np.cos(self.el)

        sc.axes.plot_wireframe(x, y, z, linewidth=1)
        self.setCentralWidget(sc)

        # self.update_plot()

        self.show()

        """fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_wireframe(x, y, z, linewidth=1, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()"""
        """self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()"""

    def update_plot(self):
        # on laisse la première valeur du tableau afin de garder une fenetre de taille 50
        # on append une nouvelle valeur aléatoire
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # clear le canvas
        self.canvas.axes.plot(self.xdata, self.ydata, 'b')
        # trigger le canvas et actualise le plot
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()