import sys
from PyQt5.QtWidgets import  QDesktopWidget, QMenuBar,QItemDelegate,QLabel, QScrollArea,QGridLayout, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton , QMessageBox, QListWidget, QBoxLayout,QLineEdit,QFileDialog,QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from Z80 import Z80 as z
import funciones

class HexDelegate(QItemDelegate):
	def createEditor(self, parent, option, index):
		w = QLineEdit(parent)
		w.setInputMask(">HH")
		return w

class ventanaPrincipal(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.mainWidget = App(self)
		self.mainWidget.llenaDiccionario()
		self.setCentralWidget(self.mainWidget)
		self.setGeometry(0,0,1200,3000)
		self.setFixedSize(1200,600)
		menubar = QMenuBar()
		fileMenu = menubar.addMenu('Opciones')
		impMenu = QAction('Cargar Archivo',self)
		impAct = QAction('Acerca de...',self)
		fileMenu.addAction(impMenu)
		fileMenu.addAction(impAct)
		#fileMenu.triggered[impMenu].connect(abrirVentana)
		impMenu.triggered.connect(self.abrirVentana)
		self.setMenuBar(menubar)
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def abrirVentana(self):
		self.vencar2 = QMainWindow()
		self.vencar2.setWindowTitle("Direccion carga")
		buttonY  = QPushButton('Ok')
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
		self.vencar2.show()

	def obtenArchivo(self):
		self.vencar2.close()
		dircarga = self.cajaY.text()
		print(dircarga)
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _=QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()","","hex (*.HEX)",options = options)
		self.mainWidget.cargaMemoria(dircarga, files[0])
		self.mainWidget.enableExecutionDirection()


class App(QWidget):
	ChangedPositions = {}

	def __init__(self,parent):
		super(App,self).__init__(parent)
		self.title = 'PyQt5 table - pythonspot.com'
		self.left = 0
		self.top = 0
		self.width = 1200
		self.height = 3000
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.createTable()
		self.crearLista()
		self.crearListaDeRegistros()

		self.pila = []
		vbox = QBoxLayout(3)

		for x in range(251):
			self.pila.append(QLabel())
			label = self.pila[x]
			vbox.addWidget(label)
		######LINEAS PARA EL FONDO DE PILA
		fondoPILA = self.pila[0]
		fondoPILA.setText("FONDO")
		fondoPILA.setStyleSheet("QLabel { color: green}")
		#################################
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
		self.GRIDPRINCIPAL = QGridLayout()
		GRID2 = QGridLayout()
		contenedor = QWidget()

		codigo = QWidget()
		contcodigo = QBoxLayout(2)
		lbl1 = QLabel()
		lbl2 = QLabel()
		lbl3 = QLabel()
		contcodigo.addWidget(lbl1)
		contcodigo.addWidget(lbl2)
		contcodigo.addWidget(lbl3)
		codigo.setLayout(contcodigo)

		GRID2.addWidget(self.win2, 0,0)
		contenedor.setLayout(GRID2)
		self.GRIDPRINCIPAL.setColumnStretch(0,4)
		self.GRIDPRINCIPAL.setColumnStretch(1,1)
		self.GRIDPRINCIPAL.setColumnStretch(2,4)
		self.GRIDPRINCIPAL.addWidget(self.tableWidget, 0, 0)
		self.GRIDPRINCIPAL.addWidget(codigo, 0, 2)
		self.GRIDPRINCIPAL.addWidget(container, 2, 0)
		self.GRIDPRINCIPAL.addWidget(contenedor, 3, 0)
		self.GRIDPRINCIPAL.addWidget(area, 0, 1)
		#self.GRIDPRINCIPAL.addWidget(containerAdress,2,1)

		self.setLayout(self.GRIDPRINCIPAL)

	def crearListaDeRegistros(self):
		self.win2 = QWidget()

		self.registros1 = []
		vbox = QGridLayout()
		x = 0
		registros = ["B","C","D","E","H","L","A","F","SP","IX","IY","PC","IFF1","IFF2","I","R","C\'","D\'","E\'","H\'","L\'","A\'"]
		for cadena in registros:
		  self.registros1.append(QLabel())
		  label = self.registros1[x]
		  label.setText(cadena + " = " + getattr(z, cadena.replace("\'","_")))
		  x+=1

		vbox.addWidget(self.registros1[0],0,0)
		vbox.addWidget(self.registros1[1],0,1)
		vbox.addWidget(self.registros1[2],0,2)
		vbox.addWidget(self.registros1[3],0,3)
		vbox.addWidget(self.registros1[4],0,4)
		vbox.addWidget(self.registros1[5],1,0)
		vbox.addWidget(self.registros1[6],1,1)
		vbox.addWidget(self.registros1[7],1,2)
		vbox.addWidget(self.registros1[8],1,3)
		vbox.addWidget(self.registros1[9],1,4)
		vbox.addWidget(self.registros1[10],2,0)
		vbox.addWidget(self.registros1[11],2,1)
		vbox.addWidget(self.registros1[12],2,2)
		vbox.addWidget(self.registros1[13],2,3)
		vbox.addWidget(self.registros1[14],2,4)
		vbox.addWidget(self.registros1[15],3,0)
		vbox.addWidget(self.registros1[16],3,1)
		vbox.addWidget(self.registros1[17],3,2)
		vbox.addWidget(self.registros1[18],3,3)
		vbox.addWidget(self.registros1[19],3,4)
		vbox.addWidget(self.registros1[20],4,0)
		vbox.addWidget(self.registros1[21],4,1)
		self.win2.setLayout(vbox)

	def ponerPasoAPaso(self):
		self.button2.deleteLater()
		self.button2 = QPushButton('Siguiente Instrucción', self)
		self.button2.pressed.connect(self.desensambladoPasoAPaso)
		self.button3 = QPushButton('Salir paso a paso', self)
		self.button3.pressed.connect(self.salirPasoPaso)
		self.ly.addWidget(self.button2)
		self.ly.addWidget(self.button3)
		self.disableExecutionDirection()

	def salirPasoPaso(self,):
		self.button3.deleteLater()
		self.button2.deleteLater()
		self.button2 = QPushButton('Paso a paso', self)
		self.button2.pressed.connect(self.ponerPasoAPaso)
		self.ly.addWidget(self.button2)
		self.enableExecutionDirection()

	def asignarPC(self):
		val = self.textbox.text()
		if len(val) == 4:
			z.PC = val
			self.registros1[11].setText("PC = " + z.PC)

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
		self.GRIDPRINCIPAL.addWidget(self.containerAdress,2,1)
		self.textbox.textEdited.connect(self.asignarPC)

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
			horizantalLabels.append(funciones.tohex(i,8))
		for i in range(4096):
			verticalLabels.append(funciones.tohex(i*16,16))
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

			l = ["B","C","D","E","H","L","A","F","SP","IX","IY","PC","IFF1","IFF2","I","R"]
			for i in l:
				i = i + " = " + getattr(z, i)
				self.listWidget.addItem(i)

	@pyqtSlot()
	def changed(self):
		lista = [chr(i) for i in range(65,71)] + [str(i) for i in range(10)]
		if len(self.tableWidget.selectedItems())!=0:
			for currentQTableWidgetItem in self.tableWidget.selectedItems():
				key_row_int = currentQTableWidgetItem.row()
				key_colum_int = currentQTableWidgetItem.column()
				key_row = hex(currentQTableWidgetItem.row())[2:]
				key_column = hex(currentQTableWidgetItem.column())[2:]

				key = key_row + key_column
				content = currentQTableWidgetItem.text()

				App.ChangedPositions[int(key,16)] = content
				content = content.upper()
			z.mem.cambiarContenido(content, key)

	def llenaDiccionario(self):
		file = open('tablaCompleta.txt','r')
		self.table = {}
		for line in file.readlines():
			line = line.replace('\n','').split('|')
			self.table[line[1]] = line[0].split(':')

# Funcion para cargar el contenido del archivo en la memoria
	def cargaMemoria(self, dirCarga, archivo):
		code = open(archivo, 'r')
		for line in code.readlines():
			line = line.replace(':','').replace("\n", "")
			# El desensamble termina al encontrar la ultima linea del codigo objeto
			if (line != '00000001FF'):
				start = line[2:6]
				line = list(map(''.join, zip(*[iter(line)]*2)))

				# Vemos que el checksum coincida con el resultado del codigo objeto
				checksum = line[len(line)-1]
				line = line[:len(line)-1]
				sum = funciones.compDos(eval('+'.join([str(int(num,16)) for num in line])))

				line = line[4:]

				if (sum == checksum):
					i = int(dirCarga,16) + int(start,16)
					while(len(line)>0):
						localidad = funciones.tohex(i,16)
						z.mem.cambiarContenido(line[0], localidad)
						row = int(localidad[:3], 16)
						column = int(localidad[3], 16)
						item = QTableWidgetItem(line[0])
						self.tableWidget.setItem(row, column, item)
						App.ChangedPositions[int(localidad,16)] = line[0]

						line = line[1:]
						i += 1
				else:
					print ('Codigo violado', checksum, sum)
					return
			else:
				return z.mem

	def desensambladoTrazo(self):
		inst = ""
		j = int(z.PC,16)
		act = ''
		while(inst != 'HALT'):
			act += z.mem.obtenerContenido(funciones.tohex(j,8))
			j += 1
			if act == 'DDCB' or act == 'FDCB':
				des = line[j]
				act += 'V'+line[j+1]
				j += 2
				inst = self.table.get(act)[0]
				inst = inst.replace('V', des+'H')
				long = int(self.table.get(act)[1])
				z.PC = hex(j-4+long)[2:].zfill(4).upper()
				self.ejecutar(act, inst)
				j = int(z.PC,16)
				act = ''
			elif act in self.table:
				tem = act
				inst = self.table.get(act)[0]
				long = int(self.table.get(act)[1])
				longact = len(act)/2
				# Bandera para saber cuando poner la H en los numeros al desensamblar
				flagh = 0
				while(long != longact) :
					act = z.mem.obtenerContenido(funciones.tohex(j,8))
					tem += act
					longact += 1
					j += 1
					if inst.find('WW') != -1:
						inst = (act+'H').join(inst.rsplit('W',1))
						flagh = 1
					elif inst.find('V') != -1:
						inst = inst.replace('V', act+'H')
					elif inst.find('W') != -1:
						if flagh == 1: inst = inst.replace('W', act)
						else: inst = inst.replace('W', act+'H')
				z.PC = hex(j)[2:].zfill(4).upper()
				self.ejecutar(inst)
				j = int(z.PC,16)
				act = ''
				tem = ''

	def desensambladoPasoAPaso(self):
		inst = ""
		j = int(z.PC,16)
		act = ''
		act += z.mem.obtenerContenido(funciones.tohex(j,8))
		j += 1
		if act == 'DDCB' or act == 'FDCB':
			des = line[j]
			act += 'V'+line[j+1]
			j += 2
			inst = self.table.get(act)[0]
			inst = inst.replace('V', des+'H')
			long = int(self.table.get(act)[1])
			z.PC = hex(j-4+long)[2:].zfill(4).upper()
			self.ejecutar(act, inst)
			j = int(z.PC,16)
			act = ''
			print(z.PC, act, inst)
		elif act in self.table:
			tem = act
			inst = self.table.get(act)[0]
			long = int(self.table.get(act)[1])
			longact = len(act)/2
			# Bandera para saber cuando poner la H en los numeros al desensamblar
			flagh = 0
			while(long != longact) :
				act = z.mem.obtenerContenido(funciones.tohex(j,8))
				tem += act
				longact += 1
				j += 1
				if inst.find('WW') != -1:
					inst = (act+'H').join(inst.rsplit('W',1))
					flagh = 1
				elif inst.find('V') != -1:
					inst = inst.replace('V', act+'H')
				elif inst.find('W') != -1:
					if flagh == 1: inst = inst.replace('W', act)
					else: inst = inst.replace('W', act+'H')
			z.PC = hex(j)[2:].zfill(4).upper()
			print(z.PC, tem, inst)
			self.ejecutar(inst)
			j = int(z.PC,16)
			act = ''
			tem = ''
		if (inst == "HALT"):
			while(z.mem.obtenerContenido(z.PC)!= "00"):
				z.PC = funciones.tohex(int(z.PC,16) +1, 16)

	def ejecutar(self, instrucciones):
		registros = ["B","C","D","E","H","L","A","F","SP","IX","IY","PC","IFF1","IFF2","I","R","C_","D_","E_","H_","L_","A_"]
		pcAdd = ['PUSH', 'CALL', 'RST']
		pcRet = ['POP', 'RET']
		inst = instrucciones.split(" ")
		if (len(inst) == 1):
			flag = z.callMethod(z, inst[0], "")
			if inst[0] in pcAdd:
				self.addPila()
			elif inst[0] in pcRet:
				self.retPila()
			self.cambiaLocalidad(flag)
		else:
			flag = z.callMethod(z, inst[0], inst[1])
			if inst[0] in pcAdd:
				self.addPila()
			elif inst[0] in pcRet:
				self.retPila()
			self.cambiaLocalidad(flag)

		for i in range(len(self.registros1)):
			self.registros1[i].setText(registros[i].replace("_","\'") + " = "+getattr(z,registros[i]))

		return

	def addPila(self):
		indicePila = int((65534 - int(z.SP, 16))/2)
		label = self.pila[indicePila]
		label.setText(z.mem.obtenerContenido(funciones.tohex(int(z.SP,16)+1,8))+z.mem.obtenerContenido(z.SP))
		return

	def retPila(self):
		indicePila = int((65536 - int(z.SP,16))/2)
		label = self.pila[indicePila]
		label.setText("")
		return

	def cambiaLocalidad(self, flag):
		if flag!= None:
			for elem in flag.keys():
				row = int(elem[:3], 16)
				column = int(elem[3], 16)
				item = QTableWidgetItem(flag[elem])
				self.tableWidget.setItem(row, column, item)
				App.ChangedPositions[int(elem,16)] = flag[elem]
		else: return


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ventanaPrincipal()
	ex.show()
	sys.exit(app.exec_())