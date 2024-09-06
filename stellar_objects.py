from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsItem

class StellarObject(QGraphicsItem):
    def __init__(self):
        QGraphicsItem.__init__(self)
        self.icon = 'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\graphics\\ruined_planet.png'
        self.coords = [100, 80]
        self.width = 200
        self.height = 200

    def boundingRect(self):
        x, y = self.coords
        return QRectF(x, y, self.width, self.height)

    def paint(self, painter, option, widget):
        x, y = self.coords
        target = QRectF(x, y, self.width, self.height)
        painter.drawImage(target, QImage(self.icon))

