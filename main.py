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

mynodes = []

PORT = 55
'''
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
'''
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
        self.sub.clicked.connect(self.sub2)

    def printButt(self):
        print("Print listNode")
        print(mynodes)

    def sub2(self):
        p1 = ViewClass().mapToScene(int(mynodes[3].pos().x()),int(mynodes[3].pos().y()))
        p2 = ViewClass().mapToScene(int(mynodes[20].pos().x()),int(mynodes[20].pos().y()))

        par1 = mynodes[3].parentItem()
        par2 = mynodes[20].parentItem()

        x1 = p1.x() + par1.pos().x()
        y1 = p1.y() + par1.pos().y()
        x2 = p2.x() + par2.pos().x()
        y2 = p2.y() + par2.pos().y()

        print("p1,p2:", p1, p2)
        print("par1, par2:", par1, par2)
        print("x1, y1, x2, y2:", x1, y1, x2, y2)
        e = Edge(QPointF(x1, y1), QPointF(x2, y2))
        print("Edge:", e)
        mynodes[3].addEdge(e)
        mynodes[20].addEdge(e)



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
    mouseX = 0
    mouseY = 0
    idx = 0

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, QRectF(-2000, -2000, 4000, 4000), parent)
        self.node_start = None
        self.node_end = None
        self.pos = None
        self.pos_end = None

    def mouseDoubleClickEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if event.button() == Qt.LeftButton and self.node_start is None and modifiers == QtCore.Qt.AltModifier:
            SceneClass.prepStartEndNode = 1
            self.node_start = self.makeNodeFromTable(event.scenePos())
        else:
            self.node_start = None
            SceneClass.prepStartEndNode = 0
            self.saveNodeToGlobalList()

        pass

    def mouseMoveEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        x = event.scenePos().x()
        y = event.scenePos().y()
        self.mouseX = x
        self.mouseY = y
        super(SceneClass, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        global listNode, numberNode, temporListNodes
        modifiers = QApplication.keyboardModifiers()
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()

        if event.button() == Qt.LeftButton and self.node_start and modifiers == QtCore.Qt.ControlModifier:
            node = self.makeNodeFromTable(event.scenePos())                          #self.addItem(node)
            self.ItemIndexMethod(self.BspTreeIndex)
            self.node_end = node
            edge = Edge(self.node_start, self.node_end)
            # Save Nodes
            if len(temporListNodes) > 0:
                temporListNodes.append([numberNode, self.node_end.pos().x(), self.node_end.pos().y()])
            if len(temporListNodes) == 0:
                temporListNodes.append([numberNode, self.node_start.pos().x(), self.node_start.pos().y()])
                numberNode += 1
                temporListNodes.append([numberNode, self.node_end.pos().x(), self.node_end.pos().y()])
            numberNode += 1
            self.addItem(edge)
            self.node_start = self.node_end
        super(SceneClass, self).mousePressEvent(event)

    def saveNodeToGlobalList(self):
        global listNode, numberNode, temporListNodes
        listNode.append(temporListNodes)
        temporListNodes = []

    def makeNodeFromTable(self, mousePos):
        global listNode, numberNode
        b = DataWindow()
        t = b.nodeInfoWidget
        width = int(t.item(0, 11).text())
        height = int(t.item(0, 12).text())
        nodeName = t.item(0, 5).text()

        node = (XNode(None, QPointF(0, 0), width, height, nodeName))
        pnt = node
        mynodes.append(node)
        self.addItem(node)
        node.setPos(mousePos)

        for row in range(1, 15):                    #TODO - how many rows/columns to get
            xl = int(t.item(row, 0).text())
            yl = int(t.item(row, 1).text())
            namel = t.item(row, 2).text()
            numl = t.item(row, 3).text()
            seqNuml = t.item(row, 4).text()
            nodeName = t.item(row, 5).text()
            seqNumr = t.item(row, 6).text()
            numr = t.item(row, 7).text()
            namer = t.item(row, 8).text()
            xr = int(t.item(row, 9).text())
            yr = int(t.item(row, 10).text())
            width = int(t.item(row, 11).text())
            height = int(t.item(row, 12).text())
            print("width, height", width, height)
            if xl != 0 and yl != 0:
                nodel = (XNode(None, QPointF(0, 0), width, height, str(namel)))
                mynodes.append(nodel)
                mynodes[-1].setParentItem(pnt)
                mynodes[-1].setPos(QPointF(xl, yl))
                numberNode += 1
                x1 = (ViewClass().mapToScene(nodel.pos().x(), nodel.pos().x())).x()
                y1 = (ViewClass().mapToScene(nodel.pos().x(), nodel.pos().y())).y()
                listNode.append([numberNode, x1, y1])

            if xr != 0 and yr != 0:
                noder = (XNode(None, QPointF(0, 0), width, height, str(namer)))
                mynodes.append(noder)
                mynodes[-1].setParentItem(pnt)
                mynodes[-1].setPos(QPointF(xr, yr))
                numberNode += 1
                x1 = (ViewClass().mapToScene(noder.pos().x(), noder.pos().x())).x()
                y1 = (ViewClass().mapToScene(noder.pos().x(), noder.pos().y())).y()
                listNode.append([numberNode, x1, y1])

        # TODO Numbers node
        #elf.update()
        return node  # for use as start node


class XNode(QGraphicsItem):
    def __init__(self, parent, position, width, height, name):
        super(XNode, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.edges = []
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setPos(position)
        self.icolor = QColor(50,50,50)
        self.name = name
        self.width = width
        self.height = height
        self.setSelected(False)
        self.rec = QRectF(QPointF(-self.width/2, -self.height/2), QPoint(width, height))

    def boundingRect(self):
        adjust = 4
        return QRectF(self.rec)

    def paint(self, painter, option, widget):
        painter.setBrush(self.icolor)
        p = QPen(Qt.green)
        if self.isSelected():
            p = QPen(Qt.red)
        painter.drawRect(self.rec)
        #painter.drawRoundedRect(-20, 40, -80, 160, 5.0, 5.0, Qt.AbsoluteSize)

        p.setWidth(3)
        painter.setPen(p)
        p = QPen(Qt.darkBlue)
        f = QFont()
        fw = QFontMetricsF(f).width(self.name)
        fh = QFontMetricsF(f).height()
        painter.drawText(QPointF((-fw/2)+1, fh/2), self.name)

    def hoverEnterEvent(self, event):
        self.icolor = QColor(120,120,120)
        self.update()
        #self.update()
        #cursor = QCursor(Qt.OpenHandCursor)
        #QApplication.instance().setOverrideCursor(cursor)

    def hoverLeaveEvent(self, event):
        self.icolor = QColor(100,100,100)
        self.update()

    def mouseMoveEvent(self, event):
        global temporListNodes
        origCursorPos = event.lastScenePos()
        actualCursorPos = event.scenePos()
        origPos = self.scenePos()
        aktualCursorPos_x = actualCursorPos.x() - origCursorPos.x() + origPos.x()
        aktualCursorPos_y = actualCursorPos.y() - origCursorPos.y() + origPos.y()
        self.setPos(QPointF((aktualCursorPos_x), (aktualCursorPos_y)))

    def mousePressEvent(self, event):
        self.setSelected(True)

    def mouseReleaseEvent(self, event):
        pass

    def addEdge(self, edge):
        self.edges.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            pen = QPen()
            pen.setColor(Qt.green)
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
        return self.rect()'''
    '''def paint(self, painter, option, widget):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.darkGray), Qt.SolidPattern)
        # Draw rounded rectangle
        painter.drawPath(self.draw())
        painter.end()'''
    #def rect(self):
        #return self.boundingRect()

class Edge(QGraphicsLineItem):
    def __init__(self, source, dest, parent=None):
        QGraphicsLineItem.__init__(self, parent)

        if not isinstance(source, QPointF):
            print("====>>>Not QPointF")
            self.source = source
            self.dest = dest
            self.source.addEdge(self)
            self.dest.addEdge(self)

            self.pos1 = self.dest.pos()
            self.pos2 = self.source.pos()

        if isinstance(source, QPointF):
            print("=====>>>QPointF")
            self.pos1 = source
            self.pos2 = dest

        self.setPen(QPen(Qt.red, 3))
        self.adjust()

        return


    def adjust(self):
        self.prepareGeometryChange()
        self.setLine(QLineF(self.pos1, self.pos2))

    '''def adjust(self):
        self.prepareGeometryChange()
        self.setLine(QLineF(self.dest.pos(), self.source.pos()))'''

        #self.setLine(QLineF(QPointF(-100, -200), QPointF(300, 4000)))


        #self.s=SceneClass()
        #self.s.addLine(QLineF(-100.0, -200.0, 300, 400))
        #self.update()
        #self.show()



from dataView import H3TableHandler


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dw = DataWindow()
    dw.show()

    wd = WindowClass()
    wd.show()

    #h = H3TableHandler()


    sys.exit(app.exec_())

'''
self.clipboard = QApplication.clipboard()
self.mime_data = self.clipboard.mimeData()
self.pc = pyperclip
self.text_clip = ""'''