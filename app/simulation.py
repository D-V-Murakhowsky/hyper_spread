import pandas as pd
import numpy as np
import networkx as nx
from random import choice

from app.models import SimulationData


class Simulation:

    def __init__(self, graph: nx.Graph, sim_data: SimulationData):
        self.G = graph
        self.data = sim_data

    def run(self):
        # simulation DataFrame
        df = pd.DataFrame(index=self.G.nodes, columns=['t_inf', 't_sus'])
        pass