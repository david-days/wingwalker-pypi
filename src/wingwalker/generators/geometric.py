from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.iterators import ParamFunctor, SectionFunctor


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

class GeometricSectionFunctor(SectionFunctor):
    """
    Class that generates lambdas for geometric wing subsections
    """

    def __init__(self, build_params: WingRequest, idx: int):
        super().__init__(build_params=build_params, idx=idx)
        # Offsets for z
        self.offset_z = self.offsets[0] * self.length
        self.end_z = self.offsets[1] * self.length
        self.l_chunk = (self.end_z - self.offset_z) / (self.iterations - 1)
        # Offsets for chord
        chord_diff = (self.base_chord - self.end_chord)
        self.chord_start = self.base_chord - (self.offsets[0] * chord_diff)
        self.chord_end = self.base_chord - (self.offsets[1] * chord_diff)
        self.chord_chunk = (self.chord_start - self.chord_end) / (self.iterations - 1)


    def chord_func(self):
        """
        Calculate the chord at a given t for this subsection
        """
        return lambda t: self.chord_start - (t * self.chord_chunk)

    def  twist_func(self):
        """
        Use the linear twist lambda from the base class
        Returns:

        """
        return super().twist_func()

    def z_func(self):
        """
        Return the lambda to calculate the z(t) for this subsection
        Returns:

        """
        return lambda t: self.offset_z + (t * self.l_chunk)

    def area_func(self):
        """
        Calculate the area for the subsection
        Returns:

        """
        return lambda: (self.end_z - self.offset_z) * (self.chord_start + self.chord_end) / 2.0

    def calc_offsets(self):
        return super().calc_offsets()

    def normalize_sections(self, section_vals: list[float]) -> list[float]:
        return super().normalize_sections(section_vals)