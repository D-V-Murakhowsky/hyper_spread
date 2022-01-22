from dataclasses import dataclass
from collections import namedtuple
from networkx import Graph


@dataclass
class GraphData:

    G: Graph = None
    number_of_nodes: int = 100
    graph_type: str = 'ER'
    p1: float = 0.3
    p2: float = 0
    k: int = 0
    metrics: namedtuple = None

    def __str__(self):
        return f'Graph type: {self.graph_type}, number of nodes: {self.number_of_nodes}'
