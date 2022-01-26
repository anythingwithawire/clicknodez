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

listNode = None
numberNode = 0
temporListNodes = None

mynodes = None
if mynodes is None:
    mynodes = list()

PORT = 55

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
        self.sub.clicked.connect(self.sub2)

    def printButt(self):
        print("Print listNode")
        print(mynodes)

    def sub2(self):
        p1 = mynodes[3].parentItem()
        p2 = mynodes[30].parentItem()

        e = Edge(mynodes[3], mynodes[30])
        mynodes[3].addEdge(e)
        mynodes[30].addEdge(e)



class ViewClass(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.s = SceneClass()
        self.setScene(self.s)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

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


class   SceneClass(QGraphicsScene):
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
        #self.addItem(XNode())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MiddleButton:
            print("MMB")
        x = event.scenePos().x()
        y = event.scenePos().y()
        #qt = QTransform()
        #print("SceneClass====>>", self.itemAt(x, y, qt))
        if event.button() == Qt.LeftButton and self.node_start is None:
            SceneClass.prepStartEndNode = 1
            b = DataWindow()
            t = b.nodeInfoWidget
            width = int(t.item(0, 11).text())
            height = int(t.item(0, 12).text())
            nodeName = t.item(0, 5).text()

            mynodes.append((XNode(None, QPointF(0,0), width, height, nodeName)))
            self.addItem(mynodes[-1])
            pnt = mynodes[-1]
            self.update()
            for row in range(0, 15):
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
                    mynodes.append(XNode(None, QPointF(0,0), width, height, str(namel)))
                    mynodes[-1].type = 70000
                    if (row!=0):
                        #mynodes[-1]
                        mynodes[-1].setParentItem(pnt)
                        mynodes[-1].setPos(QPointF(xl, yl))
                    mynodes[-1].setFlags(QGraphicsItem.ItemIsFocusable) #| QGraphicsItem.ItemIsMovable)
                    mynodes.append(XNode(None, QPointF(0, 0), width, height, str(namer)))
                    if (row != 0):
                        #mynodes[-1].
                        mynodes[-1].setParentItem(pnt)
                        mynodes[-1].setPos(QPointF(xr, yr))
                    mynodes[-1].setFlags(QGraphicsItem.ItemIsFocusable)  # | QGraphicsItem.ItemIsMovable)

                    self.update()
                '''nodel = XNode(None, QPointF(0, 0), 50, "L 389")
            self.addItem(nodel)
            self.update()

            # TODO Numbers node
            nodel.setPos(QPointF(-90 + xl, yl - 90 + (22 * row)))
            nodel.setZValue(110)
            nodel.setVisible(True)
            self.addItem(nodel)
            nodel.setParentItem(nodeP)
            self.update()
            if xr != 0 and yr != 0:
            noder = XNode(None, QPointF(0, 0), 10, "L 397")
            # TODO Numbers node
            self.addItem(nodel)
            noder.setPos(-90 + xr, yr - 90 + (22 * row))
            noder.setParentItem(nodeP)'''
            pnt.setPos(QPointF(self.mouseX, self.mouseY))

            '''for n in range(0, 16):
                node = XNode(None, event.scenePos() + QPoint(0, 22) * n, 10, str(n).zfill(2))
                # TODO Numbers node
                self.addItem(node)
                node.setParentItem(nodeP)
                node.setPos(110, -130 + (22 * n))
                self.node_start = node
            nodeP.setPos(x, y)'''
        else:
            self.node_start = None
            SceneClass.prepStartEndNode = 0
            self.saveNodeToGlobalList()


        '''nodeP = XNode(None, QPointF(SceneClass.mouseX, SceneClass.mouseY), 90, "Node 000")
        s=SceneClass()
        s.addItem(nodeP)
        s.update()
        b = DataWindow()
        t = b.nodeInfoWidget

        for row in range(0,10):
            xl = int(t.item(row, 0).text())
            yl = int(t.item(row, 1).text())
            namel = t.item(row, 2).text()
            numl = t.item(row, 3).text()
            seqNuml = t.item(row, 4).text()
            seqNumr = t.item(row, 5).text()
            numr = t.item(row, 6).text()
            namer = t.item(row, 7).text()
            yr = int(t.item(row, 8).text())
            xr = int(t.item(row, 9).text())
            K = self.Node()
            if xl !=0 and yl!=0:
                node = XNode(None, QPointF(0, 0) , 10, str(namel).zfill(2))
                # TODO Numbers node
                s.addItem(node)
                node.setPos(QPointF(-90+xl, yl-90 + (22 * row)))
                node.setParentItem(nodeP)
            if xr !=0 and yr!=0:
                node = XNode(None, QPointF(0, 0) , 10, str(namel).zfill(2))
                # TODO Numbers node
                s.addItem(node)
                node.setPos(-90+xr, yr-90 + (22 * row))
                node.setParentItem(nodeP)'''

    def saveNodeToGlobalList(self):
        global listNode, numberNode, temporListNodes
        listNode.append(temporListNodes)
        temporListNodes = None

    def mouseMoveEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        self.mouseX = x
        self.mouseY = y
        #print("mouse->", self.mouseX, self.mouseY, self)
        #i = self.itemAt(x,y, qt)
        #if i:
        #    print("====>>", i)
        super(SceneClass, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        i = self.itemAt(x, y, qt)
        if i:
            if i.isSelected():
                i.setSelected(False)
                print("====>>", i)
        super(SceneClass, self).mousePressEvent(event)

        '''x = event.scenePos().x()
        y = event.scenePos().y()
        qt = QTransform()
        global listNode, numberNode, temporListNodes
        if event.button() == Qt.LeftButton and self.node_start and not self.itemAt(x,y, qt):
            node = XNode(None, event.scenePos(), 10, "L 480")
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
            self.node_start = self.node_end'''

class Node(QGraphicsEllipseItem):
    def __init__(self, rect=QRectF(-20, -20, 20, 20), parent=None):
        QGraphicsEllipseItem.__init__(self, rect, parent)
        self.edges = None
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

    def __init__(self, parent, position, width, height, name):
        super(XNode, self).__init__(parent)
        #self.XNode(None, position, size, name)
        self.setAcceptHoverEvents(True)
        self.edges = None
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        #self.setPos(position)
        self.icolor = QColor(50,50,50)
        self.name = name
        self.width=width
        self.height=height
        self.setSelected(False)
        self.rec=QRectF(QPointF(-self.width/2, -self.height/2), QPoint(width, height))


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
        #painter.GraphicsRectItem(self.boundingRect())
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
        pass

        global temporListNodes
        origCursorPos = event.lastScenePos()
        actualCursorPos = event.scenePos()

        origPos = self.scenePos()
        #print(origCursorPos.x(), origCursorPos.y(), "Old position of x,y")
        #if len(temporListNodes) > 0:
        #    for i in range(len(temporListNodes)):
        #        for j in range(len(temporListNodes[i])):
        #            print(temporListNodes[i][j], 'temporListNodes [i][j]')
        aktualCursorPos_x = actualCursorPos.x() - origCursorPos.x() + origPos.x()
        aktualCursorPos_y = actualCursorPos.y() - origCursorPos.y() + origPos.y()
        self.setPos(QPointF((aktualCursorPos_x), (aktualCursorPos_y)))

        #print((aktualCursorPos_x, aktualCursorPos_y), "New position of x,y")'''

    def mousePressEvent(self, event):
        pass
        #self.setSelected(True)

    def mouseReleaseEvent(self, event): pass

    def addEdge(self, edge):
        if self.edges:
            self.edges.append(edge)
        else:
            self.edges = list()

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
            if self.edges:
                for edge in self.edges:
                    edge.adjust()
            else:
                edges = list()

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
        self.source = self.mapToScene(source.pos())
        self.dest = self.mapToScene(dest.pos())
        source.addEdge(self.source)
        dest.addEdge(self.dest)
        #self.source.addEdge(self)
        #self.dest.addEdge(self)
        #self.setPen(QPen(Qt.red, 3))
        self.adjust()

    def adjust(self):
        self.prepareGeometryChange()
        self.setLine(QLineF(self.dest + QPointF(-0, -0), self.source + QPointF(-0, -0)))


        self.setLine(QLineF(QPointF(-100, -200), QPointF(300, 4000)))


        self.s=SceneClass()
        self.s.addLine(QLineF(-100.0, -200.0, 300, 400))
        self.update()
        self.show()

        x=1


from dataView import H3TableHandler


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dw = DataWindow()
    dw.show()

    wd = WindowClass()
    wd.show()

    h = H3TableHandler()

    sys.exit(app.exec_())

'''
self.clipboard = QApplication.clipboard()
self.mime_data = self.clipboard.mimeData()
self.pc = pyperclip
self.text_clip = ""'''