import networkx as nx
import numpy as np
from random import choice, shuffle
from itertools import combinations
from random import randint
from typing import Union, Literal
from networkx.algorithms.approximation.clustering_coefficient import average_clustering


from app.models import GraphData, MeasuredGraph
from app import Metrics


class GraphGenerator:

    def __init__(self, n_of_nodes: int = 100, k: int = 0, prob1: float = 0, prob2: float = 0):

        self.n_of_nodes = n_of_nodes  # number of nodes in generating graph
        self.k = k  # quantity of neighbours for a node. Should be even
        self.prob1 = prob1  # probability of short wire
        self.prob2 = prob2  # probability of long wire

        self.possible_edges = None
        self.G = nx.Graph()
        self.G.add_nodes_from(list(range(n_of_nodes)))

    @staticmethod
    def graph_generate(graph_data: GraphData) -> MeasuredGraph:
        """
        Main class fabric
        :param graph_data: dataclass GraphData instance
        :return: networks graph
        """
        if graph_data.graph_type not in ['ER', 'WS', 'SW']:
            raise ValueError('Improper graph type')

        grph = None
        if graph_data.graph_type == 'ER':
            grph = GraphGenerator(n_of_nodes=graph_data.n_of_nodes, prob1=graph_data.p1)
            grph.er_edges()
        elif graph_data.graph_type == 'WS':
            grph = GraphGenerator(n_of_nodes=graph_data.n_of_nodes, k=graph_data.k, prob1=graph_data.p1)
            grph.ws_edges()
        elif graph_data.graph_type == 'SW':
            grph = GraphGenerator(n_of_nodes=graph_data.n_of_nodes, k=graph_data.k,
                                  prob1=graph_data.p1, prob2=graph_data.p2)
            grph.sw_edges()

        return MeasuredGraph(G=grph.G,
                             parameters=graph_data,
                             metrics=Metrics(0, 0))

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

    def graph_metrics(self) -> Metrics:
        avg_ls = list(filter(lambda x: x > 0.5,
                             [nx.average_shortest_path_length(C) for C in (self.G.subgraph(c).copy()
                                                                           for c in nx.connected_components(self.G))]))
        avg_distance = np.mean(avg_ls)
        cl_koef = average_clustering(self.G, trials=10000)

        return Metrics(avg_distance, cl_koef)
