from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("SGI")

    button1 = QtWidgets.QPushButton(win)
    button1.setText("1")
    button1.setGeometry(0,0, 50, 30)

    button2 = QtWidgets.QPushButton(win)
    button2.setText("2")
    button2.setGeometry(0, 30, 50, 30)

    button3 = QtWidgets.QPushButton(win)
    button3.setText("3")
    button3.setGeometry(0, 60, 50, 30)

    button4 = QtWidgets.QPushButton(win)
    button4.setText("4")
    button4.setGeometry(0, 90, 50, 30)

    vp = QtWidgets.QAbstractScrollArea(win)
    vp.setGeometry(60, 0, 300, 300)

    label = QtWidgets.QLabel(vp)
    label.setText("teste2")
    label.move(50, 50)

    win.show()
    sys.exit(app.exec_())

window()
    
