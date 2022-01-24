import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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

class SceneClass(QGraphicsScene):

    prepStartEndNode = 0
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, QRectF(0, 0, 2000, 2000), parent)

        self.node_start = None
        self.node_end = None
        self.pos = None
        self.pos_end = None

    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.MiddleButton:
            print("MMB")

        if event.button() == Qt.LeftButton and self.node_start is None:
            SceneClass.prepStartEndNode = 1
            node = Node()
            # TODO Numbers node
            self.addItem(node)
            node.setPos(event.scenePos() + QPointF(10, 10))
            self.node_start = node
        else:
            self.node_start = None
            SceneClass.prepStartEndNode = 0

            self.saveNodeToGlobalList()

    def saveNodeToGlobalList(self):
        global listNode, numberNode, temporListNodes

        listNode.append(temporListNodes)
        temporListNodes = []


    def mouseMoveEvent(self, event):
        super(SceneClass, self).mouseMoveEvent(event)


    def mousePressEvent(self, event):
        global listNode, numberNode, temporListNodes
        if event.button() == Qt.LeftButton and self.node_start:
            node = Node()
            # TODO Numbers node
            self.addItem(node)

            # Indexing Node?
            self.ItemIndexMethod(self.BspTreeIndex)

            node.setPos(event.scenePos() + QPointF(10, 10))

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
        #self.setAcceptHoverEvents(True)

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

