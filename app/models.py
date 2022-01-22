from dataclasses import dataclass, asdict
from networkx import Graph
from typing import Union, Literal

from app import Metrics


@dataclass
class GraphData:

    n_of_nodes: int = 70
    graph_type: Union[Literal['ER'], Literal['WS'], Literal['SW']] = 'ER'
    p1: float = 0.3
    p2: float = 0
    k: int = 0

    def __repr__(self):
        return f'Graph type: {self.graph_type}, number of nodes: {self.n_of_nodes}'

    def return_kwargs(self):
        return asdict(self)


@dataclass
class MeasuredGraph:

    G: Graph = Graph()
    parameters: GraphData = GraphData()
    metrics: Metrics = Metrics(0, 0)


