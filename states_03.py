
from PyQt4 import QtCore, QtGui



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

	button = QtGui.QPushButton('info')
	button.setMinimumSize(QtCore.QSize(50, 30))
	button.setMaximumSize(QtCore.QSize(50, 30))
	buttonProxy = QtGui.QGraphicsProxyWidget()
	buttonProxy.setWidget(button)

	box = QtGui.QGroupBox()
	box.setStyleSheet("QGroupBox {background: transparent; border: 2px solid black;color: red; background-color: rgba(20%, 30%, 30%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title{background:transparent; margin-top:5px; margin-left:5px;}")
	box.setTitle("Options")

	layout2 = QtGui.QVBoxLayout()
	box.setLayout(layout2)
	# layout2.addWidget(QtGui.QRadioButton("Herring"))
	# layout2.addWidget(QtGui.QRadioButton("Blue Parrot"))
	# layout2.addWidget(QtGui.QRadioButton("Petunias"))
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
	machine.setInitialState(state1)

	# State 1.
	state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
	state1.assignProperty(box, 'geometry', QtCore.QRect(-400, 50, 350, 150))
	state1.assignProperty(boxProxy, 'opacity',1.0)

	# State 2.
	state2.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
	state2.assignProperty(box, 'geometry', QtCore.QRect(10, 50, 350, 150))
	x = state2.assignProperty(boxProxy, 'opacity', 1.0)

	t1 = state1.addTransition(button.clicked, state2)
	animation1SubGroup = QtCore.QSequentialAnimationGroup()
	animation1SubGroup.addPause(150)
	animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))
	t1.addAnimation(animation1SubGroup)
	t1.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))

	t2 = state2.addTransition(button.clicked, state1)
	t2.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state2))
	t2.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state2))

	machine.start()
	view = QtGui.QGraphicsView(scene)
	view.show()
	sys.exit(app.exec_())
