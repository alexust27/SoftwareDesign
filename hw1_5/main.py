#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
from drawing_api import DrawingApi, DrawingPlt, DrawingTurtle
from graph import GraphMatrix, GraphList


n_vertex = 10


def parse_args(args) -> (int, int):
    """
        Парсер аргументов
        :param   args: аргументы для парсера
        :type    args: list
        :rtype:  (int, int)
        :return: апи для рисования и способ задания
    """
    global n_vertex
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", help="api для рисования, вариант 1 - pyplot, 2 - turtle", type=int, required=True)
    parser.add_argument("--use", help="способ задания графа: list - через список ребер, matrix - через матрицу",
                        type=str, required=True)
    parser.add_argument("-v", help="кол-во вершин, по умолчанию 10", type=int, required=False)
    ns = parser.parse_args(args)
    use = ns.use
    if ns.v and ns.v > 0:
        n_vertex = ns.v
    draw_api = ns.api
    if draw_api != 1 and draw_api != 2:
        raise argparse.ArgumentError(None, "неизвестный api, поробуйте 1 или 2")
    if use != 'matrix' and use != 'list':
        raise argparse.ArgumentError(None, "неизвестный способ задания графа, попробуйте list или matrix")
    return draw_api, 1 if use == 'matrix' else 0


def main():
    try:
        api, is_matrix = parse_args(sys.argv[1:])
    except argparse.ArgumentError as ae:
        print('ERROR:', ae.args[0])
        return
    if api == 1:
        draw_api = DrawingPlt()
    else:
        draw_api = DrawingTurtle()
    if is_matrix:
        g = GraphMatrix(draw_api, n_vertex)
        g.draw_graph()
    else:
        g = GraphList(draw_api, n_vertex)
        g.draw_graph()


if __name__ == '__main__':
    main()
