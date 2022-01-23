import pandas as pd
import numpy as np
import networkx as nx
from random import choice

from app.models import SimulationData, SimulationResult
from app.utils import Utils


class Simulation:

    def __init__(self, graph: nx.Graph, sim_data: SimulationData):
        self.G = graph
        self.data = sim_data
        self.stat = SimulationResult(self.G.nodes)

    def run(self):
        # simulation DataFrame
        df = pd.DataFrame(index=self.G.nodes, columns=['t_inf', 't_sus'])

        # initial infected
        initial_node = choice(list(self.G.nodes))
        df.at[initial_node, 't_inf'] = 1

        # main simulation loop
        for step in range(self.data.n_of_steps):

            # already infected
            infected = df.loc[~df.t_inf.isna()].index.tolist()
            df.loc[infected, 't_inf'] += 1

            # possible infection during the contacts
            for node in infected:
                neighbours = [item[1] for item in self.G.edges(node)]
                for neighbour in neighbours:
                    if Utils.prob_func(self.data.p_trans) == 1:
                        if (np.isnan(df.at[neighbour, 't_inf'])) and (np.isnan(df.at[neighbour, 't_sus'])):
                            df.at[neighbour, 't_inf'] = 1  # starts infections day counter
                            self.stat.n_of_infected[node] += 1  # writes infections stat

            # recovery
            df.loc[df.t_inf == self.data.t_rec]['t_sus'] = 0
            df.loc[df.t_inf == self.data.t_rec]['t_inf'] = np.nan

            # from sust state
            df.loc[df.t_sus == self.data.t_sus] = np.nan

        pass
