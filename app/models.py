from dataclasses import dataclass, asdict
from networkx import Graph
import pandas as pd
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
class SimulationData:

    p_trans: float = 0.2     # transition probability
    t_rec: int = 14          # recovery time
    t_sus: int = 90         # sustainable time
    n_of_steps: int = 20    # number of simulation steps
    iter: int = 1            # number of iterations (simulations)


@dataclass
class SimulationResult:

    comparison: pd.DataFrame

    @property
    def sorted_data(self):
        return self.comparison.sort_values(['n_infected', 'n_connections'], ascending=False)

    @property
    def sort_by_connections(self):
        return self.comparison.sort_values(['n_connections', 'n_infected'], ascending=False)

    def __init__(self, nodes):
        self.comparison = pd.DataFrame(index=nodes, columns=['n_connections', 'n_infected'])


@dataclass
class MeasuredGraph:

    G: Graph = Graph()
    metrics: Metrics = Metrics(0, 0)


