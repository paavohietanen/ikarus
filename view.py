from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QBasicTimer
from timeit import default_timer as timer
from ship import CollidingParticle, Ship
import random
import keyboard

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