from tkinter import *
from tkinter.colorchooser import askcolor
import numpy as np
import numpy.random as rd


class MainClass:

    def __init__(self):
        self.segmentList = []  # la list des segments hors polygon convex
        self.polygonConvex = []  # la list des cotes du polygon convex
        self.polygonNormals = []  # la list des normals de chaque cote du polygon convex

    segmentList = []  # la list des segments hors polygon convex
    polygonConvex = []  # la list des cotes du polygon convex
    polygonNormals = []  # la list des normals de chaque cote du polygon convex

    # Create a point using 2 coords
    def CreatePoint(self, x1, y1):
        return np.array([x1, y1])

    # Create a segment using 4 coords
    def CreateSegment4(self, x1, y1, x2, y2):
        return np.array([[x1, y1], [x2, y2]])

    # Create a segment using 2 points
    def CreateSegment(self, p1, p2):
        # return CreateSegment(p1[0], p1[1], p2[0], p2[1])
        return np.array([[p1[0], p1[1]],
                         [p2[0], p2[1]]
                         ])

    # Create a polygone using a list of points (points du tk avec dernier element identique au premier)
    def CreatePolygone(self, pointList):
        long = pointList.size
        if long == 0:
            return np.zeros(1)
        res = np.zeros((2, long))
        for i in range(0, long, 2):
            res[i][0] = pointList[i]
            res[i][1] = pointList[i + 1]

    # dx = x2-x1 et dy = y2-y1, alors les normales sont (-dy, dx) et (dy, -dx).
    def CalculateNormals(self, myPolygon):
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
    def EquationParametric(self, Segment, tValue):
        ptA = Segment[0][:]
        ptB = Segment[1][:]
        return (1 - tValue) * ptA + tValue * ptB

    # dessine tous les segments
    def DrawAllLines(self):
        for segment in self.segmentList:
            myPaint.drawLine(segment)

    # change a 2*2 Vector to a 2*1
    def NewNormal(self, normal):
        difX = -normal[0][0]
        difY = -normal[0][1]
        return np.array([normal[1][0] + difX, normal[1][1] + difY])

    # trouve la valeur T d intersection d un segment selon un cote de polygone et sa normale
    def FindTValue(self, Segment, Polygon, Normal):
        ptA = Segment[0][:]
        ptB = Segment[1][:]
        ptP = Polygon[0][:]
        D = ptB - ptA
        Wi = ptA - ptP
        n = self.NewNormal(Normal)
        denominator = np.dot(D, n)
        if denominator > 0:
            tIsInf = True
        else:
            tIsInf = False
        return -np.dot(Wi, n) / denominator, tIsInf

    # mets a jour le tinf et tsup d un segment
    # par rapport a un cote et sa normale
    def CyriusBeckBis(self, segment, cotePolygon, normal, tInf, tSup):
        t, isInfValue = self.FindTValue(segment, cotePolygon, normal)
        if isInfValue:
            if t > tInf:
                tInf = t
        else:
            if t < tSup:
                tSup = t
        return tInf, tSup

    # renvoie true si la ligne appartient au polygone
    # selon son tInf et tSup et les nouvelles valeurs t
    def CyriusBeckAddLine(self, tInf, tSup, newSegment):
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
    def CyriusBeck(self, polygonNormalsList, polygonConvexList):

        '''for i in range (len(self.segmentList)):
            print(self.segmentList[i])
        print()
        print()
        print()
        for i in range(len(self.polygonConvex)):
            print(self.polygonConvex[i])
        '''
        newSegmentList = []
        newSegment = [0, 0]
        print("Nb segments to check : ", len(self.segmentList))
        for segment in self.segmentList:
            tInf = -np.exp(9)
            tSup = np.exp(9)
            for ind in range(len(polygonConvexList)):
                tInf, tSup = self.CyriusBeckBis(segment, polygonConvexList[ind], polygonNormalsList[ind], tInf, tSup)
            # ajouter a la nouvelle liste le nouveau segment ou pas
            resLine, newSegment = self.CyriusBeckAddLine(tInf, tSup, newSegment)
            if resLine:
                a = (self.EquationParametric(segment, newSegment[0]))
                b = (self.EquationParametric(segment, newSegment[1]))
                newSegmentList.append(self.CreateSegment(a, b))
                # newSegmentList.append(segment)
        print("New segments : ", len(newSegmentList))
        return newSegmentList

    # cree un nombre n donne aleatoire de lignes
    def RandomLines(self, nbToCreate):
        for ind in range(nbToCreate):
            x1, x2, x3, x4 = rd.randint(0, 600, 4, dtype=int)
            # x3, x4 = rd.randint(301, 600, 2, dtype=int)
            seg = self.CreateSegment4(x1, x2, x3, x4)
            self.segmentList.append(seg)

    # renvoie true si il y a une intesection entre deux lignes, et le point d intersection
    def LinesIntersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])  # ax-bx,cx-dx
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return False, [0, 0]
        # raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return True, [x, y]

    # renvoie true si il y a une intesection entre 4 pts, et le point d intersection
    def LinesIntersectionFromPoints(self, A1, A2, B1, B2):
        line1 = [A2[0] - A1[0]][A2[1] - A1[1]]
        line2 = [B2[0] - B1[0]][B2[1] - B1[1]]
        return self.LinesIntersection(line1, line2)

    # renvoie true si le point est visible par rapport au bord du polygon et sa normale
    def Visibility(self, ptBord, ptToLocate, NormalBord):
        norm = self.NewNormal(NormalBord)
        mySeg = self.CreateSegment(ptBord, ptToLocate)
        mySeg = self.NewNormal(mySeg)
        myMax = np.max(abs(mySeg))
        mySeg = np.array([mySeg[0] / myMax, mySeg[1] / myMax])
        dot = np.dot(norm, mySeg)
        if dot > 0:
            print("point à droite")
        if dot < 0:
            print("point a gauche")
        else:
            print("point sur l intersection")

    # Algo de Hodgman pour afficher l intersection de la figure avec le polygon
    # PLsommets : liste de N1 sommets (Entrée)
    # PWsommets : liste de N3 sommets, avec F1 = FN3 (Entrée)
    def Hodgman(self, PLsommets, PWsommets, myNormals):
        for i in range(len(PWsommets) - 1):
            N2 = 0
            PS = []
            S = PLsommets[i]
            for j in range(len(PLsommets)):
                if j == 0:
                    F = PLsommets[j]
                else:
                    isTrue, coord = self.LinesIntersectionFromPoints(S, PLsommets[j], PWsommets[i], PWsommets[i + 1])
                    if isTrue:
                        PS.append(coord)
                        N2 += 1
                S = PLsommets[j]
                if self.Visibility(PWsommets[i], S, myNormals[i]):
                    PS.append(S)
                    N2 += 1
            if N2 > 0:
                isTrue, coord = self.LinesIntersectionFromPoints(S, PLsommets[j], PWsommets[i], PWsommets[i + 1])
                if isTrue:
                    PS.append(coord)
                    N2 += 1
                PLsommets = PS
        return PS

