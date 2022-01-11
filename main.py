def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

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

        self.root.mainloop()

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

#Create a point using 2 coords
def CreatePoint(x1, y1):
    return np.array([x1, y1])

#Create a segment using 4 coords
def CreateSegment(x1, y1, x2, y2):
    return np.array([x1, y1], [x2, y2])

#Create a segment using 2 points
def CreateSegment(p1, p2):
    #return CreateSegment(p1[0], p1[1], p2[0], p2[1])
    return np.array([ [p1[0], p1[1]],
                      [p2[0], p2[1]]
                      ])

#Create a polygone using a list of points (points du tk avec dernier element identique au premier)
def CreatePolygone(pointList):
    long = pointList.size
    if long == 0:
        return np.zeros(1)
    res = np.zeros((2, long))
    for i in range(0, long, 2):
        res[i][0] = pointList[i]
        res[i][1] = pointList[i+1]

def line_intersection(line1, line2, i):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]) #ax-bx,cx-dx
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False
       #raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    i[0] = x
    i[1] = y
    return True


if __name__ == '__main__':
    a = CreateSegment(CreatePoint(0.0, 0.0), CreatePoint(3.0, 3.0))
    b = CreateSegment(CreatePoint(1.0, 1.0), CreatePoint(1.0, 3.0))
    i = np.array([0,0])
    res = line_intersection(a, b, i)
    print(res)
    #Paint()