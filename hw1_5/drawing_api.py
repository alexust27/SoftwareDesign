import turtle
import matplotlib.pyplot as plt


class DrawingApi:
    def get_drawing_area_width(self):
        pass

    def get_drawing_area_height(self):
        pass

    def draw_circle(self, *args):
        pass

    def draw_line(self, *args):
        pass


class DrawingPlt(DrawingApi):
    def __init__(self, w=800, h=600):
        plt.axis('off')
        self.__width = w
        self.__height = h
        plt.ylim(0, self.__height)
        plt.xlim(0, self.__width)

    def get_drawing_area_width(self):
        return self.__width

    def get_drawing_area_height(self):
        return self.__height

    def draw_circle(self, xs, ys, radius=200):
        plt.scatter(x=xs, y=ys, s=radius, c='black')

    def draw_line(self, x, y):
        plt.plot(x, y, linewidth=3, color='black')

    def show(self):
        plt.show()


class DrawingTurtle(DrawingApi):
    def __init__(self, w=600, h=800):
        self.__height = h
        self.__width = w
        self.__t = turtle.Turtle()
        self.__t.screen.setup(width=w, height=h)
        self.__t.penup()
        self.__t.pensize(3)
        self.__t.setposition(0, 0)
        self.__t.speed(10)
        self.__offset = 300

    def get_drawing_area_width(self):
        return self.__width

    def get_drawing_area_height(self):
        return self.__height

    def draw_circle(self, x, y):
        self.__t.goto(x - self.__offset, y - self.__offset)
        self.__t.pendown()
        self.__t.dot(20)
        self.__t.penup()

    def draw_line(self, xs, ys):
        self.__t.goto(xs[0] - self.__offset, ys[0] - self.__offset)
        self.__t.pendown()
        self.__t.goto(xs[1] - self.__offset, ys[1] - self.__offset)
        self.__t.penup()

    def show(self):
        turtle.done()