# classe qui gere l affichage
class Paint(object):
    mainClass = MainClass()
    DEFAULT_PEN_SIZE = 1.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.click_number = 0
        self.coordinates = []  # coordonnÃ©es des sommets d'un polygon
        self.root = Tk()
        self.m = Menu(self.root, tearoff=0)
        self.m.add_command(label="Draw", command=self.draw)
        self.m.add_command(label="Eraser", command=self.eraser)
        self.m.add_separator()
        self.m.add_command(label="CyriusBeck", command=self.CyriusBeckLauch)
        self.m.add_command(label="Fill", command=self.RemplissageLCA)
        self.m.add_command(label="Clear", command=self.clear)
        self.m.add_command(label="Color", command=self.colorSelector)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=0)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()

        # self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.draw
        self.c.bind('<Button-1>', self.paint)
        self.root.bind("<Button-3>", self.do_popup)

    def draw(self):
        self.c.unbind('<B1-Motion>')
        self.c.bind('<Button-1>', self.paint)
        self.eraser_on = False

    def colorSelector(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def eraser(self):
        self.c.unbind('<Button-1>')
        self.c.bind('<B1-Motion>', self.paint)
        self.eraser_on = True

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def clear(self):
        self.c.delete("all")
        # segmentList.clear()   # la list des segments hors polygon convex
        # polygonConvex.clear()   # la list des cotes du polygon convex
        # polygonNormals.clear()

    def drawLine(self, x, y, z, a):
        self.c.create_line(x, y, z, a)

    def drawLine(self, line):
        x, y = line[0][:]
        z, a = line[1][:]
        self.c.create_line(x, y, z, a)

    def do_popup(self, event, mainClass=mainClass):
        self.click_number = 0
        self.line_width = self.choose_size_button.get()
        paint_color = self.color
        self.c.create_line(x1, y1, first_x, first_y,
                           width=self.line_width, fill=paint_color,
                           capstyle=ROUND, smooth=TRUE, splinesteps=36)
        seg = mainClass.CreateSegment4(x1, y1, first_x, first_y)
        mainClass.polygonConvex.append(seg)
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    """
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
    """

    def paint(self, event, mainClass=mainClass):
        self.line_width = self.choose_size_button.get()
        if not self.eraser_on:
            global x1, y1
            global x2, y2
            global first_x, first_y
            if self.click_number == 0:
                x1 = event.x
                y1 = event.y
                first_x = x1
                first_y = y1
                self.click_number = 1
            else:
                x2 = event.x
                y2 = event.y
                paint_color = self.color
                self.c.create_line(x1, y1, x2, y2,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
                seg = mainClass.CreateSegment4(x1, y1, x2, y2)
                mainClass.polygonConvex.append(seg)

                x1 = event.x
                y1 = event.y
        else:
            paint_color = 'white'
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def CyriusBeckLauch(self, mainClass=mainClass):
        mainClass.RandomLines(10)
        # self.DrawAllLines(mainClass.segmentList)
        mainClass.polygonNormals = mainClass.CalculateNormals(mainClass.polygonConvex)
        mainClass.segmentList = mainClass.CyriusBeck(mainClass.polygonNormals, mainClass.polygonConvex)
        self.clear()
        self.DrawPolygon(mainClass.polygonConvex)
        self.DrawAllLines(mainClass.segmentList)

    def DrawAllLines(self, segmentsList):
        for seg in segmentsList:
            self.drawLine(seg)

    # dessine toutes les cotes d un polygone array
    def DrawPolygon(self, listSegments):
        for ind in range(len(listSegments)):
            self.drawLine(listSegments[ind])

    def RemplissageLCA(self):
        startXStracage = 0
        startYStracage = 0

        for i in range(delimitationRec()[0], delimitationRec()[1]):
            inside = False
            exiting = False
            for j in range(delimitationRec()[2], delimitationRec()[3]):
                if isOnthePoly(i, j):
                    print(inside)
                    print(exiting)

                    if not inside:
                        inside = True
                    else:
                        inside = False

                    if not inside and exiting:
                        self.c.create_line(startXStracage, startYStracage, i, j)
                        exiting = False

                    elif inside and not exiting:
                        startXStracage = j
                        startYStracage = i
                        exiting = True

    # ====================================================================================
    # ====================================================================================
    # ====================================================================================


def delimitationRec(mainClass=Paint.mainClass):
    polygonConvex = mainClass.polygonConvex
    maxx = 0
    maxy = 0
    minx = 10000
    miny = 10000
    for i in range(len(polygonConvex)):
        for j in range(len(polygonConvex[i])):
            if polygonConvex[i][j][0] > maxx:
                maxx = polygonConvex[i][j][0]
            if polygonConvex[i][j][1] > maxy:
                maxy = polygonConvex[i][j][1]
            if polygonConvex[i][j][0] < minx:
                minx = polygonConvex[i][j][0]
            if polygonConvex[i][j][1] < miny:
                miny = polygonConvex[i][j][1]
    return minx, maxx, miny, maxy


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def isOnthePoly(px, py, mainClass=Paint.mainClass):
    polygonConvex = mainClass.polygonConvex
    for n in range(len(myPaint.mainClass.polygonConvex)):
        if distance(polygonConvex[n][0][0], polygonConvex[n][0][1], px, py) + distance(polygonConvex[n][1][0],
                                                                                       polygonConvex[n][1][1], px,
                                                                                       py) == distance(
            polygonConvex[n][0][0], polygonConvex[n][0][1], polygonConvex[n][1][0], polygonConvex[n][1][1]):
            print("yup")
            return True
        else:
            return False

    # ====================================================================================
    # ====================================================================================
    # ====================================================================================


myPaint = Paint()

if __name__ == '__main__':
    # myPaint = Paint()
    myPaint.root.mainloop()

    """
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
    """
