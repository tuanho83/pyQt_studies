import sys
from PyQt4 import QtGui, QtCore

#create the graphicsView which contains the graphicsScene
class GraphicsView(QtGui.QGraphicsView):
	#initialize and set dragMode and renderHints for everything inside the view
	def __init__(self, parent=None):
		super(GraphicsView, self).__init__(parent)

		#the dragMode should be changed to use the rihgt-mousebutton
		self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

		self.setRenderHint(QtGui.QPainter.Antialiasing)
		self.setRenderHint(QtGui.QPainter.TextAntialiasing)

	#crate a zoom function for the mouse-wheel
	def wheelEvent(self, event):
		factor = 1.5 ** (event.delta() / 240.0)
		self.scale(factor, factor)

#create the GraphicsScene containing the main graphics
class GraphicsScene(QtGui.QGraphicsScene):

	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
		#set the size of the scene
		self.setSceneRect(0,0,2000,2000)

		button = QtGui.QPushButton('info')
		button.setMinimumSize(QtCore.QSize(50, 30))
		button.setMaximumSize(QtCore.QSize(50, 30))
		buttonProxy = QtGui.QGraphicsProxyWidget()
		buttonProxy.setWidget(button)

		box = QtGui.QGroupBox()
		box.setStyleSheet("QGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(20%, 30%, 30%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title{background:transparent; margin-top:5px; margin-left:5px;}")
		box.setTitle("C'est la vie.")

		box_child = QtGui.QGroupBox(box)
		box_child.setTitle('Bonjourno')
		box_child.setObjectName('childGroupBox')
		box_child.setStyleSheet("QGroupBox#childGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(10%, 30%, 10%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title#childGroupBox{background:transparent; margin-top:5px; margin-left:5px;}")

		layout2 = QtGui.QVBoxLayout()
		box.setLayout(layout2)
		layout2.addStretch()

		boxProxy = QtGui.QGraphicsProxyWidget()
		boxProxy.setWidget(box)

		# Parent widget.
		widget = QtGui.QGraphicsWidget()
		layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical, widget)
		layout.addItem(buttonProxy)
		widget.setLayout(layout)


		#QGraphics Scene

		# scene = QtGui.QGraphicsScene(0, 0, 400, 300)
		# scene.setBackgroundBrush(scene.palette().window())
		# scene.addItem(widget)
		# scene.addItem(boxProxy)

		self.setBackgroundBrush(self.palette().window())
		self.addItem(widget)
		self.addItem(boxProxy)

		machine = QtCore.QStateMachine()
		state1 = QtCore.QState(machine)
		state2 = QtCore.QState(machine)
		machine.setInitialState(state1)

		# State 1.
		state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
		state1.assignProperty(box, 'geometry', QtCore.QRect(-400, 50, 350, 150))
		state1.assignProperty(box_child, 'geometry', QtCore.QRect(30, 300, 150, 100))
		state1.assignProperty(boxProxy, 'opacity',1.0)

		# State 2.
		state2.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
		state2.assignProperty(box, 'geometry', QtCore.QRect(10, 50, 350, 150))
		state2.assignProperty(box_child, 'geometry', QtCore.QRect(30, 30, 150, 100))
		state2.assignProperty(boxProxy, 'opacity', 1.0)

		t1 = state1.addTransition(button.clicked, state2)
		animation1SubGroup = QtCore.QSequentialAnimationGroup()
		animation1SubGroup.addPause(150)
		animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))

		animation1SubGroup_2 = QtCore.QSequentialAnimationGroup()
		animation1SubGroup_2.addPause(600)
		animation1SubGroup_2.addAnimation(QtCore.QPropertyAnimation(box_child, 'geometry', state1))

		t1.addAnimation(animation1SubGroup)
		t1.addAnimation(animation1SubGroup_2)
		t1.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))

		t2 = state2.addTransition(button.clicked, state1)
		animation1SubGroup_3 = QtCore.QSequentialAnimationGroup()
		animation1SubGroup_3.addPause(300)	
		animation1SubGroup_3.addAnimation(QtCore.QPropertyAnimation(box_child, 'geometry', state2))
		t2.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state2))
		t2.addAnimation(animation1SubGroup_3)
		t2.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state2))

		machine.start()
		# view = QtGui.QGraphicsView(self)
		# centerLayout = QtGui.QVBoxLayout()
		# centerLayout.addWidget(view)

#Create a new class which inherrits from "QtGui.QMainWindow"
class slider(QtGui.QMainWindow):
	def __init__(self):
		super(slider, self).__init__()
		self.initUI()

	#create the GUI
	def initUI(self):
		self.main_widget = QtGui.QWidget(self)
		hbox = QtGui.QHBoxLayout()
		self.scene = GraphicsScene()
		view = GraphicsView(self.scene)

		hbox.addWidget(view)
		hbox.addStretch(1)
		self.main_widget.setLayout(hbox)
		self.setCentralWidget(self.main_widget)
		self.setGeometry(100, 100, 700, 500)
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	window = slider()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()