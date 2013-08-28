from PyQt4 import QtGui,QtCore

class slider(QtGui.QWidget):
	def __init__(self,parent=None):
		super(slider, self).__init__(parent)
		
		# Text edit and button.
		button = QtGui.QPushButton()
		buttonProxy = QtGui.QGraphicsProxyWidget()
		buttonProxy.setWidget(button)

		box = QtGui.QGroupBox()
		box.setStyleSheet("QGroupBox {border: none; background-color: rgba(10%, 10%, 10%, 50%);}")
		box.setFlat(True)
		box.setTitle("Options")

		layout2 = QtGui.QVBoxLayout(self)
		box.setLayout(layout2)
		layout2.addWidget(QtGui.QLabel("AppleBee's"))
		layout2.addWidget(QtGui.QRadioButton("Herring"))
		layout2.addWidget(QtGui.QRadioButton("Blue Parrot"))
		layout2.addWidget(QtGui.QRadioButton("Petunias"))
		layout2.addStretch()

		boxProxy = QtGui.QGraphicsProxyWidget()
		boxProxy.setWidget(box)

		# Parent widget.
		widget = QtGui.QGraphicsWidget()
		layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical, widget)
		layout.addItem(buttonProxy)
		widget.setLayout(layout)

		scene = QtGui.QGraphicsScene(0, 0, 400, 300)
		scene.setBackgroundBrush(scene.palette().window())
		scene.addItem(widget)
		scene.addItem(boxProxy)

		machine = QtCore.QStateMachine()
		state1 = QtCore.QState(machine)
		state2 = QtCore.QState(machine)
		state3 = QtCore.QState(machine)
		machine.setInitialState(state1)

		# State 1.
		state1.assignProperty(button, 'text', "Switch to state 2")
		state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 250, 400, 150))
		state1.assignProperty(box, 'geometry', QtCore.QRect(0, 0, 250, 250))
		# state1.assignProperty(boxProxy, 'opacity', 0.0)

		# State 2.
		state2.assignProperty(button, 'text', "Switch to state 3")
		state2.assignProperty(widget, 'geometry', QtCore.QRectF(0, 250, 400, 150))
		state2.assignProperty(box, 'geometry', QtCore.QRect(0, 0, 250-450, 250))
		# state2.assignProperty(boxProxy, 'opacity', 1.0)

		# State 3.
		state3.assignProperty(button, 'text', "Switch to state 1")
		state3.assignProperty(widget, 'geometry', QtCore.QRectF(0, 250, 400, 150))
		state3.assignProperty(box, 'geometry', QtCore.QRect(0, 0, 450-250, 250))
		# state3.assignProperty(boxProxy, 'opacity', 1.0)


		t1 = state1.addTransition(button.clicked, state2)
		animation1SubGroup = QtCore.QSequentialAnimationGroup()
		animation1SubGroup.addPause(0)
		animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))
		t1.addAnimation(animation1SubGroup)
		t1.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))


		t2 = state2.addTransition(button.clicked, state3)
		t2.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state3))
		t2.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state3))

		t3 = state3.addTransition(button.clicked, state1)
		t3.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))
		t3.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))


		machine.start()
		QtGui.QGraphicsView(scene)
		self.centerOnScreen()

	def centerOnScreen (self):
			'''centerOnScreen()
	Centers the window on the screen.'''
			#resolution = QtGui.QDesktopWidget().screenGeometry()
			resolution = QtGui.QDesktopWidget().availableGeometry()
			self.frameGeometry()
			#self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
					  #(resolution.height() / 2) - (self.frameSize().height() / 2))



class Pixmap(QtGui.QGraphicsObject):
	def __init__(self, pix):
		super(Pixmap, self).__init__()

		self.p = QtGui.QPixmap(pix)

	def paint(self, painter, option, widget):
		painter.drawPixmap(QtCore.QPointF(), self.p)

	def boundingRect(self):
		return QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(self.p.size()))

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	app.setStyle("Plastique")
	mainWin = slider()
	mainWin.show()
	sys.exit(app.exec_())
