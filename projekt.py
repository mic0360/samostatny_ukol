import sys, time
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtCore import QSize, Qt, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class Ellipse():
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Animation(QThread):
    duration = 10
    speed = 1
    statusChanged = pyqtSignal(object)

    def __init__(self, duration, speed):
        super(Animation, self).__init__()
        self.duration = duration
        if speed > 1:
          self.speed = speed

    def set_speed(self, speed):
        self.speed = speed

    def run(self):
        for i in range(self.duration):
            circle = Ellipse(30 + i, 30 + i, 200, 200)
            self.statusChanged.emit(circle)
            time.sleep(float(1)/float(self.speed))

        for i in range(self.duration):
            circle = Ellipse(530 + i, 500 - i, 200, 200)
            self.statusChanged.emit(circle)
            time.sleep(float(1)/float(self.speed))

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1000, 700))

        buttonCircle = QPushButton('Vezmi míč', self)
        buttonCircle.clicked.connect(self.draw_circle)
        buttonCircle.resize(100, 50)
        buttonCircle.move(10, 10)
        self.circle = None

        buttonAnimation = QPushButton('Zahoď míč', self)
        buttonAnimation.clicked.connect(self.draw_animation)
        buttonAnimation.resize(100, 50)
        buttonAnimation.move(10, 70)

    def draw_circle(self):
        self.circle = Ellipse(30, 30, 200, 200)
        self.update()

    def draw_animation(self):
        self.animation = Animation(500, 3000)
        self.animation.statusChanged.connect(self.onStatusChanged)
        self.animation.start()

    def onStatusChanged(self, value):
        self.circle = value
        self.update()

    def paintEvent(self, event):
        QMainWindow.paintEvent(self, event)
        painter = QPainter(self)

        if not self.circle is None:
            painter.setPen(QPen(Qt.red, 10))
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            painter.drawEllipse(self.circle.x, self.circle.y, self.circle.width, self.circle.height)

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())