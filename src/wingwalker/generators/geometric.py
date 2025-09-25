from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.iterators import ParamFunctor


class GeometricFunctor(ParamFunctor):
    """
    Class for geometric wing shapes (semi-rectangular -> trapezoid -> triangular)
    """

    def __init__(self, build_params: WingRequest):
        super().__init__(build_params)

    def chord_func(self):
        """
        Lambda function for linear change from base_chord to end_chord
        Returns:
            lambda function chord(t) = base_chord - (t * (base_chord - end_chord)/(iterations - 1))
        """
        chord_step = (self.base_chord - self.end_chord) / (self.iterations - 1)
        return lambda t: self.base_chord - (t * chord_step)

    def twist_func(self):
        return super().twist_func()

    def z_func(self):
        """
        Z function for rectangular wings: z(t) as uniform pieces of the length of the wing
        Returns:
            lambda function z(t) = t * (length/(iterations - 1))
        """
        l_step = self.length / (self.iterations - 1)
        return lambda t: t * l_step

    def area_func(self):
        return lambda: (self.base_chord + self.end_chord) * self.length / 2.0