import unittest
from unittest import TestCase

from app.graph_generator import GraphGenerator


class TestGraph(TestCase):

    def test_kwargs(self):
        """
        Test exception for improper grpah type
        :return:
        """
        self.assertRaises(ValueError, lambda: GraphGenerator.graph_generate('AA'))

    def test_generation(self):
        """
        Test generation of different complex network graphs
        :return:
        """
        grph = GraphGenerator.graph_generate('ER', n_of_nodes=100, prob1=0.4)
        self.assertEqual(100, len(grph.G.nodes))
        self.assertLess(100, len(grph.G.edges))

        grph = GraphGenerator.graph_generate('WS', n_of_nodes=100, prob1=0.4, k=2)
        self.assertEqual(100, len(grph.G.nodes))
        self.assertLess(100, len(grph.G.edges))

        grph = GraphGenerator.graph_generate('SW', n_of_nodes=100, prob1=0.8, prob2=0.3, k=2)
        self.assertEqual(100, len(grph.G.nodes))
        self.assertLess(100, len(grph.G.edges))
