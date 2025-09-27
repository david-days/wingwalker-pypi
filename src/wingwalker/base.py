"""
Base classes for wingwalker
"""
from abc import ABC, abstractmethod


class Reader(ABC):
    xs, ys = [], []
    chord_len = 0
    airfoil_desig = 'airfoil'

    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def read(self, c_len: float = 1.0) -> (list[float], list[float], str):
        """
        Method for reading wingwalker data
        Args:
            self (Reader): This instance
            c_len (float): Length of chord (unitless)
        Returns:
            The coordinates in [x],[y] arrays and the airfoil designation read from the data (or 'airfoil' by default)
        """
        pass
