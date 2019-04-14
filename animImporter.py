from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm

class animUI(QtWidgets.QDialog):

	def __init__(self):
		super(animUI, self).__init__()
		self.buildUI()

	def deleteKeys(self):
		sel = pm.ls(selection = True)

		obj = pm.listRelatives(sel[0],allDescendents = True)

		shapes = []

		for a in obj:
			if a.type() == 'nurbsCurve':
				shapes.append(a)

		connection = []
		for item in shapes:
			connection.append(pm.listConnections(pm.listRelatives(item, parent = True), connections = True))

		types = ['animCurveTA', 'animCurveTT', 'animCurveTL', 'animCurveTU']

		pm.select(clear = True)
		for items in connection:
			for asset in items:
				print(asset[-1])
				if asset[-1].type() in types:
					pm.select(asset[-1], add = True)

		pm.delete()

	def importFunc(self):
		self.deleteKeys()
		self.fileName = self.displayArea.text()
		# print(self.fileName)
		if self.fileName == '':
			print("Please enter a file to be imported")
		else:
			pm.importFile(self.fileName, usingNamespaces = False, force = True)

			types = ['animCurveTA', 'animCurveTT', 'animCurveTL', 'animCurveTU']

			objList = []
			objs = pm.ls()

			for obj in objs:
				if obj.type() in types:
					objList.append(obj)

			source = []
			destination = []

			for obj in objList:
				# source.append("{0}_{1}.output".format(fileName,obj.name()))
				source.append("{0}.output".format(obj.name()))
			for obj in objList:
				a,b = obj.name().rsplit('_',1)
				destination.append("{0}.{1}".format(a,b))

			for i in range(len(destination)):
				if not pm.ls(source[i]):
					pass
				else:
					pm.connectAttr(source[i], destination[i])

	def quitter(self):
		self.close()

	def buildUI(self):
		print('building')
		self.setWindowTitle('Anim Export - Import')

		self.layout = QtWidgets.QGridLayout(self)

		self.pathLabel = QtWidgets.QLabel('Path')
		self.layout.addWidget(self.pathLabel, 1,0,1,1)
		self.displayArea = QtWidgets.QLineEdit()
		self.layout.addWidget(self.displayArea, 1,1,1,4)
		self.importBtn = QtWidgets.QPushButton("Import")
		self.layout.addWidget(self.importBtn, 2,1,1,1)
		self.importBtn.clicked.connect(self.importFunc)
		self.cancelBtn = QtWidgets.QPushButton('Cancel')
		self.cancelBtn.clicked.connect(self.quitter)
		self.layout.addWidget(self.cancelBtn, 2,2,1,1)



anim = animUI()
anim.show()
