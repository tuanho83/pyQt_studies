import sys
import random
from PyQt4.QtGui import * 

NO_INDEX = False
OPTIMIZE = False
ITEM_COORD_CACHE = False
ITEM_DEVICE_CACHE = False
NESTED_ITEMS = False


class TestItem(QGraphicsEllipseItem):
    def paint(self, painter, option, index):
        return QGraphicsEllipseItem.paint(self, painter, option, index)

    def hoverEnterEvent (self, e):
        self.setBrush(QBrush(QColor("orange")))

    def hoverLeaveEvent(self,e):
        self.setBrush(QBrush(None))

if __name__ == '__main__':
    n = int(sys.argv[1]) # Number of items. With 5000 I already
                           # have performance problems
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Populates scene
    prev = None
    for i in xrange(n):
        # Random geometry and position
        r1 = random.randint(10, 100)
        # r2 = random.randint(10, 100)
        r1 = 10
        r2 = 10
        x = random.randint(0, 200)
        y = random.randint(0, 200)

        item = TestItem(x, y, r1*2, r2*2)
        item.setAcceptsHoverEvents(True)

        if NESTED_ITEMS: 
            # Creates a parent child structure among items
            if not prev:
                scene.addItem(item)
            else:
                item.setParentItem(prev)
            prev = item
        else:
            scene.addItem(item)

        if ITEM_COORD_CACHE:
            item.setCacheMode(QGraphicsItem.ItemCoordinateCache)
        elif ITEM_DEVICE_CACHE:
            item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    # Creates View
    view = QGraphicsView(scene)
    # Sets basic Flags for nice rendering 
    view.setRenderHints(QPainter.Antialiasing or QPainter.SmoothPixmapTransform)

    if NO_INDEX:
        view.setItemIndexMethod(QGraphicsScene.NoIndex);

    if OPTIMIZE:
        view.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing
                                  or QGraphicsView.DontClipPainter
                                  or QGraphicsView.DontSavePainterState)

    view.show()
    sys.exit(app.exec_())
