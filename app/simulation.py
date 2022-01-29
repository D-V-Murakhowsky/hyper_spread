import pandas as pd
import numpy as np
import networkx as nx
from random import choice
import logging

from PyQt5.QtCore import pyqtSignal, QObject


from app.models import SimulationData, SimulationResult, GraphData
from app.utils import Utils


logger = logging.getLogger('main_logger')


class SimulationManager(QObject):
    """
    Uses to run multiply simulations using Simulation class for s single one
    """
    progress_updater = pyqtSignal(int)   # used for updating progress bar in the main window
    finished = pyqtSignal(pd.DataFrame)  # used on simulation finish

    def __init__(self, graph: nx.Graph, sim_data: SimulationData, current_value: int = 0) -> None:
        super().__init__()
        self.G = graph
        self.data = sim_data
        self.current_value = current_value

    def run(self):
        self.progress_updater.emit(self.current_value + 10)
        self.finished.emit(pd.DataFrame())
        pass


class SimulateMany:
    """
    Used to run multiply simulations
    For test purposes extracted from SimulationManager which emits signals
    """

    def __init__(self, graph: nx.Graph, sim_data: SimulationData) -> None:
        self.G = graph
        self.data = sim_data

    def run_simulations(self):
        results = [Simulation(graph=self.G, sim_data=self.data).run() for _ in range(self.data.iter)]
        pass


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
            logger.info(f'Step {step}')
            logger.info(f'Infected: {df.loc[~df.t_inf.isna()].shape[0]}')
            logger.info(f'Recovering: {df.loc[~df.t_sus.isna()].shape[0]}')

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
            logger.info(f'From infected to recovering: {df.loc[df.t_inf == self.data.t_rec].shape[0]}')
            df.loc[df.t_inf == self.data.t_rec, 't_sus'] = 0
            df.loc[df.t_inf == self.data.t_rec, 't_inf'] = np.nan

            # recovery from sustainable state
            logger.info(f'From sustainable to normal state {df.loc[df.t_sus == self.data.t_sus].shape[0]}')
            df.loc[df.t_sus == self.data.t_sus, 't_sus'] = np.nan

        n_of_connected_nodes = [len(self.G.edges(node)) for node in self.G.nodes]
        self.stat.comparison['n_connections'] = n_of_connected_nodes
        self.stat.comparison['n_infected'] = self.stat.n_of_infected

        return self.stat
