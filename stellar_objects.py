from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsItem
import random

stellar_obj_graphics = [
    'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\graphics\\ruined_planet.png',
    'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\graphics\\planet_red.png',
    'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\graphics\\asteroid.png',
    'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\graphics\\planet_blue.png'
]

class StellarObject(QGraphicsItem):
    def __init__(self, x, y, width, height):
        QGraphicsItem.__init__(self)
        self.icon = random.choice(stellar_obj_graphics)
        self.coords = [x, y]
        self.width = width
        self.height = height

    def boundingRect(self):
        x, y = self.coords
        return QRectF(x, y, self.width, self.height)

    def paint(self, painter, option, widget):
        x, y = self.coords
        target = QRectF(x, y, self.width, self.height)
        painter.drawImage(target, QImage(self.icon))

