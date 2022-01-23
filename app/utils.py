from random import choice, shuffle
import numpy as np


class Utils:

    @staticmethod
    def prob_func(prob: float) -> np.array:
        """
        Choices vertexes to connect from a list
        :param prob: probability of wiring
        :return: chosen nodes
        """
        p = int(prob * 100)
        arr = np.zeros(100)
        arr[:p] = 1
        arr = list(arr)
        shuffle(arr)
        return choice(arr)