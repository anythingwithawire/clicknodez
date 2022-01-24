import sys

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QMainWindow

listNode = []
numberNode = 0
temporListNodes = []


class WindowClass(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.view = ViewClass()
        # self.setCentralWidget(self.view)
        self.h = QHBoxLayout(self)
        self.h.addWidget(self.view)
        self.butt = QPushButton("Print")
        self.h.addWidget(self.butt)
        self.setLayout(self.h)

        self.mainWid = QWidget(self)
        self.mainWid.setFocus()
        self.setCentralWidget(self.mainWid)
        self.mainWid.setLayout(self.h)

        self.butt.clicked.connect(self.printButt)

    def printButt(self):
        print("Print listNode")
        print(listNode)


class ViewClass(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.s = SceneClass()
        self.setScene(self.s)
        self.setRenderHint(QPainter.Antialiasing)


        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event):

        print(event)
        # Zoom Factor
        zoomInFactor = 1.2
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor


        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
        return
        #event.accept()
        # do not propagate the event to the scroll area scrollbars
        return True

class SceneClass(QGraphicsScene):
    prepStartEndNode = 0

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, QRectF(0, 0, 2000, 2000), parent)

        self.node_start = None
        self.node_end = None
        self.pos = None
        self.pos_end = None

        #self.addItem(XNode())

    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.MiddleButton:
            print("MMB")
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        print("====>>", self.itemAt(x,y, qt))
        if event.button() == Qt.LeftButton and self.node_start is None :
            SceneClass.prepStartEndNode = 1
            node = XNode(None, event.scenePos(), "bill")
            # TODO Numbers node
            self.addItem(node)
            node.setPos(event.scenePos())
            self.node_start = node
        else:
            self.node_start = None
            SceneClass.prepStartEndNode = 0

            self.saveNodeToGlobalList()
        # def wheelEvent(self, source, event):



    def saveNodeToGlobalList(self):
        global listNode, numberNode, temporListNodes

        listNode.append(temporListNodes)
        temporListNodes = []

    def mouseMoveEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        i = self.itemAt(x,y, qt)
        if i:
            print("====>>", i)
        super(SceneClass, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        global listNode, numberNode, temporListNodes
        if event.button() == Qt.LeftButton and self.node_start and not self.itemAt(x,y, qt):
            node = XNode(None, event.scenePos(), "fred")
            self.addItem(node)


            # TODO Numbers node

            # Indexing Node?
            self.ItemIndexMethod(self.BspTreeIndex)

            #node.setPos(event.scenePos() + QPointF(10, 10))

            self.node_end = node
            edge = Edge(self.node_start, self.node_end)

            # Save Nodes
            if len(temporListNodes) > 0:
                temporListNodes.append([numberNode,
                                        self.node_end.pos().x(),
                                        self.node_end.pos().y()])

            if len(temporListNodes) == 0:
                temporListNodes.append([numberNode,
                                        self.node_start.pos().x(),
                                        self.node_start.pos().y()])

                numberNode += 1
                temporListNodes.append([numberNode,
                                        self.node_end.pos().x(),
                                        self.node_end.pos().y()])

            numberNode += 1

            self.addItem(edge)

            self.node_start = self.node_end
        super(SceneClass, self).mousePressEvent(event)



class Node(QGraphicsEllipseItem):
    def __init__(self, rect=QRectF(-20, -20, 20, 20), parent=None):
        QGraphicsEllipseItem.__init__(self, rect, parent)
        self.edges = []
        self.setZValue(1)
        self.setBrush(Qt.darkGray)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        # self.setAcceptHoverEvents(True)

    def mouseMoveEvent(self, event):
        global temporListNodes
        origCursorPos = event.lastScenePos()
        actualCursorPos = event.scenePos()

        origPos = self.scenePos()
        print(origCursorPos.x(), origCursorPos.y(), "Old position of x,y")
        if len(temporListNodes) > 0:
            for i in range(len(temporListNodes)):
                for j in range(len(temporListNodes[i])):
                    print(temporListNodes[i][j], 'temporListNodes [i][j]')
        aktualCursorPos_x = actualCursorPos.x() - origCursorPos.x() + origPos.x()
        aktualCursorPos_y = actualCursorPos.y() - origCursorPos.y() + origPos.y()
        self.setPos(QPointF(aktualCursorPos_x, aktualCursorPos_y))

        print((aktualCursorPos_x, aktualCursorPos_y), "New position of x,y")

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

    def addEdge(self, edge):
        self.edges.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.setBrush(Qt.green if value else Qt.darkGray)

        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()

        return QGraphicsItem.itemChange(self, change, value)



class XNode(QGraphicsItem):
    """
    A simple QGraphicsItem that can be dragged around the scene.
    Of course, this behavior is easier to achieve if you simply use the default
    event handler implementations in place and call
    QGraphicsItem.setFlags( QGraphicsItem.ItemIsMovable )

    ...but this example shows how to do it by hand, in case you want special behavior
    (e.g. only allowing left-right movement instead of arbitrary movement).
    """

    def __init__(self, parent, position, name):
        super(XNode, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.edges = []
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setPos(position)
        self.icolor = Qt.red
        self.setAcceptHoverEvents(True)
        self.name = name

    def boundingRect(self):
        return QRectF(-25, -25, 50, 50)

    def paint(self, painter, option, widget):
        painter.setBrush(self.icolor)
        p = QPen(Qt.green)
        if self.isSelected():
            p = QPen(Qt.darkYellow)

        p.setWidth(3)
        painter.setPen(p)
        painter.drawRect(self.boundingRect())
        p = QPen(Qt.green)
        painter.drawText(QPointF(-10, 0), self.name)

    def hoverEnterEvent(self, event):
        self.icolor = Qt.red
        self.update()
        #cursor = QCursor(Qt.OpenHandCursor)
        #QApplication.instance().setOverrideCursor(cursor)

    def hoverLeaveEvent(self, event):
        self.icolor = Qt.blue
        self.update()
        #QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self, event):
        #new_pos = event.scenePos()

        # Keep the old Y position, so only the X-pos changes.
        #old_pos = self.scenePos()
        #new_pos.setY(old_pos.y())

        #self.setPos(new_pos)

        global temporListNodes
        origCursorPos = event.lastScenePos()
        actualCursorPos = event.scenePos()

        origPos = self.scenePos()
        print(origCursorPos.x(), origCursorPos.y(), "Old position of x,y")
        if len(temporListNodes) > 0:
            for i in range(len(temporListNodes)):
                for j in range(len(temporListNodes[i])):
                    print(temporListNodes[i][j], 'temporListNodes [i][j]')
        aktualCursorPos_x = actualCursorPos.x() - origCursorPos.x() + origPos.x()
        aktualCursorPos_y = actualCursorPos.y() - origCursorPos.y() + origPos.y()
        self.setPos(QPointF(aktualCursorPos_x, aktualCursorPos_y))

        print((aktualCursorPos_x, aktualCursorPos_y), "New position of x,y")
    # We must override these or else the default implementation prevents
    #  the mouseMoveEvent() override from working.
    def mousePressEvent(self, event):
        self.setSelected(True)

    def mouseReleaseEvent(self, event): pass

    def addEdge(self, edge):
        self.edges.append(edge)


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            pen = QPen()
            pen.setColor(Qt.green)
            #pen.setBrush(QBrush(Qt.darkGray), Qt.SolidPattern)
            self.icolor = (Qt.green if value else Qt.darkGray)
            self.prepareGeometryChange()
            self.update()

        if change == QGraphicsItem.ItemPositionHasChanged:
            self.prepareGeometryChange()
            for edge in self.edges:
                edge.adjust()

        return QGraphicsItem.itemChange(self, change, value)
    '''path = QPainterPath()
    path.adPath(item)
    return path'''

    '''
    def boundedRect(self):
        return self.rect()

   def paint(self, painter, option, widget):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.darkGray), Qt.SolidPattern)
        # Draw rounded rectangle
        painter.drawPath(self.draw())
        painter.end()


    def rect(self):
        return QRectF(-50, -50, 100, 100)'''


class Edge(QGraphicsLineItem):
    def __init__(self, source, dest, parent=None):
        QGraphicsLineItem.__init__(self, parent)
        self.source = source
        self.dest = dest
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.setPen(QPen(Qt.red, 3))
        self.adjust()

    def adjust(self):
        self.prepareGeometryChange()
        self.setLine(QLineF(self.dest.pos() + QPointF(-10, -10), self.source.pos() + QPointF(-10, -10)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wd = WindowClass()
    wd.show()
    sys.exit(app.exec_())
