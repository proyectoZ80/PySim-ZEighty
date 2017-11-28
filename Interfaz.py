import sys
from PyQt5.QtWidgets import QItemDelegate,QLabel, QScrollArea,QGridLayout, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QListWidget, QBoxLayout,QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from Z80 import Z80 as z
import funciones

class HexDelegate(QItemDelegate):
	def createEditor(self, parent, option, index):
		w = QLineEdit(parent)
		w.setInputMask(">HH")
		return w

class App(QWidget):
	ChangedPositions = {}

	def __init__(self):
		super().__init__()
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

		button = QPushButton('Trazo', self)
		button.pressed.connect(self.prueba)

		button3 = QPushButton('Salir Paso a Paso', self)
		self.button2 = QPushButton('Paso a Paso', self)
		"""self.button2.pressed.connect(self.asignarPC)"""

		container = QWidget()
		ly = QBoxLayout(0)
		ly.addWidget(button)
		ly.addWidget(self.button2)
		container.setLayout(ly)

		win = QWidget()
		area = QScrollArea()

		self.pila = []
		vbox = QBoxLayout(3)

		for x in range(251):
			self.pila.append(QLabel())
			label = self.pila[x]
			vbox.addWidget(label)

		win.setLayout(vbox)
		area.setWidget(win)
		area.verticalScrollBar().setValue(5000)

		GRIDPRINCIPAL = QGridLayout()
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
		GRIDPRINCIPAL.setColumnStretch(0,4)
		GRIDPRINCIPAL.setColumnStretch(1,1)
		GRIDPRINCIPAL.setColumnStretch(2,4)
		GRIDPRINCIPAL.addWidget(self.tableWidget, 0, 0)
		GRIDPRINCIPAL.addWidget(codigo, 0, 2)
		GRIDPRINCIPAL.addWidget(container, 2, 0)
		GRIDPRINCIPAL.addWidget(contenedor, 3, 0)
		GRIDPRINCIPAL.addWidget(area, 0, 1)
		self.setLayout(GRIDPRINCIPAL)

		self.show()

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

	def prueba(self):
		self.llenaDiccionario()
		self.cargaMemoria("0000")
		self.desensambladoTrazo("0000", self.table)

	def llenaDiccionario(self):
		file = open('tablaCompleta.txt','r')
		self.table = {}
		for line in file.readlines():
			line = line.replace('\n','').split('|')
			self.table[line[1]] = line[0].split(':')

# Funcion para cargar el contenido del archivo en la memoria
	def cargaMemoria(self, dirCarga):
		code = open('FAC.txt', 'r')
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

	def desensambladoTrazo(self, dirEjec, table):
		inst = ""
		z.PC = dirEjec
		j = int(dirEjec,16)
		act = ''
		while(inst != 'HALT'):
			act += z.mem.obtenerContenido(funciones.tohex(j,8))
			j += 1
			if act == 'DDCB' or act == 'FDCB':
				des = line[j]
				act += 'V'+line[j+1]
				j += 2
				inst = table.get(act)[0]
				inst = inst.replace('V', des+'H')
				long = int(table.get(act)[1])
				z.PC = hex(j-4+long)[2:].zfill(4).upper()
				self.ejecutar(act, inst)
				j = int(z.PC,16)
				act = ''
			elif act in table:
				tem = act
				inst = table.get(act)[0]
				long = int(table.get(act)[1])
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

	def desensambladoPasoAPaso(self, table):
		inst = ""
		z.PC = dirEjec
		j = int(dirEjec,16)
		act = ''
		act += z.mem.obtenerContenido(funciones.tohex(j,8))
		j += 1
		if act == 'DDCB' or act == 'FDCB':
			des = line[j]
			act += 'V'+line[j+1]
			j += 2
			inst = table.get(act)[0]
			inst = inst.replace('V', des+'H')
			long = int(table.get(act)[1])
			z.PC = hex(j-4+long)[2:].zfill(4).upper()
			self.ejecutar(act, inst)
			j = int(z.PC,16)
			act = ''
		elif act in table:
			tem = act
			inst = table.get(act)[0]
			long = int(table.get(act)[1])
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
	ex = App()
	sys.exit(app.exec_())
