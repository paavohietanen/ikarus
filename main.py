import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from stellar_objects import StellarObject
from timeit import default_timer as timer
from view import GameView
    
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

        self.enemy_ship = self.view.newEnemy()
        self.view.scene.addItem(self.enemy_ship)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    sys.exit(app.exec_())