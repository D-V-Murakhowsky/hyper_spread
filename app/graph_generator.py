import networkx as nx
import numpy as np
from random import choice, shuffle
from itertools import combinations
from random import randint
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

        self.n_of_nodes = n_of_nodes  # number of nodes in generating graph
        self.k = k                    # quantity of neighbours for a node. Should be even
        self.prob1 = prob1            # probability of short wire
        self.prob2 = prob2            # probability of long wire

        self.possible_edges = None
        self.G = nx.Graph()
        self.G.add_nodes_from(list(range(n_of_nodes)))

    @staticmethod
    def graph_generate(graph_type: Union[Literal['ER'], Literal['WS'], Literal['SW']],
                       n_of_nodes: int = 100, k: int = 0,
                       prob1: float = 0, prob2: float = 0) -> nx.Graph:
        """
        Main class fabric
        :param graph_type: defines the one of the possible graph types
        :param n_of_nodes: number of nodes in generating graph
        :param k: number of neighbours. Should be even.
        :param prob1: Probability of short wire
        :param prob2: Probability of long wire
        :return: networks graph
        """
        if graph_type not in ['ER', 'WS', 'SW']:
            raise ValueError('Improper graph type')

        if graph_type == 'ER':
            grph = GraphGenerator(n_of_nodes=n_of_nodes, prob1=prob1)
            grph.er_edges()
        elif graph_type == 'WS':
            grph = GraphGenerator(n_of_nodes=n_of_nodes, k=k, prob1=prob1)
            grph.ws_edges()
        elif graph_type == 'SW':
            grph = GraphGenerator(n_of_nodes=n_of_nodes, k=k, prob1=prob1, prob2=prob2)
            grph.sw_edges()

        return grph.G

    @staticmethod
    def prob_func(prob: float) -> np.array:
        """
        Choices vertexes to connect from a list
        :param prob: probability of wiring
        :return: chosen nodes
        """
        p = int(prob * 100)
        arr = np.zeros(100)
        arr[:p] = 1
        arr = list(arr)
        shuffle(arr)
        return choice(arr)

    @staticmethod
    def make_n_k(k: int) -> np.array:
        """
        Neighbours numbers
        :param k: number of node
        :return: number of neighbours
        """
        if k % 2 != 0:
            raise ValueError("k shouldn't be odd")

        n_k = np.array(list(range(k + 1)))
        return n_k - int(k / 2)

    def er_edges(self):
        """
        Generates Erdos - Renyi graph
        Mutates G params of the class
        :return: None
        """
        self.possible_edges = combinations(list(self.G.nodes), 2)
        edge_list = []
        for edge in self.possible_edges:
            if self.prob_func(self.prob1) == 1:
                edge_list.append(edge)
        self.G.add_edges_from(edge_list)

    def ws_edges(self):
        """
        Generates Watts - Strogatz graph
        Mutates G params of the class
        :return: None
        """
        # neighbours
        n_k = self.make_n_k(self.k)

        # initial wiring
        near_edges = []
        for node in list(self.G.nodes):
            neighbours = n_k + node
            for one in neighbours:
                if one != node:
                    if one < 0:
                        one += self.n_of_nodes
                    elif one > self.n_of_nodes - 1:
                        one -= self.n_of_nodes
                near_edges.append((node, one))

        # rewiring
        final_edges = []
        for edge in near_edges:
            if self.prob_func(self.prob1) == 1:
                # make rewiring
                node = edge[0]
                node_left = node + 1 if (node + 1) < self.n_of_nodes else (node + 1 - self.n_of_nodes)
                node_right = node - 1 if (node - 1) > -1 else (node - 1 + self.n_of_nodes)
                while (new_node := randint(0, self.n_of_nodes)) in [node_right, node, node_left]:
                    pass
                final_edges.append((edge[0], new_node))
            else:
                final_edges.append((edge[0], edge[1]))
        self.G.add_edges_from(final_edges)

    def sw_edges(self):
        """
        Generates Song - Wang graph
        Mutates G params of the class
        :return: None
        """
        n_k = self.make_n_k(self.k)

        # wiring
        near_edges = []
        far_edges = []
        for node in list(self.G.nodes):
            neighbours = n_k + node
            # short distance
            for one in neighbours:
                if self.prob_func(self.prob1) == 1:
                    if one != node:
                        if one < 0:
                            one += self.n_of_nodes
                        elif one > self.n_of_nodes - 1:
                            one -= self.n_of_nodes
                    near_edges.append((node, one))

            # long distance
            not_neighbours = [node for node in list(self.G.nodes) if node not in neighbours]
            for one in not_neighbours:
                if self.prob_func(self.prob2) == 1:
                    if one < 0:
                        one += self.n_of_nodes
                    elif one > self.n_of_nodes - 1:
                        one -= self.n_of_nodes
                    far_edges.append((node, one))

        self.G.add_edges_from(near_edges)
        self.G.add_edges_from(far_edges)


