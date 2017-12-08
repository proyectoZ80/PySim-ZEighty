import sys
from PyQt5.QtWidgets import QDesktopWidget, QMenuBar, QItemDelegate, QLabel, QScrollArea, QGridLayout, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox, QListWidget, QBoxLayout, QLineEdit, QFileDialog, QFrame, QHeaderView, QTableWidgetSelectionRange
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from Interfaz import ventanaPrincipal
import funciones

class VentanaInicio(QWidget):
	def __init__(self,parent = None):
		super().__init__(parent)
		self.title = 'PySim ZEighty'
		self.left = 50
		self.top = 50
		self.width = 1090
		self.height = 600
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.button = QPushButton("Iniciar Simulador Z80")
		self.button1 = QPushButton()
		self.button2 = QPushButton()
		self.button3 = QPushButton()
		self.button4 = QPushButton()
		self.container =    QWidget()
		self.layout = QGridLayout()
		self.layout.setColumnStretch(0, 6)
		self.layout.setColumnStretch(2, 2)
		self.layout.setRowStretch(0,2)
		self.layout.setRowStretch(2,6)
		QPushButton("Iniciar Simulador Z80")
		self.layout.addWidget(self.button, 1,1)
		self.container.setLayout(self.layout)
		self.layoutPrincipal = QBoxLayout(0)
		self.layoutPrincipal.addWidget(self.container)
		self.setLayout(self.layoutPrincipal)
		self.button.setStyleSheet("border:2px solid #000; border-radius: px;font-size: 29px;font-weight: bold;padding:15px")
		self.button.pressed.connect(self.IniciarInterfaz)

		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		self.setMinimumWidth(1090)
		self.setMinimumHeight(600)
		self.setMaximumWidth(1090)
		self.setMaximumHeight(600)


	def IniciarInterfaz(self):
		self.hide()
		self.ex = ventanaPrincipal()
		self.ex.setStyleSheet("background-color: #fff")
		self.ex.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = VentanaInicio()
	ex.setStyleSheet(    "background-image: url(Z80.png);background-position: center center; ")
	ex.show()
	sys.exit(app.exec_())
