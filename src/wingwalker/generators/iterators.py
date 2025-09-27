from abc import ABC, abstractmethod

from wingwalker.build_params.wing_request import WingRequest


class ParamFunctor(ABC):
    @abstractmethod
    def __init__(self, build_params: WingRequest):
        self.build_params = build_params
        self.twist = build_params.twist
        self.mirrored = build_params.mirrored
        self.base_chord = build_params.base_chord
        self.end_chord = build_params.end_chord
        self.length = build_params.span
        self.twist = build_params.twist
        self.iterations = build_params.iterations

    @abstractmethod
    def chord_func(self):
        """
        method to return a lambda calculating chord(t)

        Returns:
            lambda function calculating chord(t) length.  Default is to return
            the base_cord (square wing)
        """
        return lambda x: self.base_chord

    @abstractmethod
    def twist_func(self):
        """
        Chord function for a constant progressive twist along the length of the wing
        twist(t)
        Returns:
            lambda function theta(t) = t * (twist/(iterations - 1))
        """
        twist_dir = -1.0 if self.mirrored else 1.0
        twist_chunk = twist_dir * self.twist/(self.iterations - 1)
        return lambda t: t * twist_chunk

    @abstractmethod
    def z_func(self):
        """
        method to return a lambda calculating z(t)
        Returns:
            lambda function calculating z(t).  Default is to return equal sections
            of length/(iterations - 1)
        """
        l_section = self.length / (self.iterations - 1)
        return lambda t: t * l_section

    @abstractmethod
    def area_func(self):
        """
        Method to return area() of the wing
        Returns:
            lambda function generating the area
        """
        return lambda: self.base_chord * self.length

class TIterator:
    """
    Iterator for values of (t) as inputs for the lambda functions
    """
    def __init__(self, build_params: WingRequest):
        self.iterations = build_params.iterations

    def __iter__(self):
        self.t = 0
        return self

    def __next__(self):
        if self.t >= self.iterations:
            raise StopIteration
        current_t = self.t
        self.t += 1
        return current_t
