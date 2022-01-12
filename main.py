def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import numpy.random as rd
from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):
    DEFAULT_PEN_SIZE = 1.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.m = Menu(self.root, tearoff=0)
        self.m.add_command(label="Draw", command=self.draw)
        self.m.add_command(label="Eraser", command=self.eraser)
        self.m.add_separator()
        self.m.add_command(label="Fill", command=self.fill)
        self.m.add_command(label="Color", command=self.colorSelector)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=0)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()

        self.root.bind("<Button-3>", self.do_popup)

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.draw
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def draw(self):
        self.eraser_on = False

    def colorSelector(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def eraser(self):
        self.eraser_on = True

    def fill(self):
        self.eraser_on = False

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear(self):
        self.c.delete("all")

    def drawLine(self, x, y, z, a):
        self.c.create_line(x, y, z, a)

    def drawLine(self, line):
        x, y = line[0][:]
        z, a = line[1][:]
        self.c.create_line(x, y, z, a)


'''
def line_intersection(line1, line2, i):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])  # ax-bx,cx-dx
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False
    # raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    i[0] = x
    i[1] = y
    return True
    
    
class MyCanva(Frame):

    def __init__(self):
        super().__init__()
        self.master.title("MathProject")
        self.pack(fill=BOTH, expand=1)



    def initUI(self, canvas):
        canvas.create_line(15, 25, 200, 25)
        canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)


def main():
    root = Tk()
    myCanva = MyCanva()
    canvas = Canvas(myCanva)
    myCanva.initUI(canvas)
    root.geometry("400x250+300+300")
    canvas.pack(fill=BOTH, expand=1)
    root.mainloop()
'''


# Create a point using 2 coords
def CreatePoint(x1, y1):
    return np.array([x1, y1])


# Create a segment using 4 coords
def CreateSegment4(x1, y1, x2, y2):
    return np.array([[x1, y1], [x2, y2]])


# Create a segment using 2 points
def CreateSegment(p1, p2):
    # return CreateSegment(p1[0], p1[1], p2[0], p2[1])
    return np.array([[p1[0], p1[1]],
                     [p2[0], p2[1]]
                     ])


# Create a polygone using a list of points (points du tk avec dernier element identique au premier)
def CreatePolygone(pointList):
    long = pointList.size
    if long == 0:
        return np.zeros(1)
    res = np.zeros((2, long))
    for i in range(0, long, 2):
        res[i][0] = pointList[i]
        res[i][1] = pointList[i + 1]


# dessine toutes les cotes d un polygone array
def DrawPolygon(listSegments):
    for ind in range(len(listSegments)):
        myPaint.drawLine(listSegments[ind])


# dx = x2-x1 et dy = y2-y1, alors les normales sont (-dy, dx) et (dy, -dx).
def CalculateNormals(myPolygon):
    normalList = []
    for ind in range(len(myPolygon)):
        seg = myPolygon[ind]
        dx = seg[1][0] - seg[0][0]
        dy = seg[1][1] - seg[0][1]
        norm = np.array([[dy, -dx], [-dy, dx]], dtype=float)
        norm = norm / norm.max()
        normalList.append(norm)
    return normalList


# Q(t) = (1 − t)A + tB, t ∈ [0, 1], l'équation paramétrique du segment [AB].
def EquationParametric(Segment, tValue):
    ptA = Segment[0][:]
    ptB = Segment[1][:]
    return (1 - tValue) * ptA + tValue * ptB


# change a 2*2 Vector to a 2*1
def NewNormal(normal):
    difX = -normal[0][0]
    difY = -normal[0][1]
    return np.array([normal[1][0] + difX, normal[1][1] + difY])


# trouve la valeur T d intersection d un segment selon un cote de polygone et sa normale
def FindTValue(Segment, Polygon, Normal):
    ptA = Segment[0][:]
    ptB = Segment[1][:]
    ptP = Polygon[0][:]
    D = ptB - ptA
    Wi = ptA - ptP
    n = NewNormal(Normal)
    denominator = np.dot(D, n)
    if denominator > 0:
        tIsInf = True
    else:
        tIsInf = False
    return -np.dot(Wi, n) / denominator, tIsInf


# mets a jour le tinf et tsup d un segment
# par rapport a un cote et sa normale
def CyriusBeckBis(segment, cotePolygon, normal, tInf, tSup):
    t, isInfValue = FindTValue(segment, cotePolygon, normal)
    if isInfValue:
        if t > tInf:
            tInf = t
    else:
        if t < tSup:
            tSup = t
    return tInf, tSup


# renvoie true si la ligne appartient au polygone
# selon son tInf et tSup et les nouvelles valeurs t
def CyriusBeckAddLine(tInf, tSup, newSegment):
    print(tInf, tSup)
    if tInf < tSup:
        if tInf < 0 and tSup > 1:
            # print("segment interieur", tInf, tSup)
            return True, [0, 1]
        else:
            if tInf > 1 or tSup < 0:
                # print("segment exterieur", tInf, tSup)
                return False, newSegment
            else:
                if tInf < 0:
                    # print("A = origin segment interieur")
                    tInf = 0
                else:
                    if tSup > 1:
                        # print("B extremite segment int")
                        tSup = 1
                # print("creer nouveau segment ", tInf, tSup)
                newSegment = [tInf, tSup]
                return True, newSegment
    else:
        # print("segment exterieur", tInf, tSup)
        return False, newSegment


# fonction cyrius beck qui renvoie une liste de segments inclus dans le polygone
def CyriusBeck():
    newSegmentList = []
    newSegment = [0, 0]
    print("Nb segments to check : ", len(segmentList))
    for segment in segmentList:
        tInf = -np.exp(9)
        tSup = np.exp(9)
        for ind in range(len(polygonConvex)):
            tInf, tSup = CyriusBeckBis(segment, polygonConvex[ind], polygonNormals[ind], tInf, tSup)
        # ajouter a la nouvelle liste le nouveau segment ou pas
        resLine, newSegment = CyriusBeckAddLine(tInf, tSup, newSegment)
        if resLine:
            a = (EquationParametric(segment, newSegment[0]))
            b = (EquationParametric(segment, newSegment[1]))
            newSegmentList.append(CreateSegment(a, b))
            # newSegmentList.append(segment)
    print("New segments : ", len(newSegmentList))
    return newSegmentList


# cree un nombre n donne aleatoire de lignes
def RandomLines(nbToCreate):
    for ind in range(nbToCreate):
        x1, x2, x3, x4 = rd.randint(0, 600, 4, dtype=int)
        # x3, x4 = rd.randint(301, 600, 2, dtype=int)
        seg = CreateSegment4(x1, x2, x3, x4)
        segmentList.append(seg)


# dessine tous les segments
def DrawAllLines():
    for segment in segmentList:
        myPaint.drawLine(segment)


segmentList = []  # la list des segments hors polygon convex
polygonConvex = []  # la list des cotes du polygon convex
polygonNormals = []  # la list des normals de chaque cote du polygon convex

if __name__ == '__main__':

    # creation des points du polygon
    p1 = [300, 200]
    p2 = [500, 300]
    p3 = [500, 400]
    p4 = [300, 300]

    # creation des cotes du polygon
    s1 = CreateSegment(p1, p2)
    s2 = CreateSegment(p2, p3)
    s3 = CreateSegment(p3, p4)
    s4 = CreateSegment(p4, p1)

    # adding cotes to polygon list
    polygonConvex.append(s1)
    polygonConvex.append(s2)
    polygonConvex.append(s3)
    polygonConvex.append(s4)

    # create normals for each polygon
    polygonNormals = CalculateNormals(polygonConvex)

    # test1 = CreateSegment4(200, 250, 450, 250)
    # segmentList.append(test1)

    myPaint = Paint()

    DrawPolygon(polygonConvex)

    RandomLines()
    # DrawAllLines()
    segmentList = CyriusBeck()

    DrawAllLines()
    # myPaint.drawLine(polygonNormals[0][:])
    # myPaint.drawLine(test1)

    myPaint.root.mainloop()
