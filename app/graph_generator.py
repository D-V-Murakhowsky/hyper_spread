from PyQt5 import QtWidgets as qw
from app.gui.main_window import Ui_MainWindow
import sys
import networkx as nx
import numpy as np
from random import choice, shuffle
from itertools import combinations
from random import randint
from networkx.algorithms.approximation.clustering_coefficient import average_clustering
from typing import Union, Literal


options = {
    "node_color": "#A0CBE2",
    "width": 0.5,
    "with_labels": False,
    'node_size': 50,
    'alpha': 0.8,
    'edge_color': 'grey'
}


class GraphGenerator:

    def __init__(self, n_of_nodes: int = 100, k: int = 0, prob1: float = 0, prob2: float = 0):

        # mathematics init
        self.G = nx.Graph()
        self.G.add_nodes_from(list(range(n_of_nodes)))
        self.possible_edges = None
        self.k = k
        self.prob1 = prob1
        self.prob2 = prob2

    @staticmethod
    def graph_generate(graph_type: Union[Literal['ER'], Literal['WS'], Literal['SW']],
                       n_of_nodes: int = 100, k: int = 0, prob1: float = 0, prob2: float = 0):
        if graph_type not in ['ER', 'WS', 'SW']:
            raise ValueError('Improper graph type')

        if graph_type == 'ER':
            grph = GraphGenerator(n_of_nodes=n_of_nodes, prob1=prob1)
            grph.er_edges()
            return grph.G

    @staticmethod
    def prob_func(prob):
        p = int(prob * 100)
        arr = np.zeros(100)
        arr[:p] = 1
        arr = list(arr)
        shuffle(arr)
        return choice(arr)

    @staticmethod
    def make_n_k(k):
        if k % 2 != 0:
            raise ValueError("k shouldn't be odd")

        n_k = np.array(list(range(k + 1)))
        return n_k - int(k / 2)

    def er_edges(self):
        self.possible_edges = combinations(list(self.G.nodes), 2)
        edge_list = []
        for edge in self.possible_edges:
            if self.prob_func(self.prob1) == 1:
                edge_list.append(edge)
        self.G.add_edges_from(edge_list)

    def WS_edges(self):
        N = int(self.ui.spinBox.value())
        p = float(self.ui.prob1.text())

        # neighbours
        k = int(self.ui.k.text())
        n_k = self.make_n_k(k)

        # initial wiring
        near_edges = []
        for node in list(self.G.nodes):
            neighbours = n_k + node
            for one in neighbours:
                if one != node:
                    if one < 0:
                        one += N
                    elif one > N - 1:
                        one -= N
                near_edges.append((node, one))

        # rewiring
        final_edges = []
        for edge in near_edges:
            if self.prob_func(p) == 1:
                # make rewiring
                node = edge[0]
                node_left = node + 1 if (node + 1) < N else (node + 1 - N)
                node_right = node - 1 if (node - 1) > -1 else (node - 1 + N)
                while (new_node := randint(0, N)) in [node_right, node, node_left]:
                    pass
                final_edges.append((edge[0], new_node))
            else:
                final_edges.append((edge[0], edge[1]))
        self.G.add_edges_from(final_edges)

    def SW_edges(self):
        N = int(self.ui.spinBox.value())
        p1 = float(self.ui.prob1.text())
        p2 = float(self.ui.prob2.text())

        # neighbours
        k = int(self.ui.k.text())
        n_k = self.make_n_k(k)

        # wiring
        near_edges = []
        far_edges = []
        for node in list(self.G.nodes):
            neighbours = n_k + node
            # short distance
            for one in neighbours:
                if self.prob_func(p1) == 1:
                    if one != node:
                        if one < 0:
                            one += N
                        elif one > N - 1:
                            one -= N
                    near_edges.append((node, one))

            # long distance
            not_neighbours = [node for node in list(self.G.nodes) if node not in neighbours]
            for one in not_neighbours:
                if self.prob_func(p2) == 1:
                    if one < 0:
                        one += N
                    elif one > N - 1:
                        one -= N
                    far_edges.append((node, one))

        self.G.add_edges_from(near_edges)
        self.G.add_edges_from(far_edges)


