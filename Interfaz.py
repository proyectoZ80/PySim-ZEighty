import sys
from PyQt5.QtWidgets import QDesktopWidget, QMenuBar, QItemDelegate, QLabel, QScrollArea, QGridLayout, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox, QListWidget, QBoxLayout, QLineEdit, QFileDialog, QFrame, QHeaderView, QTableWidgetSelectionRange, QHBoxLayout, QComboBox, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, Qt
from Z80 import Z80 as z
import funciones


class HexDelegate(QItemDelegate):
	def createEditor(self, parent, option, index):
		w = QLineEdit(parent)
		w.setInputMask(">HH")
		return w


class ventanaPrincipal(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.mainWidget = App(self)
		self.mainWidget.llenaDiccionario()
		self.setCentralWidget(self.mainWidget)
		self.setFixedSize(1190, 670)
		menubar = QMenuBar()
		fileMenu = menubar.addMenu('Opciones')
		impMenu = QAction('Cargar Archivo', self)
		fileMenu.addAction(impMenu)
		impMenu.triggered.connect(self.abrirVentana)
		self.setMenuBar(menubar)
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		menubar.setStyleSheet("font-size: 13px;font-weight: bold;selection-background-color:  #c2185b")
		fileMenu.setStyleSheet("font-size: 13px;font-weight: bold;")

	def abrirVentana(self):
		self.vencar2 = QMainWindow()
		self.vencar2.setWindowTitle("Direccion carga")
		buttonY = QPushButton('Ok')
		labelY = QLabel()
		labelY.setText('Direccion de Carga: ')
		self.cajaY = QLineEdit()
		widY = QWidget()
		self.cajaY.setText("0000")
		self.cajaY.alignment()
		self.cajaY.setInputMask(">HHHH")
		layY = QBoxLayout(3)
		layY.addWidget(buttonY)
		layY.addWidget(self.cajaY)
		layY.addWidget(labelY)
		widY.setLayout(layY)
		self.vencar2.setCentralWidget(widY)
		buttonY.pressed.connect(self.obtenArchivo)
		self.vencar2.setStyleSheet("background-color: #90caf9")
		labelY.setStyleSheet("font-size: 13px;font-weight: bold")
		self.cajaY.setStyleSheet("background-color: #8bc34a;padding:10px 7px;border-radius: 15px;margin: 5px;font-size: 13px;font-weight: bold")
		buttonY.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 18px;font-size: 12px;font-weight: bold;padding:10px 7px;border-radius: 15px")
		self.vencar2.show()

	def obtenArchivo(self):
		self.vencar2.close()
		dircarga = self.cajaY.text().zfill(4)
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(
			self, "QFileDialog.getOpenFileName()", "", "hex (*.HEX)", options=options)
		if len(files) != 0:
			self.mainWidget.cargaMemoria(dircarga, files[0])


class App(QWidget):
	ChangedPositions = {}

	def __init__(self, parent):
		super(App, self).__init__(parent)
		self.title = 'PySim ZEighty'
		self.left = 0
		self.top = 0
		self.width = 1200
		self.height = 3000
		self.initUI()
		self.carga = 0

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.createTable()
		self.crearLista()
		self.crearListaDeRegistros()

		self.pila = []
		self.base = []
		vbox = QBoxLayout(3)

		for x in range(11):
			self.base.append(QLabel())
			label = self.base[x]
			label.setText("xxxxxxxxxx")
			vbox.addWidget(label)
		self.base[10].setText("")
		for x in range(256):
			self.pila.append(QLabel())
			label = self.pila[x]
			vbox.addWidget(label)
		fondoPILA = self.pila[0]
		fondoPILA.setText("FONDO")

		button = QPushButton('Trazo', self)
		button.pressed.connect(self.desensambladoTrazo)

		self.button2 = QPushButton('Paso a Paso', self)
		self.button2.pressed.connect(self.ponerPasoAPaso)

		container = QWidget()
		self.ly = QBoxLayout(0)
		self.ly.addWidget(button)
		self.ly.addWidget(self.button2)
		container.setLayout(self.ly)

		win = QWidget()
		area = QScrollArea()

		win.setLayout(vbox)
		area.setWidget(win)
		area.verticalScrollBar().setValue(area.verticalScrollBar().maximum())
		area.setStyleSheet("background-color: #90caf9")
		self.GRIDPRINCIPAL = QGridLayout()
		GRID2 = QGridLayout()
		contenedor = QWidget()

		codigo = QWidget()
		contcodigo = QBoxLayout(2)
		codigo.setStyleSheet("background-color: #f48fb1")

		desFont = QFont("Times", 14, QFont.Bold)
		self.mostrarDesensamble = []

		for x in range(9):
			self.mostrarDesensamble.append(QLabel())
			self.mostrarDesensamble[x].setFont(desFont)
			contcodigo.addWidget(self.mostrarDesensamble[x])
			self.mostrarDesensamble[x].setStyleSheet("color: #000;")

		self.mostrarDesensamble[0].setText('Código Desensamblado')
		self.mostrarDesensamble[1].setText('PC		Código		Instrucción')
		self.mostrarDesensamble[8].setStyleSheet("QLabel { color: white; background-color: black; border-radius: 23px}")

		codigo.setLayout(contcodigo)
		self.mostrarDesensamble[0].setAlignment(Qt.AlignCenter)

		#boton ir a
		containerGoTO = QWidget()
		self.goTo = QLineEdit(self)
		self.goTo.setInputMask(">HHHH")
		self.goTo.setText("0000")
		addressLabel = QLabel()
		addressLabel.setText("Ir a")
		addressLabel1 = QLabel()
		addressLabel1.setText("dirección")
		addressLabel2 = QLabel()
		addressLabel2.setText("de memoria: ")
		self.box1 = QBoxLayout(2)
		self.box1.addWidget(addressLabel)
		self.box1.addWidget(addressLabel1)
		self.box1.addWidget(addressLabel2)
		self.box1.addWidget(self.goTo)
		containerGoTO.setLayout(self.box1)

		containerCleanMemory = QWidget()
		#boton desde
		self.clean1 = QLineEdit(self)
		self.clean1.setInputMask(">HHHH")
		self.clean1.setText("0000")
		cleanTextFrom = QLabel()
		cleanTextFrom.setText("Limpiar desde")
		#boton hasta
		self.clean2 = QLineEdit(self)
		self.clean2.setInputMask(">HHHH")
		self.clean2.setText("0000")
		cleanTextTo = QLabel()
		cleanTextTo.setText("hasta")
		#boton limpiar
		self.box2 = QBoxLayout(0)
		self.box2.addWidget(cleanTextFrom)
		self.box2.addWidget(self.clean1)
		self.box2.addWidget(cleanTextTo)
		self.box2.addWidget(self.clean2)
		containerCleanMemory.setLayout(self.box2)

		#buttons to clean
		containerCleanMemory1 = QWidget()
		self.cleanButton = QPushButton("Limpiar", self)
		self.cleanAll = QPushButton("Limpiar toda la memoria", self)
		self.box3 = QBoxLayout(0)
		self.box3.addWidget(self.cleanButton)
		self.box3.addWidget(self.cleanAll)
		containerCleanMemory1.setLayout(self.box3)

		self.dSpinBoxF = QDoubleSpinBox()
		self.dSpinBoxF.setMinimum(2.5)
		self.dSpinBoxF.setMaximum(9000)
		self.dSpinBoxF.setValue(3.58)
		self.dSpinBoxF.setSingleStep(0.01)

		containerEjec = QWidget()
		timeFrecWid = QWidget()
		allTime = QWidget()

		self.timeTitle = QLabel()
		self.timeSub = QLabel()
		self.instCiclos = QLabel()
		self.instTime = QLabel()
		self.totalTime = QLabel()
		self.labelZ = QLabel()
		self.labelY = QLabel()

		self.labelZ.setFixedSize(45, 48)
		self.labelY.setFixedSize(55, 48)
		self.totalTime.setFixedSize(110, 48)
		self.instTime.setFixedSize(110, 48)
		self.instCiclos.setFixedSize(30, 30)

		self.timeTitle.setText("Tiempo de Ejecución")
		self.timeSub.setText("     Frecuencia              CiclosT    Instrucción   	    Total")
		self.instCiclos.setText("    ")
		self.instTime.setText("       ")
		self.totalTime.setText("       ")
		self.labelZ.setText("[MHz]")
		self.labelY.setText("[MicroS]")

		frecTime = QHBoxLayout()
		uneTime = QVBoxLayout()
		layTime = QVBoxLayout()

		self.timeTitle.setAlignment(Qt.AlignCenter)
		self.instTime.setAlignment(Qt.AlignCenter)
		self.totalTime.setAlignment(Qt.AlignCenter)
		self.labelZ.setAlignment(Qt.AlignCenter)
		self.labelY.setAlignment(Qt.AlignCenter)
		self.instCiclos.setAlignment(Qt.AlignCenter)

		frecTime.addWidget(self.dSpinBoxF)
		frecTime.addWidget(self.labelZ)
		frecTime.addWidget(self.instCiclos)
		frecTime.addWidget(self.instTime)
		frecTime.addWidget(self.totalTime)
		frecTime.addWidget(self.labelY)
		timeFrecWid.setLayout(frecTime)
		uneTime.addWidget(self.timeTitle)
		uneTime.addWidget(self.timeSub)
		uneTime.addWidget(timeFrecWid)
		allTime.setLayout(uneTime)

		layTime.addWidget(containerCleanMemory1)
		layTime.addWidget(allTime)
		containerEjec.setLayout(layTime)

		self.containerAdress = QWidget()
		self.textbox = QLineEdit(self)
		self.textbox.setInputMask(">HHHH")
		self.textbox.setText("0000")
		addressLabel = QLabel()
		addressLabel.setText("Dir. Ejecución")
		self.box1 = QBoxLayout(2)
		self.box1.addWidget(addressLabel)
		self.box1.addWidget(self.textbox)
		self.containerAdress.setLayout(self.box1)
		self.textbox.textEdited.connect(self.asignarPC)

		memLbl = QLabel()
		memLbl.setText('Memoria')
		memLbl.setAlignment(Qt.AlignCenter)
		pilaLbl = QLabel()
		pilaLbl.setText('Stack')
		pilaLbl.setAlignment(Qt.AlignCenter)
		memLbl.setStyleSheet("font-size: 12px;font-weight: bold")
		pilaLbl.setStyleSheet("font-size: 12px;font-weight: bold")

		GRID2.addWidget(self.win2, 0, 0)
		GRID2.addWidget(self.win3, 1, 0)
		GRID2.addWidget(self.win4, 2, 0)
		contenedor.setLayout(GRID2)
		self.GRIDPRINCIPAL.setColumnStretch(0, 5)
		self.GRIDPRINCIPAL.setColumnStretch(1, 1)
		self.GRIDPRINCIPAL.setColumnStretch(2, 4)
		self.GRIDPRINCIPAL.addWidget(memLbl, 0, 0)
		self.GRIDPRINCIPAL.addWidget(pilaLbl, 0, 1)
		self.GRIDPRINCIPAL.addWidget(self.tableWidget, 1, 0)
		self.GRIDPRINCIPAL.addWidget(area, 1, 1)
		self.GRIDPRINCIPAL.addWidget(codigo, 1, 2)
		self.GRIDPRINCIPAL.addWidget(container, 2, 0)  # Botones paso a paso y trazo
		self.GRIDPRINCIPAL.addWidget(self.containerAdress, 2, 1)  # Dir Ejecucion
		self.GRIDPRINCIPAL.addWidget(containerCleanMemory, 2, 2)  # From TO
		self.GRIDPRINCIPAL.addWidget(contenedor, 3, 0)  # Registros
		self.GRIDPRINCIPAL.addWidget(containerGoTO, 3, 1)  # IR a DIR
		self.GRIDPRINCIPAL.addWidget(containerEjec, 3, 2)

		self.goTo.textEdited.connect(self.goToPosition)
		self.goTo.editingFinished.connect(self.goToPosition)
		self.cleanButton.pressed.connect(self.LimpiarMemoria)
		self.cleanAll.pressed.connect(self.LimpiarMemoriaCompleta)
		self.dSpinBoxF.valueChanged.connect(self.changeFrec)
		self.setLayout(self.GRIDPRINCIPAL)

		#Estilos
		containerGoTO.setStyleSheet("background-color: #90caf9;color: #000;border: none; border-radius: 23px;font-size: 13px;font-weight: bold")
		self.goTo.setStyleSheet("background-color: #8bc34a;padding:10px 0;border-radius: 15px;margin: 5px")
		self.tableWidget.setStyleSheet("background-color: #f48fb1;color: #000; sans-serif;font-size: 13px;font-weight: bold;gridline-color: #fff;selection-background-color:  #c2185b;border: none")
		contenedor.setStyleSheet("background-color: #90caf9;font-size: 13px;font-weight: bold;border-radius: 23px")
		button.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size:15px;font-weight: bold;padding:15px")
		self.button2.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size:15px;font-weight: bold;padding:15px")

		self.clean1.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size: 12px;font-weight: bold;padding:15px")
		self.clean2.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size: 12px;font-weight: bold;padding:15px")
		cleanTextFrom.setStyleSheet("font-size: 12px;font-weight: bold")
		cleanTextTo.setStyleSheet("font-size: 12px;font-weight: bold")
		containerCleanMemory.setStyleSheet("background-color: #90caf9;padding: 15px; border-radius: 23px")
		self.cleanButton.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 18px;font-size: 12px;font-weight: bold;padding:15px")
		self.cleanAll.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 18px;font-size: 12px;font-weight: bold;padding:15px")
		self.containerAdress.setStyleSheet("background-color: #90caf9;color: #000;border: none; border-radius: 23px;font-size: 13px;font-weight: bold")
		self.textbox.setStyleSheet("background-color: #8bc34a;padding:10px 0;border-radius: 15px;margin: 5px")
		self.dSpinBoxF.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 18px;font-size: 12px;font-weight: bold;padding:15px")

		containerEjec.setStyleSheet("background-color: #90caf9;color: #000;border: none; border-radius: 23px;font-size: 13px;font-weight: bold")
		self.labelY.setStyleSheet("background-color: #f48fb1;font-size: 12px;font-weight: bold")
		self.labelZ.setStyleSheet("background-color: #8bc34a;font-size: 12px;font-weight: bold")
		self.instTime.setStyleSheet("background-color: #f48fb1;border: none; border-radius: 23px;font-size:15px;font-weight: bold;padding:15px")
		self.totalTime.setStyleSheet("background-color: #f48fb1;border: none; border-radius: 23px;font-size:15px;font-weight: bold;padding:15px")

	def changeFrec(self):
		if z.time == 0:
			z.frec = (self.dSpinBoxF.value()) * 1000000
		else:
			pass

	def crearListaDeRegistros(self):
		self.win2 = QWidget()

		#widget para F
		vboxAll = QGridLayout()
		self.win1 = QWidget()
		self.win3 = QWidget()
		self.registerF_BIN = []
		vboxF = QBoxLayout(0)

		self.registros1 = []
		vbox = QGridLayout()
		x = 0
		registros = ["B","C","D","E","H","L","A","F","SP","IX","IY","PC","IFF1","IFF2","I","R","B\'","C\'","D\'","E\'","H\'","L\'","A\'","F\'"]
		for cadena in registros:
			self.registros1.append(QLabel())
			label = self.registros1[x]
			label.setText(cadena + " = ")
			x+=1

		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[0].setText("S")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[1].setText("Z")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[2].setText("X")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[3].setText("H")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[4].setText("X")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[5].setText("(P/V)")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[6].setText("N")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[7].setText("C")
		self.registerF_BIN.append(QLabel())
		self.registerF_BIN[8].setText('Banderas')

		regLabel = QLabel()
		regLabel.setText('Registros')
		vbox.addWidget(regLabel, 0,4)
		vbox.addWidget(self.registros1[0],1,0)
		vbox.addWidget(self.registros1[1],1,2)
		vbox.addWidget(self.registros1[2],1,4)
		vbox.addWidget(self.registros1[3],1,6)
		vbox.addWidget(self.registros1[4],1,8)
		vbox.addWidget(self.registros1[5],2,0)
		vbox.addWidget(self.registros1[6],2,2)
		vbox.addWidget(self.registros1[7],2,4)
		vbox.addWidget(self.registros1[8],2,6)
		vbox.addWidget(self.registros1[9],2,8)
		vbox.addWidget(self.registros1[10],3,0)
		vbox.addWidget(self.registros1[11],3,2)
		vbox.addWidget(self.registros1[12],3,4)
		vbox.addWidget(self.registros1[13],3,6)
		vbox.addWidget(self.registros1[14],3,8)
		vbox.addWidget(self.registros1[15],4,0)
		vbox.addWidget(self.registros1[16],4,2)
		vbox.addWidget(self.registros1[17],4,4)
		vbox.addWidget(self.registros1[18],4,6)
		vbox.addWidget(self.registros1[19],4,8)
		vbox.addWidget(self.registros1[20],5,0)
		vbox.addWidget(self.registros1[21],5,2)
		vbox.addWidget(self.registros1[22],5,4)
		vbox.addWidget(self.registros1[23],5,6)
		vboxF.addWidget(self.registerF_BIN[8])
		vboxF.addWidget(self.registerF_BIN[0])
		vboxF.addWidget(self.registerF_BIN[1])
		vboxF.addWidget(self.registerF_BIN[2])
		vboxF.addWidget(self.registerF_BIN[3])
		vboxF.addWidget(self.registerF_BIN[4])
		vboxF.addWidget(self.registerF_BIN[5])
		vboxF.addWidget(self.registerF_BIN[6])
		vboxF.addWidget(self.registerF_BIN[7])
		self.win3.setLayout(vboxF)
		self.registros1[0].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[1].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[2].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[3].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[4].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[5].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[6].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[7].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[8].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[9].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[10].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[11].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[12].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[13].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[14].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[15].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[16].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[17].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[18].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[19].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[20].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[21].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[22].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros1[23].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registerF_BIN[0].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[1].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[2].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[3].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[4].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[5].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[6].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[7].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN[8].setStyleSheet("padding: 0; font-size: 10px")
		self.crearEntradaDeRegistros(registros, vbox)
		self.win2.setLayout(vbox)


	def crearEntradaDeRegistros(self, registros, vbox):
		reg16 = ['SP', 'PC', 'IX', 'IY']
		self.registros2 = []
		x = 0
		for cadena in registros:
			self.registros2.append(QLineEdit())
			editReg = self.registros2[x]
			editReg.setText(getattr(z, cadena.replace("\'","_")))
			if cadena in reg16:
				editReg.setInputMask(">HHHH")
			elif cadena == 'IFF1' or cadena == 'IFF2':
				editReg.setInputMask("B")
			else:
				editReg.setInputMask(">HH")
			x+=1

		self.registerF_BIN1 = []
		vboxF1 = QBoxLayout(0)
		self.win4 = QWidget()
		for i in range(8):
			self.registerF_BIN1.append(QLineEdit())
			self.registerF_BIN1[i].setText("0")
			self.registerF_BIN1[i].setInputMask('B')
		self.registerF_BIN1.append(QLineEdit())
		self.registerF_BIN1[8].setText('F =')

		vbox.addWidget(self.registros2[0],1,1)
		self.registros2[0].textChanged.connect(lambda: self.editarRegistros(0, registros, reg16))
		vbox.addWidget(self.registros2[1],1,3)
		self.registros2[1].textChanged.connect(lambda: self.editarRegistros(1, registros, reg16))
		vbox.addWidget(self.registros2[2],1,5)
		self.registros2[2].textChanged.connect(lambda: self.editarRegistros(2, registros, reg16))
		vbox.addWidget(self.registros2[3],1,7)
		self.registros2[3].textChanged.connect(lambda: self.editarRegistros(3, registros, reg16))
		vbox.addWidget(self.registros2[4],1,9)
		self.registros2[4].textChanged.connect(lambda: self.editarRegistros(4, registros, reg16))
		vbox.addWidget(self.registros2[5],2,1)
		self.registros2[5].textChanged.connect(lambda: self.editarRegistros(5, registros, reg16))
		vbox.addWidget(self.registros2[6],2,3)
		self.registros2[6].textChanged.connect(lambda: self.editarRegistros(6, registros, reg16))
		vbox.addWidget(self.registros2[7],2,5)
		self.registros2[7].textChanged.connect(lambda: self.editarRegistros(7, registros, reg16))
		vbox.addWidget(self.registros2[8],2,7)
		self.registros2[8].textChanged.connect(lambda: self.editarRegistros(8, registros, reg16))
		vbox.addWidget(self.registros2[9],2,9)
		self.registros2[9].textChanged.connect(lambda: self.editarRegistros(9, registros, reg16))
		vbox.addWidget(self.registros2[10],3,1)
		self.registros2[10].textChanged.connect(lambda: self.editarRegistros(10, registros, reg16))
		vbox.addWidget(self.registros2[11],3,3)
		self.registros2[11].textChanged.connect(lambda: self.editarRegistros(11, registros, reg16))
		vbox.addWidget(self.registros2[12],3,5)
		self.registros2[12].textChanged.connect(lambda: self.editarRegistros(12, registros, reg16))
		vbox.addWidget(self.registros2[13],3,7)
		self.registros2[13].textChanged.connect(lambda: self.editarRegistros(13, registros, reg16))
		vbox.addWidget(self.registros2[14],3,9)
		self.registros2[14].textChanged.connect(lambda: self.editarRegistros(14, registros, reg16))
		vbox.addWidget(self.registros2[15],4,1)
		self.registros2[15].textChanged.connect(lambda: self.editarRegistros(15, registros, reg16))
		vbox.addWidget(self.registros2[16],4,3)
		self.registros2[16].textChanged.connect(lambda: self.editarRegistros(16, registros, reg16))
		vbox.addWidget(self.registros2[17],4,5)
		self.registros2[17].textChanged.connect(lambda: self.editarRegistros(17, registros, reg16))
		vbox.addWidget(self.registros2[18],4,7)
		self.registros2[18].textChanged.connect(lambda: self.editarRegistros(18, registros, reg16))
		vbox.addWidget(self.registros2[19],4,9)
		self.registros2[19].textChanged.connect(lambda: self.editarRegistros(19, registros, reg16))
		vbox.addWidget(self.registros2[20],5,1)
		self.registros2[20].textChanged.connect(lambda: self.editarRegistros(20, registros, reg16))
		vbox.addWidget(self.registros2[21],5,3)
		self.registros2[21].textChanged.connect(lambda: self.editarRegistros(21, registros, reg16))
		vbox.addWidget(self.registros2[22],5,5)
		self.registros2[22].textChanged.connect(lambda: self.editarRegistros(22, registros, reg16))
		vbox.addWidget(self.registros2[23],5,7)
		self.registros2[23].textChanged.connect(lambda: self.editarRegistros(23, registros, reg16))

		vboxF1.addWidget(self.registerF_BIN1[8])
		self.registerF_BIN1[0].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[0], 7))
		vboxF1.addWidget(self.registerF_BIN1[0])
		self.registerF_BIN1[1].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[1], 6))
		vboxF1.addWidget(self.registerF_BIN1[1])
		self.registerF_BIN1[2].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[2], 5))
		vboxF1.addWidget(self.registerF_BIN1[2])
		self.registerF_BIN1[3].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[3], 4))
		vboxF1.addWidget(self.registerF_BIN1[3])
		self.registerF_BIN1[4].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[4], 3))
		vboxF1.addWidget(self.registerF_BIN1[4])
		self.registerF_BIN1[5].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[5], 2))
		vboxF1.addWidget(self.registerF_BIN1[5])
		self.registerF_BIN1[6].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[6], 1))
		vboxF1.addWidget(self.registerF_BIN1[6])
		self.registerF_BIN1[7].textEdited.connect(lambda: self.editarBanderas(self.registerF_BIN1[7], 0))
		vboxF1.addWidget(self.registerF_BIN1[7])
		self.win4.setLayout(vboxF1)

		self.registros2[0].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[1].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[2].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[3].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[4].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[5].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[6].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[7].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[8].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[9].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[10].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[11].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[12].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[13].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[14].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[15].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[16].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[17].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[18].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[19].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[20].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[21].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[22].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registros2[23].setStyleSheet("padding: 5px 0; font-size: 10px")
		self.registerF_BIN1[0].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[1].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[2].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[3].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[4].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[5].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[6].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[7].setStyleSheet("padding: 0 2px; font-size: 10px")
		self.registerF_BIN1[8].setStyleSheet("padding: 0 4px; font-size: 10px")

	def editarRegistros(self, i, registros, reg16):
		if registros[i] in reg16:
			v = self.registros2[i].text().zfill(4)
		elif registros[i] == 'IFF1' or registros[i] == 'IFF2':
			v = self.registros2[i].text().zfill(1)
		else:
			v = self.registros2[i].text().zfill(2)
		if registros[i] == "F":
			register = z.hexToBin(self.registros2[i].text().zfill(2))
			self.editarBanderasHex(register)
		setattr(z, registros[i], v)

	def editarBanderas(self, registro, t):
		registerF = registro.text()
		if len(registerF) > 0:
			z.changeFlag(t,registerF)
			self.registros2[7].setText(z.F)

	def editarBanderasHex(self,register):
		self.registerF_BIN1[0].setText(register[0])
		self.registerF_BIN1[1].setText(register[1])
		self.registerF_BIN1[2].setText(register[2])
		self.registerF_BIN1[3].setText(register[3])
		self.registerF_BIN1[4].setText(register[4])
		self.registerF_BIN1[5].setText(register[5])
		self.registerF_BIN1[6].setText(register[6])
		self.registerF_BIN1[7].setText(register[7])

	def ponerPasoAPaso(self):
		z.time = 0
		self.button2.deleteLater()
		self.button2 = QPushButton('Siguiente Instrucción', self)
		self.button2.pressed.connect(self.desensambladoPasoAPaso)
		self.button3 = QPushButton('Salir paso a paso', self)
		self.button3.pressed.connect(self.salirPasoPaso)
		self.ly.addWidget(self.button2)
		self.ly.addWidget(self.button3)
		self.button2.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size: 15px;font-weight: bold;padding:15px")
		self.button3.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size: 15px;font-weight: bold;padding:15px")
		self.disableExecutionDirection()

	def salirPasoPaso(self,):
		#Linea agregadas para reiniciar el valor del tiempo
		z.time = 0
		z.PC = "0000"
		self.button3.deleteLater()
		self.button2.deleteLater()
		self.button2 = QPushButton('Paso a paso', self)
		self.button2.pressed.connect(self.ponerPasoAPaso)
		self.ly.addWidget(self.button2)
		self.enableExecutionDirection()

	def asignarPC(self):
		z.PC = self.textbox.text().zfill(4)
		self.registros1[11].setText("PC = ")
		self.registros2[11].setText(z.PC)

	def goToPosition(self):
		self.tableWidget.clearSelection()
		position = self.goTo.text()
		lenght = len(position)
		if lenght > 3:
			position_Row = position[:3]
			position_Column = position[3:]
			position_Row = int(position_Row, 16)
			position_Column = int(position_Column, 16)
			positionCell = self.tableWidget.item(position_Row, position_Column)
			self.tableWidget.scrollToItem(positionCell)
			self.tableWidget.setRangeSelected(QTableWidgetSelectionRange(positionCell.row(), positionCell.column(), positionCell.row(), positionCell.column()), True)
		elif lenght > 0:
			position_Row = position
			position_Row = int(position_Row, 16)
			position_Column = 0
			positionCell = self.tableWidget.item(position_Row, position_Column)
			self.tableWidget.scrollToItem(positionCell)
			self.tableWidget.setRangeSelected(QTableWidgetSelectionRange(positionCell.row(), positionCell.column(), positionCell.row(), positionCell.column()), True)

	def LimpiarMemoria(self):
		limpiaDic1 = {}
		inicio = self.clean1.text().zfill(4)
		fin = self.clean2.text().zfill(4)
		for i in range(int(inicio, 16), int(fin, 16) + 1):
			limpiaDic = z.mem.cambiarContenido("00", funciones.tohex(i, 16))
			limpiaDic1.update(limpiaDic)
		self.cambiaLocalidad(limpiaDic1)

	def LimpiarMemoriaCompleta(self):
		self.carga = 0
		limpiaDic1 = {}
		for i in range(int("0000", 16), int("FFFF", 16) + 1):
			limpiaDic = z.mem.cambiarContenido("00", funciones.tohex(i, 16))
			limpiaDic1.update(limpiaDic)
		self.cambiaLocalidad(limpiaDic1)

	def enableExecutionDirection(self):
		self.containerAdress = QWidget()
		self.textbox = QLineEdit(self)
		self.textbox.setInputMask(">HHHH")
		self.textbox.setText("0000")
		addressLabel = QLabel()
		addressLabel.setText("Dir. Ejecución")
		self.box1 = QBoxLayout(2)
		self.box1.addWidget(addressLabel)
		self.box1.addWidget(self.textbox)
		self.containerAdress.setLayout(self.box1)
		self.GRIDPRINCIPAL.addWidget(self.containerAdress, 2, 1)
		self.textbox.textEdited.connect(self.asignarPC)
		self.button2.setStyleSheet("background-color: #8bc34a;border: none; border-radius: 23px;font-size: 15px;font-weight: bold;padding:15px")
		self.containerAdress.setStyleSheet("background-color: #90caf9;color: #000;border: none; border-radius: 23px;font-size: 13px;font-weight: bold")
		self.textbox.setStyleSheet("background-color: #8bc34a;padding:10px 0;border-radius: 15px;margin: 5px")

	def disableExecutionDirection(self):
		self.containerAdress.deleteLater()

	def createTable(self):
	   # Create table
		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(4096)
		self.tableWidget.setColumnCount(16)
		horizantalLabels = []
		verticalLabels = []
		for i in range(16):
			horizantalLabels.append(funciones.tohex(i, 8))
		for i in range(4096):
			verticalLabels.append(funciones.tohex(i * 16, 16))
		self.tableWidget.setHorizontalHeaderLabels(horizantalLabels)
		self.tableWidget.setVerticalHeaderLabels(verticalLabels)
		# table selection change6
		for i in range(4096):
			for j in range(16):
				self.tableWidget.setItem(i, j, QTableWidgetItem("00"))
				self.tableWidget.setColumnWidth(j, 29)

		self.tableWidget.setItemDelegate(HexDelegate())
		self.tableWidget.cellChanged.connect(self.changed)

	def crearLista(self):
			self.listWidget = QListWidget()

			l = ["B", "C", "D", "E", "H", "L", "A", "F","SP", "IX", "IY", "PC", "IFF1", "IFF2", "I", "R"]
			for i in l:
				i = i + " = " + getattr(z, i)
				self.listWidget.addItem(i)

	@pyqtSlot()
	def changed(self):
		lista = [chr(i) for i in range(65, 71)] + [str(i) for i in range(10)]
		if len(self.tableWidget.selectedItems()) != 0:
			for currentQTableWidgetItem in self.tableWidget.selectedItems():
				key_row_int = currentQTableWidgetItem.row()
				key_colum_int = currentQTableWidgetItem.column()
				key_row = hex(currentQTableWidgetItem.row())[2:]
				key_column = hex(currentQTableWidgetItem.column())[2:]

				key = key_row + key_column
				content = currentQTableWidgetItem.text()

				App.ChangedPositions[int(key, 16)] = content
				content = content.upper()
			z.mem.cambiarContenido(content, key)

	def llenaDiccionario(self):
		file = open('tablaCompleta.txt', 'r')
		self.table = {}
		for line in file.readlines():
			line = line.replace('\n', '').split('|')
			self.table[line[1]] = line[0].split(':') + line[2:]

