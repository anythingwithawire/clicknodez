import sys
from clipboard import ClipboardEx
from dataView import DataWindow

import PyQt5
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

import sys
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem



listNode = []
numberNode = 0
temporListNodes = []


class GraphicsRectItem(QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)


class WindowClass(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.view = ViewClass()
        # self.setCentralWidget(self.view)
        self.h = QHBoxLayout(self)
        self.h.addWidget(self.view)
        self.butt = QPushButton("Print")
        self.sub = QPushButton("Sub")
        self.h.addWidget(self.butt)
        self.h.addWidget(self.sub)
        self.setLayout(self.h)

        self.mainWid = QWidget(self)
        self.mainWid.setFocus()
        self.setCentralWidget(self.mainWid)
        self.mainWid.setLayout(self.h)

        self.butt.clicked.connect(self.printButt)
        self.sub.clicked.connect(SceneClass.sub)

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
            nodeP = XNode(None, event.scenePos(), 120, "Node 000")
            self.addItem(nodeP)
            for n in range(0,16):
                node = XNode(None, event.scenePos()+ QPoint(0,22) * n, 10, str(n).zfill(2))
                # TODO Numbers node
                self.addItem(node)
                node.setParentItem(nodeP)
                node.setPos(110, -130 +(22 * n))
                self.node_start = node
        else:
            self.node_start = None
            SceneClass.prepStartEndNode = 0
            self.saveNodeToGlobalList()


    def sub(self):
        print("sub")
        sub = GraphicsRectItem(0,0,2100, 1500)
        sub.setPos(0,0)
        self.addItem(sub)

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
            node = XNode(None, event.scenePos(), 10, "fred")
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

    def __init__(self, parent, position, size, name):
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
        self.size = size

        #i = GraphicsRectItem(-50, -50, 100, 100)
        #self.parentItem().scene().addItem(i)

    def boundingRect(self):
        adjust = self.size/4
        return QRectF(-self.size-adjust, -self.size-adjust, adjust +(self.size * 2), adjust +(self.size * 2))

    def paint(self, painter, option, widget):
        painter.setBrush(self.icolor)
        p = QPen(Qt.green)
        if self.isSelected():
            p = QPen(Qt.darkYellow)
        painter.drawRect(self.boundingRect())

        p.setWidth(3)
        painter.setPen(p)
        #painter.GraphicsRectItem(self.boundingRect())
        p = QPen(Qt.green)
        f = QFont()
        fw = QFontMetricsF(f).width(self.name)
        fh = QFontMetricsF(f).height()
        painter.drawText(QPointF(-fw/2, fh/4), self.name)


    def hoverEnterEvent(self, event):
        self.icolor = Qt.red
        self.update()
        #cursor = QCursor(Qt.OpenHandCursor)
        #QApplication.instance().setOverrideCursor(cursor)

    def hoverLeaveEvent(self, event):
        self.icolor = Qt.blue
        self.update()

    def mouseMoveEvent(self, event):
        global temporListNodes
        origCursorPos = event.lastScenePos()
        actualCursorPos = event.scenePos()

        origPos = self.scenePos()
        '''print(origCursorPos.x(), origCursorPos.y(), "Old position of x,y")
        if len(temporListNodes) > 0:
            for i in range(len(temporListNodes)):
                for j in range(len(temporListNodes[i])):
                    print(temporListNodes[i][j], 'temporListNodes [i][j]')'''
        aktualCursorPos_x = actualCursorPos.x() - origCursorPos.x() + origPos.x()
        aktualCursorPos_y = actualCursorPos.y() - origCursorPos.y() + origPos.y()
        self.setPos(QPointF((aktualCursorPos_x), (aktualCursorPos_y)))

        #print((aktualCursorPos_x, aktualCursorPos_y), "New position of x,y")

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
        self.setLine(QLineF(self.dest.pos() + QPointF(-0, -0), self.source.pos() + QPointF(-0, -0)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dw = DataWindow()
    dw.show()

    wd = WindowClass()
    wd.show()
    sys.exit(app.exec_())

'''
self.clipboard = QApplication.clipboard()
self.mime_data = self.clipboard.mimeData()
self.pc = pyperclip
self.text_clip = ""'''