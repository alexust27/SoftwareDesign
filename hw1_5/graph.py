from abc import abstractmethod
import numpy as np


class Graph:
    def __init__(self, drawing_api):
        self._drawing_api = drawing_api
        self.center_x = self._drawing_api.get_drawing_area_width() / 2
        self.center_y = self._drawing_api.get_drawing_area_height() / 2

    @abstractmethod
    def draw_graph(self):
        pass


class GraphMatrix(Graph):
    def __init__(self, drawing_api, n_vertex=10):
        super().__init__(drawing_api)
        if n_vertex <= 0:
            raise ValueError('Кол-во вершин должно быть больше 0')
        self.__n_vertex = n_vertex
        self.__alfa = 2 * np.pi / n_vertex
        self.matrix = np.zeros((self.__n_vertex, self.__n_vertex), bool)
        for i in range(self.__n_vertex):
            self.matrix[i][i - 1] = True

    def __get_x_y(self, vertex, radius=100):
        x = radius * np.cos(vertex * self.__alfa) + self.center_x
        y = radius * np.sin(vertex * self.__alfa) + self.center_y
        return x, y

    def draw_graph(self):
        for v in range(self.__n_vertex):
            x, y = self.__get_x_y(v)
            self._drawing_api.draw_circle(x, y)
            for u in range(self.__n_vertex):
                if self.matrix[v][u]:
                    x2, y2 = self.__get_x_y(u)
                    self._drawing_api.draw_line([x, x2], [y, y2])
        self._drawing_api.show()


class GraphList(Graph):
    def __init__(self, drawing_api, n_vertex=10):
        super().__init__(drawing_api)
        if n_vertex <= 0:
            raise ValueError('Кол-во вершин должно быть больше 0')
        self.__n_vertex = n_vertex
        self.__alfa = 2 * np.pi / n_vertex
        self.edges = [(i, (i + 1) % self.__n_vertex) for i in range(self.__n_vertex)]

    def __get_x_y(self, vertex, radius=100):
        x = radius * np.cos(vertex * self.__alfa) + self.center_x
        y = radius * np.sin(vertex * self.__alfa) + self.center_y
        return x, y

    def draw_graph(self):
        for (v, u) in self.edges:
            x, y = self.__get_x_y(v)
            self._drawing_api.draw_circle(x, y)
            x2, y2 = self.__get_x_y(u)
            self._drawing_api.draw_circle(x, y)
            self._drawing_api.draw_line([x, x2], [y, y2])
        self._drawing_api.show()
