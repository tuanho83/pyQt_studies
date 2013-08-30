import sys
from PyQt4 import QtGui, QtCore

#create the graphicsView which contains the graphicsScene
class GraphicsView(QtGui.QGraphicsView):
	#initialize and set dragMode and renderHints for everything inside the view
	def __init__(self, parent=None):
		super(GraphicsView, self).__init__(parent)


		self.setRenderHint(QtGui.QPainter.Antialiasing)
		self.setRenderHint(QtGui.QPainter.TextAntialiasing)
		  
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		# self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

		self.__dragging = False

		
		# navigation / selection
		self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
		
		self._panning = False
		self._mousePressed = False
		self._lastPanPoint = QtCore.QPointF()
		self._center = QtCore.QPointF()
		self._centerNotSet = True



	#crate a zoom function for the mouse-wheel
	def wheelEvent(self, event):
		factor = 1.5 ** (event.delta() / 240.0)
		self.scale(factor, factor)

	def mouseReleaseEvent(self,event):
	
		if event.button() == QtCore.Qt.RightButton:
			self._panning = False
			self.setCursor(QtCore.Qt.ArrowCursor)
			# self.rightClicked.emit()
			print "rightClicked"
		if event.button() == QtCore.Qt.LeftButton:
			# self.leftClicked.emit()
			print "leftClicked"
			print self._lastPanPoint
			print self._center

		if event.button() == QtCore.Qt.MidButton:
			# self.shift_rightClicked.emit()
			print "middleClicked"
			
			
	def mousePressEvent(self,event):
		
		if event.button() == QtCore.Qt.RightButton:
			self.setCursor(QtCore.Qt.OpenHandCursor)	
			self._panning = True
			if self._centerNotSet:
				# self._center = (self.scene().itemsBoundingRect().topLeft() + self.scene().itemsBoundingRect().bottomRight()) * 0.5
				self._center = (self.scene().itemsBoundingRect().topLeft() + self.scene().itemsBoundingRect().bottomRight())* 0.5
				self._centerNotSet = False
				self._lastPanPoint = event.pos()
				super(GraphicsView, self).mouseReleaseEvent(event)	

	def mouseMoveEvent(self, event):
		if self._panning:
		  delta = self.mapToScene(self._lastPanPoint) - self.mapToScene(event.pos())
		  self._lastPanPoint = event.pos()
		  self._center += delta
		  self.centerOn(self._center);
		  print 'last position: %s'% self._lastPanPoint
		  print 'center frame: %s' % self._center
		  print 'event position: %s' % event.pos()
		else:
		  super(GraphicsView, self).mouseMoveEvent(event)

#create the GraphicsScene containing the main graphics
class GraphicsScene(QtGui.QGraphicsScene):

	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
		#set the size of the scene
		self.setSceneRect(0,0,2000,2000)

		#self.addRect(QtCore.QRectF(800,800,200,200))


		self.geos = []

		#create stuff to add to the scene
		geo_01 = QtGui.QGraphicsEllipseItem(800,800,200,200)

		#add stuff to the scene
		self.addItem(geo_01)

		self.geos.append(geo_01)


class Example(QtGui.QMainWindow):

	def __init__(self):
		#The "super()"-method returns the parrent object of the example-class
		#and it's constructor is called ("__init__")
		super(Example, self).__init__()

		self.initUI()

	#create the GUI
	def initUI(self):

		#create the main widget, which holds the layout
		self.main_widget = QtGui.QWidget(self)

		#create horizontal box layout to hold the vbox and the main area
		hbox = QtGui.QHBoxLayout()

		#store the GraphicsScene in a variable so it is not destroyed
		self.scene = GraphicsScene()
		#add the scene to the GraphicsView
		view = GraphicsView(self.scene)

		hbox.addWidget(view)
		hbox.addStretch(1)

		self.main_widget.setLayout(hbox)
		self.setCentralWidget(self.main_widget)
		self.setGeometry(100, 100, 700, 500)
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
