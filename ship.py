from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QImage, QTransform
from PyQt5.QtWidgets import QGraphicsItem
from conversions import polar_to_cart, transformed_rect_sides

class Ship(QGraphicsItem):

    def __init__(self, location):
        QGraphicsItem.__init__(self)
        self.icon = 'graphics\\battleship.svg'
        self.coords = location
        self.speed = 0
        self.width = 50
        self.height = 50
        self.orientation = 0

    def boundingRect(self):
        x, y = self.coords
        rect_width, rect_height = transformed_rect_sides(50, self.orientation)
        x -= (rect_width - self.width)/2
        y -= (rect_height - self.height)/2
        self.coords = [x, y]
        self.width = rect_width
        self.height = rect_height
        return QRectF(x, y, rect_width, rect_height)

    def paint(self, painter, option, widget):
        x, y = self.coords
        rect_width, rect_height = transformed_rect_sides(50, self.orientation)
        target = QRectF(x, y, rect_width, rect_height)
        rotate_transform = QTransform()
        rotate_transform.rotate(self.orientation)
        painter.drawImage(target, QImage(self.icon).transformed(rotate_transform))
        painter.setPen(Qt.white)
        painter.drawRect(round(x), round(y), round(rect_width), round(rect_height))

    def moveForward(self, r):
        
        #
        # COORDINATE SYSTEM
        #         0
        #         -
        # -90  -     +  90
        #         +
        #        180
        #
        # y and x have to be received in reverse, because the coordinate system is
        # tilted 90 degrees clockwise (rsin(a) becomes length along the x-axis
        # and reverse.)
        #

        #print(self.orientation)
        y, x = polar_to_cart(r, self.orientation)
        #print(x, y)
        self.coords[0] += x
        self.coords[1] -= y
        #print(self.coords)

    def rotateShip(self, degrees):
        self.orientation += degrees
        self.orientation -= 360*(self.orientation // 360)


class CollidingParticle(QGraphicsItem):
    def __init__(self, origin, direction):
        QGraphicsItem.__init__(self)
        self.coords = origin
        self.setTransformOriginPoint(origin)
        self.setRotation(direction)
        self.direction = direction
        self.width = 3
        self.height = 10
        self.lifetime = 5
        self.remaining_life = 5

    def moveForward(self, r):
        
        #
        # COORDINATE SYSTEM
        #         0
        #         -
        # -90  -     +  90
        #         +
        #        180
        #
        # y and x have to be received in reverse, because the coordinate system is
        # tilted 90 degrees clockwise (rsin(a) becomes length along the x-axis
        # and reverse.)
        #

        #print(self.orientation)
        #y, x = polar_to_cart(r, self.direction)
        #print(x, y)
        self.coords -= QPointF(0, r)
        #print(self.coords)

        colliding = self.collidingItems()
        for item in colliding:
            if isinstance(item, Ship):
                self.scene().removeItem(item)
                self.lifetime = 0

    def boundingRect(self):
        x, y = self.coords.x(), self.coords.y()
        return QRectF(x, y, self.width, self.height)

    def paint(self, painter, option, widget):
        if self.lifetime >0:
            x, y = self.coords.x(), self.coords.y()
            painter.setPen(Qt.red)
            painter.setBrush(Qt.white)
            painter.drawRect(round(x), round(y), round(self.width), round(self.height))
            self.moveForward(50)
            self.lifetime -= 1
