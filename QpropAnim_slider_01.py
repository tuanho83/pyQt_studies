
from PyQt4 import QtCore, QtGui

class animGB(QtGui.QWidget):

	def __init__(self):
		QtGui.QWidget.__init__(self)

		self._vbox = QtGui.QVBoxLayout()
		self._gbContainer = QtGui.QGroupBox()
		self._gbContainer.setMinimumSize(QtCore.QSize(370, 200))
		self._gbContainer.setMaximumSize(QtCore.QSize(370, 200))
		self._hbox = QtGui.QHBoxLayout()

		self.box = QtGui.QGroupBox()
		self.box.setMinimumSize(QtCore.QSize(350, 150))
		self.box.setMaximumSize(QtCore.QSize(350, 150))
		# self.box.setGeometry(QtCore.QRect(-400, 50, 350, 150))
		self.box.setStyleSheet("QGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(20%, 30%, 30%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title{background:transparent; margin-top:5px; margin-left:5px;}")
		self.box.setTitle("C'est la vie.")



		# Dummy buttons to prevent glitch in animation when user
		# switches hover betwene to buttons. Animation will not finish and
		# freezes.
		self.buttonx = QtGui.QPushButton(self.box)
		self.buttonx.setText('i')
 		self.buttonx.setGeometry(QtCore.QRect(325, 125, 20, 20))

		self.buttony = QtGui.QPushButton(self.box)
		self.buttony.setText('o')
 		self.buttony.setGeometry(QtCore.QRect(300, 125, 20, 20))




		self.button = Ext_Button(self.box)
		self.button.setText('i')
		self.button.setObjectName('info')
		self.button.mouseHover.connect(self.info_anim)
		self.button.setGeometry(QtCore.QRect(325, 125, 20, 20))

		self.button2 = Ext_Button(self.box)
		self.button2.setText('o')
		self.button2.setObjectName('notes')
		self.button2.mouseHover.connect(self.notes_anim)
		self.button2.setGeometry(QtCore.QRect(300, 125, 20, 20))

		self.box_child = QtGui.QGroupBox(self.box)
		self.box_child.hide()
		self.box_child.setTitle('Info Box')
		self.box_child.setObjectName('childGroupBox')
		self.box_child.setStyleSheet("QGroupBox#childGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(10%, 30%, 10%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title#childGroupBox{background:transparent; margin-top:5px; margin-left:5px;}")
		self._hbox.addWidget(self.box)

		self.box_child2 = QtGui.QGroupBox(self.box)
		self.box_child2.hide()
		self.box_child2.setTitle('Notes')
		self.box_child2.setObjectName('childGroupBox')
		self.box_child2.setStyleSheet("QGroupBox#childGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(10%, 30%, 25%, 70%); margin: 1px; padding: 5px;} QGroupBox:Title#childGroupBox{background:transparent; margin-top:5px; margin-left:5px;}")

		self._vbox.addWidget(self.box)
		self._gbContainer.setLayout(self._vbox)

		centerWidget = QtGui.QVBoxLayout(self)
		centerWidget.addWidget(self._gbContainer)


	def info_anim(self,sigbool):
		if sigbool == True:
			self.button2.hide()
			self.box_child.show()
 			animation = QtCore.QPropertyAnimation(self.box_child, "geometry")
			# animation.setEasingCurve(QtCore.QEasingCurve.OutElastic)
			animation.setDuration(250)
			animation.setStartValue(QtCore.QRect(10, 200, 250, 80))
			animation.setEndValue(QtCore.QRect(10, 50, 250, 80))
			animation.start()
			self.animation = animation
		else:
			# self.button2.show()
 			animation = QtCore.QPropertyAnimation(self.box_child, "geometry")
			# animation = QtCore.QPropertyAnimation(self.box, "geometry")
			animation.setDuration(150)
			animation.setStartValue(QtCore.QRect(10, 50, 250, 80))
			animation.setEndValue(QtCore.QRect(10, 250, 250, 80))
			animation.start()
			animation.finished.connect(self.doneOutro2)
			self.animation = animation

	def notes_anim(self,sigbool):
		if sigbool == True:
			self.button.hide()
			self.box_child2.show()
			animation = QtCore.QPropertyAnimation(self.box_child2, "geometry")
			# animation.setEasingCurve(QtCore.QEasingCurve.OutElastic)
			animation.setDuration(250)
			animation.setStartValue(QtCore.QRect(-400, 50, 250, 80))
			animation.setEndValue(QtCore.QRect(10, 50, 250, 80))
			animation.start()
			self.animation = animation
		else:
			# self.button.show()
			animation = QtCore.QPropertyAnimation(self.box_child2, "geometry")
			animation.setDuration(150)
			animation.setStartValue(QtCore.QRect(10, 50, 250, 80))
			animation.setEndValue(QtCore.QRect(-400, 50, 250, 80))
			animation.start()
			animation.finished.connect(self.doneOutro)
			self.animation = animation


	def doneOutro(self):
		self.button.show()

	def doneOutro2(self):
		self.button2.show()

class Ext_Button(QtGui.QPushButton):
	mouseHover = QtCore.pyqtSignal(bool)

	def __init__(self, parent=None):
		QtGui.QPushButton.__init__(self, parent)
		self.setMouseTracking(True)

	def enterEvent(self, event):
		self.mouseHover.emit(True)
	def leaveEvent(self, event):
		self.mouseHover.emit(False)

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	main = animGB()
	main.show()
	sys.exit(app.exec_())
