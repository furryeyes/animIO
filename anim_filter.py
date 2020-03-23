"""A UI to smooth animation curves along the selected channels in maya

Usage : Run the script, you will get the UI.
		The UI provides us with two options, low pass and high pass.

        Select the channel(s) along which to smooth the curve,
		make sure to select atleast 3 contol vertices or the script will not work,
		as we are not touching the first and the last frame while smoothening, then click on
        the option of low/high pass after selecting the iterations.

		run show_widget() 

Author : vivek-v
"""

import pymel.core as _pm
import maya.OpenMayaUI as _omui

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

class AnimFilter(QtWidgets.QDialog):
	"""Class to create a dialog for Anim Curve Filter
	"""
	def __init__(self, parent=None):
		"""Init function for the UI
		"""
		super(AnimFilter, self).__init__(parent=parent)
		self.build_ui()
		
	def build_ui(self):
		"""Builds the UI for Anim Curve Filter
		"""
		
		self.layout = QtWidgets.QGridLayout(self)
		
		self.setWindowTitle("Anim Curve Filter")
		
		self.freq_label = QtWidgets.QLabel("Set number of itertions :")
		# Adding extra space for spacing in the UI.
		self.freq_label.setFixedHeight(40)
		self.layout.addWidget(self.freq_label, 0,1,1,1)
		self.freq_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.freq_slider.setFixedHeight(20)
		self.freq_slider.setMinimum(1)
		self.freq_slider.setMaximum(10)
		# Setting the spin box value as we change the slider
		self.freq_slider.valueChanged.connect(self._slider_value_change)
		self.layout.addWidget(self.freq_slider, 1,1,1,6)
		
		self.slider_sp = QtWidgets.QSpinBox()
		self.slider_sp.setMinimum(1)
		self.slider_sp.setMaximum(10)
		self.slider_sp.setFixedWidth(70)
		# Setting the slider value as we change the spin box value
		self.slider_sp.valueChanged.connect(self._sp_value_change)
		self.layout.addWidget(self.slider_sp, 1,7,1,1)
		
		# Adding a separater
		self.splitter = QtWidgets.QFrame()
		self.splitter.setFrameShape(QtWidgets.QFrame.HLine)
		self.splitter.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.splitter.setFixedHeight(20)
		self.layout.addWidget(self.splitter, 2,0,1,10)
		
		# Creating a new layout for the buttons
		self.button_layout = QtWidgets.QGridLayout()
		self.low_button = QtWidgets.QPushButton("Low Pass")
		self.low_button.setFixedWidth(150)
		self.low_button.clicked.connect(self.low_pass)
		self.button_layout.addWidget(self.low_button, 0,1,1,1)
		
		self.high_button = QtWidgets.QPushButton("High Pass")
		self.high_button.setFixedWidth(150)
		self.high_button.clicked.connect(self.high_pass)
		self.button_layout.addWidget(self.high_button, 0,2,1,1)
		
		# Adding button layout to main layout
		self.layout.addLayout(self.button_layout, 3,1,1,8)
		
	def _slider_value_change(self):
		"""Function to set the value of slider_sp, spin box if the slider is moved.
		"""
		freq_value = self.freq_slider.value()
		self.slider_sp.setValue(freq_value)
		
	def _sp_value_change(self):
		"""Function to set the value of freq_slider, slider if the spin box is updated.
		"""
		freq_value = self.slider_sp.value()
		self.freq_slider.setValue(freq_value)
		
	def low_pass(self):
		"""Function for low pass button click.
		"""
		freq_value = self.slider_sp.value()
		self._iterator_smooth(freq_value, 0)

	def high_pass(self):
		"""Function for high pass button click.
		"""
		freq_value = self.slider_sp.value()
		self._iterator_smooth(freq_value, 1)
		
	def _iterator_smooth(self, iterations, pass_value):
		"""Function to create an undo chunk and iteratively smooth the graph keys.
		The undo chunk is used to return back to the original state in one undo command.
		"""
		# Creating an undo chunk start point
		_pm.undoInfo(openChunk=True)
		# Iteratively calling the smooth keys functionality
		for iterator in xrange(iterations):
			self.smooth_keys(pass_value)
		# Creating an undo chunk end point
		_pm.undoInfo(closeChunk=True)

	def smooth_keys(self, pass_value):
		""" Function to smooth the animation curve control vertices.
		"""
		# Get the selected curves
		curves = _pm.keyframe(query = True, name = True)

		if len(curves) == 0:
			raise ValueError("Select at least 3 keys in the Graph Editor.")
		else:
			for curve in curves:
				keys = _pm.keyframe(curve, query = True, selected = True) # Frame Numbers
				sizeOfKeys = len(keys)

				# The first and last keys will not be changed, so atleast three should be selected
				if not sizeOfKeys < 3:
					# Duplicate the curve(s) to store the values
					dupCurve = _pm.duplicate(curve)

					# Starting the range with second frame
					for i in range(1, (sizeOfKeys-1)):
						prevVal = _pm.keyframe(curve, vc = True ,time = (keys[i-1], keys[i-1]), query = True)
						currVal = _pm.keyframe(curve, vc = True ,time = (keys[i], keys[i]), query = True)
						nextVal = _pm.keyframe(curve, vc = True ,time = (keys[i+1], keys[i+1]), query = True)

						# calculating Average of the frame value
						if pass_value == 0:
							average = (prevVal[0] + currVal[0]*4 + nextVal[0])/6
						if pass_value == 1:
							average = (prevVal[0] + currVal[0] + nextVal[0])/3
						

						# storing the values in the duplicate curve
						_pm.keyframe(dupCurve[0], vc = average ,time = (keys[i], keys[i]), absolute = True)

					# applying the values
					for i in range(1, (sizeOfKeys-1)):
						dupCurveVal = _pm.keyframe(dupCurve[0], vc = True ,time = (keys[i], keys[i]), query = True)
						_pm.keyframe(curve, vc = dupCurveVal[0] ,time = (keys[i], keys[i]), absolute = True)

					# deleting the duplicate curve(s) created
					_pm.delete(dupCurve[0])

				else:
					raise ValueError("Select at least 3 keys in the Graph Editor.")
		
def get_maya_main_window():
	"""Function to get the maya's main window.
	
	Returns:
		QtWidgets.QMainWindow: The Maya MainWindow.
	"""
	# Using the OpenMayaUI API to get a reference to Maya's MainWindow
	win = _omui.MQtUtil_mainWindow()
	ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
	return ptr

def show_widget():
	"""Function to get the maya main window, add it as the parent of the dialog, then show the dialog as maya window.
	"""
	parent = get_maya_main_window()
	anim_filter = AnimFilter(parent)
	anim_filter.show()

show_widget()
