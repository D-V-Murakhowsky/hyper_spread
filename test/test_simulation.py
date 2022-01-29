import unittest
from unittest import TestCase

import pathlib
import networkx as nx

from app.simulation import Simulation,SimulateMany
from app.models import SimulationData


class TestSimulation(TestCase):

    def setUp(self) -> None:
        path = pathlib.Path(__file__).parents[1].resolve() / 'assets/graph_1.pickle'
        self.G = nx.readwrite.read_gpickle(path)
        self.data = SimulationData()

    def test_one_simulation(self):
        sm = Simulation(self.G, self.data)
        result = sm.run().sorted_data
        pass

    def test_multi_simulation(self):
        self.data.iter = 2
        sm_many = SimulateMany(self.G, self.data)
        result = sm_many.run_simulations()
        pass