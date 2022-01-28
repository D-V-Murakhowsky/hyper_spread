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
    t_sus: int = 180         # sustainable time
    n_of_steps: int = 100    # number of simulation steps
    iter: int = 1            # number of iterations (simulations)


@dataclass
class SimulationResult:

    n_of_infected: pd.Series  # represents number of infected by each node
    nodes_state: pd.Series   # represents final states of nodes to mark infected nodes on the graph
    comparison: pd.DataFrame

    @property
    def sorted_data(self):
        return self.n_of_infected.sort_values(ascending=False),\
               self.comparison.sort_values(['n_infected', 'n_connections'], ascending=False)

    def __init__(self, nodes):
        self.n_of_infected = pd.Series(index=nodes)
        self.n_of_infected.fillna(0, inplace=True)
        self.nodes_state = pd.Series(nodes)
        self.nodes = False
        self.comparison = pd.DataFrame(index=nodes, columns=['n_connections', 'n_infected'])


@dataclass
class MeasuredGraph:

    G: Graph = Graph()
    metrics: Metrics = Metrics(0, 0)


