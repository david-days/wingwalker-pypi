from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.iterators import ParamFunctor, SectionFunctor


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

class RectangularSectionFunctor(SectionFunctor):
    """
    Class to calculate and return values for a rectangular wing's subsections
    """

    def __init__(self, build_params: WingRequest, idx: int):
        super().__init__(build_params=build_params, idx=idx)
        self.offset = self.offsets[0] * self.length
        self.end_z = self.offsets[1] * self.length
        self.l_chunk = (self.end_z - self.offset)/ (self.iterations - 1)


    def chord_func(self):
        """
        Constant value for the chord across all values of t
        Returns:
            the required chord
        """
        chord = self.base_chord
        return lambda t: chord

    def twist_func(self):
        """
        Linear twist function from the base class
        Returns:
        """
        return super().twist_func()

    def z_func(self):
        """
        Returns the z function for the subsection
        Returns:
            lambda for function z(t) = offset + (t * length_chunk)
        """
        return lambda t: self.offset + (t * self.l_chunk)

    def area_func(self):
        """
        Returns a calculation of the area for this section
        Returns:

        """
        return lambda: (self.end_z - self.offset) * self.base_chord

    def calc_offsets(self) ->list[float]:
        return super().calc_offsets()

    def normalize_sections(self, section_vals: list[float]) -> list[float]:
        return super().normalize_sections(section_vals)

