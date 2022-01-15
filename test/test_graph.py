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
        self.assertEqual(100, len(grph.nodes))
        self.assertLess(100, len(grph.edges))
