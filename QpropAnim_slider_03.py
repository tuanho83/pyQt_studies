
from PyQt4 import QtCore, QtGui

class animGB(QtGui.QWidget):
	infoStat_SIGNAL = QtCore.pyqtSignal(bool)
	noteStat_SIGNAL = QtCore.pyqtSignal(bool)
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.infoStat_SIGNAL.connect(self.infoChecker)
		self.noteStat_SIGNAL.connect(self.noteChecker)

		self._vbox = QtGui.QVBoxLayout()
		self._gbContainer = QtGui.QGroupBox()
		self._gbContainer.setMinimumSize(QtCore.QSize(370, 200))
		self._gbContainer.setMaximumSize(QtCore.QSize(370, 200))
		self._hbox = QtGui.QHBoxLayout()

		self.box = QtGui.QGroupBox()
		self.box.setMinimumSize(QtCore.QSize(350, 150))
		self.box.setMaximumSize(QtCore.QSize(350, 150))
		self.box.setStyleSheet("QGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(20%, 30%, 30%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title{background:transparent; margin-top:5px; margin-left:5px;}")
		self.box.setTitle("C'est la vie.")

		self.infoButton = Ext_Button(self.box)
		self.infoButton.setText('i')
		self.infoButton.setObjectName('info')
		self.infoButton.mouseHover.connect(self.info_anim)
		self.infoButton.setGeometry(QtCore.QRect(325, 125, 20, 20))

		self.noteButton = Ext_Button(self.box)
		self.noteButton.setText('o')
		self.noteButton.setObjectName('notes')
		self.noteButton.mouseHover.connect(self.notes_anim)
		self.noteButton.setGeometry(QtCore.QRect(300, 125, 20, 20))

		self.info_gb = QtGui.QGroupBox(self.box)
		self.info_gb.hide()
		self.info_gb.setTitle('Info Box')
		self.info_gb.setObjectName('childGroupBox')
		self.info_gb.setStyleSheet("QGroupBox#childGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(10%, 30%, 10%, 30%); margin: 1px; padding: 5px;} QGroupBox:Title#childGroupBox{background:transparent; margin-top:5px; margin-left:5px;}")
		self._hbox.addWidget(self.box)

		self.note_gb = QtGui.QGroupBox(self.box)
		self.note_gb.hide()
		self.note_gb.setTitle('Notes')
		self.note_gb.setObjectName('childGroupBox')
		self.note_gb.setStyleSheet("QGroupBox#childGroupBox {background: transparent; border: 2px solid black;color: black; background-color: rgba(10%, 30%, 25%, 70%); margin: 1px; padding: 5px;} QGroupBox:Title#childGroupBox{background:transparent; margin-top:5px; margin-left:5px;}")

		self.infoStatus =True
		self.noteStatus =True

		self._vbox.addWidget(self.box)
		self._gbContainer.setLayout(self._vbox)

		centerWidget = QtGui.QVBoxLayout(self)
		centerWidget.addWidget(self._gbContainer)

	def info_anim(self,sigbool):
		# On hover, animate in
		if sigbool == True:
			self.animation_01 = QtCore.QPropertyAnimation(self.info_gb, "geometry")
			self.animation_01.setDuration(250)
			self.animation_01.setStartValue(QtCore.QRect(10, 200, 250, 80))
			self.animation_01.setEndValue(QtCore.QRect(10, 50, 250, 80))

			# Check to see if other anim have finished. Without this
			# animation start to freeze and becomes glitchy.
			if self.noteStatus is True:
				print 'note anim finished: ready'
				self.info_gb.show()
				self.animation_01.start()
			else:
				print 'note anim unfinished: not ready!'
				self.info_gb.hide()
		# Exit hover, animate out
		else:
			self.animation_01.setDuration(150)
			self.animation_01.setStartValue(QtCore.QRect(10, 50, 250, 80))
			self.animation_01.setEndValue(QtCore.QRect(10, 250, 250, 80))
			self.animation_01.start()
			self.animation_01.stateChanged.connect(self.infostatus)

	def notes_anim(self,sigbool):
		# On hover, animate in
		if sigbool == True:
			self.animation_02 = QtCore.QPropertyAnimation(self.note_gb, "geometry")
			self.animation_02.setDuration(250)
			self.animation_02.setStartValue(QtCore.QRect(-400, 50, 250, 80))
			self.animation_02.setEndValue(QtCore.QRect(10, 50, 250, 80))

			if self.infoStatus is True:
				print 'info anim finished: ready'
				self.note_gb.show()
				self.animation_02.start()
			else:
				self.note_gb.hide()
				print 'info anim unfinished: not ready!'
		# Exit hover, animate out
		else:
			self.animation_02.setDuration(150)
			self.animation_02.setStartValue(QtCore.QRect(10, 50, 250, 80))
			self.animation_02.setEndValue(QtCore.QRect(-400, 50, 250, 80))
			self.animation_02.start()
			self.animation_02.stateChanged.connect(self.notestatus)


	def infostatus(self):
		# print 'hover out'
		self.animation_01.finished.connect(self.infoOutro)
		self.infoStat_SIGNAL.emit(False)

	def infoOutro(self):
		self.infoStat_SIGNAL.emit(True)
		# print 'info anim finished'

	def infoChecker(self,bool):
		# print bool
		self.infoStatus = bool
		return bool


	def notestatus(self):
		# print 'hover out'
		self.animation_02.finished.connect(self.noteOutro)
		self.noteStat_SIGNAL.emit(False)

	def noteOutro(self):
		self.noteStat_SIGNAL.emit(True)
		
	def noteChecker(self,bool):
		# print bool
		self.noteStatus = bool
		return bool

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
