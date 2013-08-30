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

	def animate(self):

		self.animations = range(3)

		#move item to position(x,y) at time t
		def animate_to(item,x,y,t):

			animation = QtGui.QGraphicsItemAnimation()
			#create a timeline of 1 second
			timeline = QtCore.QTimeLine(2000)
			#number of steps in timeline (100)
			timeline.setFrameRange(0,100)
			#set position at time t
			animation.setPosAt(t, QtCore.QPointF(x,y))
			#apply this to "item"
			animation.setItem(item)
			#add timeline to the animation
			animation.setTimeLine(timeline)

			
			#output of this definition is "animation"
			return animation

		self.animations[0] = animate_to(self.geos[0],200,200,0.2)
		self.animations[1] = animate_to(self.geos[1],200,200,0.2)
		self.animations[2] = animate_to(self.geos[2],200,200,0.2)

		#animation.timeline().start()
		self.animator.start(2000)
		[ animation.timeLine().start() for animation in self.animations ] 

	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
		#set the size of the scene
		self.setSceneRect(0,0,2000,2000)

		#self.addRect(QtCore.QRectF(800,800,200,200))

		#---create the scene-geometries ---   

		#empty list to hold the geometries
		self.geos = []

		#create stuff to add to the scene
		geo_01 = QtGui.QGraphicsEllipseItem(800,800,200,200)
		geo_02 = QtGui.QGraphicsEllipseItem(850,850,300,300)
		geo_03 = QtGui.QGraphicsEllipseItem(900,900,400,400)
		#add stuff to the scene
		self.addItem(geo_01)
		self.addItem(geo_02)
		self.addItem(geo_03)

		#put stuff into list so it can be referenced
		self.geos.append(geo_01)
		self.geos.append(geo_02)
		self.geos.append(geo_03)

		#----do the animation thing---
		self.animator = QtCore.QTimer()

		self.animator.timeout.connect(self.animate)

		self.animate()


#Create a new class which inherrits from "QtGui.QMainWindow"
class Example(QtGui.QMainWindow):

	def __init__(self):
		#The "super()"-method returns the parrent object of the example-class
		#and it's constructor is called ("__init__")
		super(Example, self).__init__()

		self.initUI()

	#create the GUI
	def initUI(self):

		"""---create the buttons---"""

		#set a font for the tool-tips
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

		#create a button and a tool-tip for the button
		btn_01 = QtGui.QPushButton('Button', self)
		btn_01.setToolTip('This is a <b>QPushButton</b> widget')
		#resize the button with a recommended size (.sizeHint())
		btn_01.resize(btn_01.sizeHint())

		#create a button and a tool-tip for the button
		btn_02 = QtGui.QPushButton('Button', self)
		btn_02.setToolTip('This is a <b>QPushButton</b> widget')
		#resize the button with a recommended size (.sizeHint())
		btn_02.resize(btn_02.sizeHint())

		"""----create a layout----"""

		#create the main widget, which holds the layout
		self.main_widget = QtGui.QWidget(self)

		#create a vertical box layout to hold the buttons on the right
		vbox = QtGui.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addWidget(btn_01)
		vbox.addWidget(btn_02)  

		#create horizontal box layout to hold the vbox and the main area
		hbox = QtGui.QHBoxLayout()

		#store the GraphicsScene in a variable so it is not destroyed
		self.scene = GraphicsScene()
		#add the scene to the GraphicsView
		view = GraphicsView(self.scene)

		hbox.addWidget(view)
		hbox.addStretch(1)
		hbox.addLayout(vbox)

		self.main_widget.setLayout(hbox)
		self.setCentralWidget(self.main_widget)

		#set the possition and size of the window, then set the window title
		#these methods have been inherited by the "QtGui.QWidget"-class
		self.setGeometry(100, 100, 700, 500)
		self.setWindowTitle("PatternNexus...Maybe?")
		#self.setWindowIcon(QtGui.QIcon('web.png'))

		self.show()

	def closeEvent(self, event):
		#create a messagebox to confirm quit
		# when QtGui.QWidget is closed the QtGui.QCloseEvent is generated
		# to modify its behaviour the event handler (closeEvent()) must be reinplemented

		#create a msgBox with 2 buttons
		#4th argument is the button combination
		#5th argument is the button with initial ketboard focus
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Are you leaving?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		#test the return value, is "yes" the event is accepted
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

def main():
	#start the application
	app = QtGui.QApplication(sys.argv)
	ex = Example()

	sys.exit(app.exec_())

#if this module (.py-file) is run as the main program the statement is true
#if this module is imported the statement will return false
if __name__ == '__main__':
	main()