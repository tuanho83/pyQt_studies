# dissecting states
from PyQt4 import QtCore, QtGui

try:
	import states_rc3
except ImportError:
	import states_rc2


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

	# Text edit and button.
	edit = QtGui.QTextEdit()
	edit.setText("asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
				 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
				 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
				 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy!")

	button = QtGui.QPushButton()
	buttonProxy = QtGui.QGraphicsProxyWidget()
	buttonProxy.setWidget(button)
	editProxy = QtGui.QGraphicsProxyWidget()
	editProxy.setWidget(edit)

	box = QtGui.QGroupBox()
	box.setFlat(True)
	box.setTitle("Options")

	layout2 = QtGui.QVBoxLayout()
	box.setLayout(layout2)
	layout2.addWidget(QtGui.QRadioButton("Herring"))
	layout2.addWidget(QtGui.QRadioButton("Blue Parrot"))
	layout2.addWidget(QtGui.QRadioButton("Petunias"))
	layout2.addStretch()

	boxProxy = QtGui.QGraphicsProxyWidget()
	boxProxy.setWidget(box)

	# Parent widget.
	widget = QtGui.QGraphicsWidget()
	layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical, widget)
	layout.addItem(editProxy)
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
	state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
	state1.assignProperty(box, 'geometry', QtCore.QRect(-200, 150, 200, 150))
	state1.assignProperty(boxProxy, 'opacity', 0.0)
	# State 2.
	state2.assignProperty(button, 'text', "Switch to state 3")
	state2.assignProperty(widget, 'geometry', QtCore.QRectF(200, 150, 200, 150))
	state2.assignProperty(box, 'geometry', QtCore.QRect(-200, 150, 200-190, 150))
	state2.assignProperty(boxProxy, 'opacity', 1.0)
	# State 3.
	state3.assignProperty(button, 'text', "Switch to state 1")
	state3.assignProperty(widget, 'geometry', QtCore.QRectF(138, 5, 400 - 138, 200))
	state3.assignProperty(box, 'geometry', QtCore.QRect(-200, 150, 400, 90))
	state3.assignProperty(boxProxy, 'opacity', 1.0)


	t1 = state1.addTransition(button.clicked, state2)
	animation1SubGroup = QtCore.QSequentialAnimationGroup()
	animation1SubGroup.addPause(0)
	animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))
	t1.addAnimation(animation1SubGroup)
	t1.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))


	t2 = state2.addTransition(button.clicked, state3)
	t2.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state2))
	t2.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state2))


	t3 = state3.addTransition(button.clicked, state1)
	t3.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state3))
	t3.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state3))


	machine.start()
	view = QtGui.QGraphicsView(scene)
	app.setActiveWindow(view)
	view.show()
	sys.exit(app.exec_())
