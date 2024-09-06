import keyboard
import sys
import random
from conversions import polar_to_cart, transformed_rect_sides
from PyQt5.QtCore import QBasicTimer, Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGraphicsView, QMainWindow, QGraphicsItem, QGraphicsScene

from PyQt5.QtGui import QImage, QTransform
from timeit import default_timer as timer
    
class GameWindow(QMainWindow):
    AreaWidth = 50
    AreaHeight = 50

    def __init__(self):
        QMainWindow.__init__(self)
        self.screenSize = QDesktopWidget().availableGeometry()
        self.initUI()
        self.view = GameView()
        self.generated = False
        self.setCentralWidget(self.view)
        self.initShip()        
        self.show()

    def initUI(self):
        self.setStyleSheet('background-color: black;')
        self.left = self.screenSize.width() * 1
        self.top = self.screenSize.height() * 1
        self.width = self.screenSize.width() * 1
        self.height = self.screenSize.height() * 1
        self.setGeometry(self.left, self.top, self.width, self.height)

    def initShip(self):
        self.ship = self.view.newShip()
        self.view.scene.addItem(self.ship)
        self.view.scene.addItem(Planet())

        self.enemy_ship = self.view.newEnemy()
        self.view.scene.addItem(self.enemy_ship)

class GameScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.generated = False
        self.stars = []
        self.initStars()

    def initStars(self):
        for _ in range(0, 10000):
            x = random.randint(0, 2000)
            y = random.randint(0, 2000)
            self.stars.append((x,y))

    def drawBackground(self, painter, rect):
        painter.setPen(Qt.white)
        for coord in self.stars:
            x, y = coord
            painter.drawPoint(x, y)

    

class GameView(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.scene = GameScene()
        self.setScene(self.scene)
        self.setSceneRect(0,0,2000, 2000)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.timer = QBasicTimer()
        self.timer.start(1, self)
        self.event_timestamp = None
        self.generated = False
    
    def newShip(self):
        self.ship = Ship([1000, 1000])
        return self.ship

    def newEnemy(self):
        self.enemy_ship = Ship([700, 700])
        return self.enemy_ship
        
    def moveShip(self):
        self.ship.moveForward(2)

    def firingSequence(self):
        particle = CollidingParticle(self.ship.boundingRect().center(), self.ship.orientation)
        self.scene.addItem(particle)

    def timerEvent(self, event):
        # timer event includes continuous rendering of graphics as well as
        # key events, because PyQt5 native keyPress/ReleaseEvents suck
        self.centerOn(self.ship)
        if self.event_timestamp:
            if timer() - self.event_timestamp >= 0.5:
                print("HIT")
                self.event_timestamp = None

        if event.timerId() == self.timer.timerId():
            if keyboard.is_pressed('up'):
                self.moveShip()
            if keyboard.is_pressed('right'):
                self.ship.rotateShip(1)
            elif keyboard.is_pressed('left'):
                self.ship.rotateShip(-1)
            if keyboard.is_pressed('space') and self.event_timestamp == None:
                self.firingSequence()
                self.event_timestamp = timer()
            self.update()

class Ship(QGraphicsItem):

    def __init__(self, location):
        QGraphicsItem.__init__(self)
        self.icon = 'battleship.svg'
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


class Planet(QGraphicsItem):
    def __init__(self):
        QGraphicsItem.__init__(self)
        self.icon = 'C:\\Users\\35840\\Documents\\Personal\\Personal code\\ikarus\\11011135.png'
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
            target = QRectF(x, y, self.width, self.height)
            painter.setPen(Qt.red)
            painter.setBrush(Qt.white)
            painter.drawRect(round(x), round(y), round(self.width), round(self.height))
            self.moveForward(50)
            self.lifetime -= 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    sys.exit(app.exec_())