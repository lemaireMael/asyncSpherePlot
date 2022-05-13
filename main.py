import random
import sys
import matplotlib
import numpy as np

# Permet d'ajouter l'argument projection='3d' dans add_subplot()
from mpl_toolkits.mplot3d import axes3d, Axes3D
matplotlib.use('Qt5agg')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QProgressBar, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import cm


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)  # super().__init__() est la méthode permettabt d'accéder au super constructeur (constructeur de la classe mère)


# * args permet de passer un tuple de longueur non définie tandis que **kwargs permet de passer un dictionnaire
# args et kwargs sont juste des convention, c'est * qui est important
# on aurait pu écrire *tuple et **dictionnaire

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.pbar = QProgressBar(self)

        #self.pbar.setGeometry(50,80,250,20)
        self.pbar.setMaximum(648)

        #self.resize(500,500)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.pbar)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)
        #self.setCentralWidget(self.canvas)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)

        max_az = 360
        max_el = 180
        angle_step = 10

        # mgrid permet d'initialiser deux matrices en vues d'une représentation en coordonnées sphériques
        # on obtien une première matrice el (élévation) et az (azimut)
        #
        #      | 0      0       0       0       0 |         | 0      1       2       3      4 |
        #      | 1      1       1       1       1 |         | 0      1       2       3      4 |
        # el = | 2      2       2       2       2 | az =    | 0      1       2       3      4 |
        #      | 3      3       3       3       3 |         | 0      1       2       3      4 |
        #      | 4      4       4       4       4 |         | 0      1       2       3      4 |
        #

        self.el, self.az = np.mgrid[0:max_el:angle_step, 0:max_az:angle_step]

        # Passage des degrés en radians
        self.el = self.el * np.pi / 180
        self.az = self.az * np.pi / 180

        # définition des coordonées catésiennes
        # Il faut initialiser une première fois (pas dans une boucle for)
        self.x = np.zeros((18, 36))
        self.y = np.zeros((18, 36))
        self.z = np.zeros((18, 36))
        self.colormapz = np.zeros((18, 36))

        # on instancie la fonction génératrice
        self.coord_gen = self.sphere_generator()
        self.test = 10
        self.update_plot()

        self.show()

        self.timer.start()

    def sphere_generator(self):
        k = 1
        for i in range(18):
            for j in range(36):
                # ici power est une valeur aléatoire (test)
                power = (random.randrange(45,55,1))*0.1

                # Calculs permettant de passer des coordonées sphériques aux coordonnées cartésiennes
                self.x[i][j] = power * np.cos(self.az[i][j]) * np.sin(self.el[i][j])
                self.y[i][j] = power * np.sin(self.az[i][j]) * np.sin(self.el[i][j])
                self.z[i][j] = power * np.cos(self.el[i][j])
                self.colormapz[i][j] = power
                self.pbar.setValue(k)
                k += 1
                yield

    def update_plot(self):

        # On vérifie que l'on ne soit pas arrivé au bout de notre fonction génétrice
        try :
            self.canvas.axes.cla()  # clear le canvas
            next(self.coord_gen)

            cm = matplotlib.cm.inferno
            sm = matplotlib.cm.ScalarMappable(cmap=cm)
            sm.set_array([])

            self.canvas.axes.plot_surface(self.x, self.y, self.z, linewidth=1, cstride=1, rstride=1, facecolors=cm(self.colormapz))
            # self.canvas.colorbar(shrink=0.5, aspect=5)
            # trigger le canvas et actualise le plot
            self.canvas.draw()

        except StopIteration:
            self.timer.stop()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()