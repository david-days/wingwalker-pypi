from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.iterators import ParamFunctor


class RectangularFunctor(ParamFunctor):
    """
    Class to return values for a rectangular planform wing
    """
    def __init__(self, build_params: WingRequest):
        super().__init__(build_params)

    def chord_func(self):
        """
        Chord function for rectangular wings: chord(t) = base_chord
        Returns:
            base_chord for all values of t
        """
        chord = self.base_chord
        return lambda t: chord

    def twist_func(self):
        return super().twist_func()

    def z_func(self):
        """
        Z function for rectangular wings: z(t) as uniform pieces of the length of the wing
        Returns:
            lambda function z(t) = t * (length/(iterations - 1))
        """
        l_step = self.length/(self.iterations - 1)
        return lambda t: t * l_step

    def area_func(self):
        return super().area_func()