# Funcion para cargar el contenido del archivo en la memoria
	def cargaMemoria(self, dirCarga, archivo):
		try:
			code = open(archivo, 'r')
			self.carga = 1
			for line in code.readlines():
				line = line.replace(':', '').replace("\n", "")
				# El desensamble termina al encontrar la ultima linea del codigo objeto
				if (line != '00000001FF'):
					start = line[2:6]
					line = list(map(''.join, zip(*[iter(line)] * 2)))

					# Vemos que el checksum coincida con el resultado del codigo objeto
					checksum = line[len(line) - 1]
					line = line[:len(line) - 1]
					sum = funciones.compDos(eval('+'.join([str(int(num, 16)) for num in line])))

					line = line[4:]

					if (sum == checksum):
						i = int(dirCarga, 16) + int(start, 16)
						while(len(line) > 0):
							localidad = funciones.tohex(i, 16)
							z.mem.cambiarContenido(line[0], localidad)
							row = int(localidad[:3], 16)
							column = int(localidad[3], 16)
							item = QTableWidgetItem(line[0])
							self.tableWidget.setItem(row, column, item)
							App.ChangedPositions[int(localidad, 16)] = line[0]

							line = line[1:]
							i += 1
					else:
						msgBox = QMessageBox()
						msgBox.setText("Código Alterado")
						msgBox.setStandardButtons(QMessageBox.Ok)
						msgBox.exec_()
						return
				else:
					return z.mem
		except:
			msgBox = QMessageBox()
			msgBox.setText("Error al abrir archivo")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec_()
			return

	def desensambladoTrazo(self):
		z.time = 0
		inst = ""
		j = int(z.PC, 16)
		act = ''
		if self.carga != 0:
			while(inst != 'HALT'):
				act += z.mem.obtenerContenido(funciones.tohex(j, 8))
				j += 1
				if act == 'DDCB' or act == 'FDCB':
					des = z.mem.obtenerContenido(funciones.tohex(j, 8))
					act += 'V' + z.mem.obtenerContenido(funciones.tohex(j + 1), 8)
					j += 2
					inst = self.table.get(act)[0]
					inst = inst.replace('V', des + 'H')
					long = int(self.table.get(act)[1])
					tiempo = self.table.get(act)[2:]
					if len(tiempo) == 1:
						z.time += int(tiempo[0])
					z.PC = hex(j - 4 + long)[2:].zfill(4).upper()
					if int(z.PC, 16) >= int("10000", 16):
						z.PC = "0000"
					self.changeLabelLines(act, inst)
					self.changeTimeLbls(tiempo)
					res = self.ejecutar(act, inst)
					if res == False:
						return
					j = int(z.PC, 16)
					act = ''
				elif act in self.table:
					tem = act
					inst = self.table.get(act)[0]
					long = int(self.table.get(act)[1])
					tiempo = self.table.get(act)[2:]
					if len(tiempo) == 1:
						z.time += int(tiempo[0])
					longact = len(act)/2
					# Bandera para saber cuando poner la H en los numeros al desensamblar
					flagh = 0
					while(long != longact):
						act = z.mem.obtenerContenido(funciones.tohex(j, 8))
						tem += act
						longact += 1
						j += 1
						if inst.find('WW') != -1:
							inst = (act + 'H').join(inst.rsplit('W', 1))
							flagh = 1
						elif inst.find('V') != -1:
							inst = inst.replace('V', act + 'H')
						elif inst.find('W') != -1:
							if flagh == 1:
								inst = inst.replace('W', act)
							else:
								inst = inst.replace('W', act + 'H')
					z.PC = hex(j)[2:].zfill(4).upper()
					if int(z.PC, 16) >= int("10000", 16):
						z.PC = "0000"
					self.changeLabelLines(tem, inst)
					self.changeTimeLbls(tiempo)
					res = self.ejecutar(inst)
					if res == False:
						return
					j = int(z.PC, 16)
					act = ''
					tem = ''
			z.PC = "0000"
			#Lineas agregadas para reiniciar el valor del tiempo
			z.time = 0
		else:
			return

	def desensambladoPasoAPaso(self):
		inst = ""
		j = int(z.PC, 16)
		act = ''
		yes = 0
		while(yes != 1):
			act += z.mem.obtenerContenido(funciones.tohex(j, 8))
			j += 1
			if act == 'DDCB' or act == 'FDCB':
				des = line[j]
				act += 'V' + line[j + 1]
				j += 2
				inst = self.table.get(act)[0]
				inst = inst.replace('V', des + 'H')
				long = int(self.table.get(act)[1])
				tiempo = self.table.get(act)[2:]
				if len(tiempo) == 1:
					z.time += int(tiempo[0])
				z.PC = hex(j - 4 + long)[2:].zfill(4).upper()
				if int(z.PC, 16) >= int("10000", 16):
					z.PC = "0000"
				'''
				self.instTime.setText(str(tiempo[0]))
				self.totalTime.setText(str(z.time))'''
				self.changeLabelLines(act, inst)
				self.changeTimeLbls(tiempo)
				res = self.ejecutar(act, inst)
				yes = 1
				if res == False:
					self.salirPasoPaso()
				j = int(z.PC, 16)
				act = ''

			elif act in self.table:
				tem = act
				inst = self.table.get(act)[0]
				long = int(self.table.get(act)[1])
				longact = len(act) / 2
				tiempo = self.table.get(act)[2:]
				if len(tiempo) == 1:
					z.time += int(tiempo[0])
				# Bandera para saber cuando poner la H en los numeros al desensamblar
				flagh = 0
				while(long != longact):
					act = z.mem.obtenerContenido(funciones.tohex(j, 8))
					tem += act
					longact += 1
					j += 1
					if inst.find('WW') != -1:
						inst = (act + 'H').join(inst.rsplit('W', 1))
						flagh = 1
					elif inst.find('V') != -1:
						inst = inst.replace('V', act + 'H')
					elif inst.find('W') != -1:
						if flagh == 1:
							inst = inst.replace('W', act)
						else:
							inst = inst.replace('W', act + 'H')
				z.PC = hex(j)[2:].zfill(4).upper()
				#Para imprimir las instrucciones de desensamble:
				if int(z.PC, 16) >= int("10000", 16):
					z.PC = "0000"
				self.changeLabelLines(tem, inst)
				self.changeTimeLbls(tiempo)
				res = self.ejecutar(inst)
				tiempo = self.table.get(act)[2:]
				yes = 1
				if res == False:
					self.salirPasoPaso()
				j = int(z.PC, 16)
				act = ''
				tem = ''
			if (inst == "HALT"):
				z.time = 0
				msgBox = QMessageBox()
				msgBox.setText("Fin de programa")
				msgBox.setStandardButtons(QMessageBox.Ok)
				msgBox.exec_()
				self.salirPasoPaso()

	def changeTimeLbls(self, tiempo):
		frecuencia = z.frec
		periodosReloj = str(int(tiempo[0]))
		tiempoInst = ((int(tiempo[0]) / frecuencia) * 1000000)
		tiempoTotal = ((z.time / frecuencia) * 1000000)
		tiempoInst = str(round(tiempoInst, 5))
		tiempoTotal = str(round(tiempoTotal, 5))
		self.instCiclos.setText(periodosReloj)
		self.instTime.setText(tiempoInst)
		self.totalTime.setText(tiempoTotal)

	def changeLabelLines(self, act, inst):
		self.mostrarDesensamble[2].setText(self.mostrarDesensamble[3].text())
		self.mostrarDesensamble[3].setText(self.mostrarDesensamble[4].text())
		self.mostrarDesensamble[4].setText(self.mostrarDesensamble[5].text())
		self.mostrarDesensamble[5].setText(self.mostrarDesensamble[6].text())
		self.mostrarDesensamble[6].setText(self.mostrarDesensamble[7].text())
		self.mostrarDesensamble[7].setText(self.mostrarDesensamble[8].text())
		self.mostrarDesensamble[8].setText(str(z.PC) + ('		') + str(act) + ('		') + str(inst))

	def ejecutar(self, instrucciones):
		registros = ["B","C","D","E","H","L","A","F","SP","IX","IY","PC","IFF1","IFF2","I","R","B_","C_","D_","E_","H_","L_","A_","F_"]
		pcAdd = ['PUSH', 'CALL', 'RST']
		pcRet = ['POP', 'RET']
		inst = instrucciones.split(" ")
		if (len(inst) == 1):
			flag = z.callMethod(z, inst[0], "")
			if inst[0] in pcAdd:
				res = self.addPila()
				if res == False: return False
			elif inst[0] in pcRet:
				res = self.retPila()
				if res == False: return False
			self.cambiaLocalidad(flag)
		else:
			flag = z.callMethod(z, inst[0], inst[1])
			if inst[0] in pcAdd:
				res = self.addPila()
				if res == False: return False
			elif inst[0] in pcRet:
				res = self.retPila()
				if res == False: return False
			self.cambiaLocalidad(flag)
		for i in range(len(self.registros1)):
			self.registros2[i].setText(getattr(z,registros[i]))
		return

	def addPila(self):
		v = int(z.SP, 16)
		if v == 0:
			v = 65536
		indicePila = int((65534 - v)/2)
		if indicePila >= 255:
			msgBox = QMessageBox()
			msgBox.setText("Pila Llena")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec_()
			return False
		label = self.pila[indicePila]
		label.setText(z.mem.obtenerContenido(funciones.tohex(int(z.SP, 16) + 1, 8)) + z.mem.obtenerContenido(z.SP))
		return

	def retPila(self):
		v = int(z.SP, 16)
		if v == 0:
			v = 65536
		indicePila = int((65536 - v)/2)
		if indicePila < 0:
			msgBox = QMessageBox()
			msgBox.setText("Pila Vacía")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec_()
			return False
		label = self.pila[indicePila]
		label.setText("")
		return


	def cambiaLocalidad(self, flag):
		if flag != None:
			for elem in flag.keys():
				row = int(elem[:3], 16)
				column = int(elem[3], 16)
				item = QTableWidgetItem(flag[elem])
				self.tableWidget.setItem(row, column, item)
				App.ChangedPositions[int(elem, 16)] = flag[elem]
		else:
			return


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ventanaPrincipal()
	ex.setStyleSheet("background-color: #fff")
	ex.show()
	sys.exit(app.exec_())
