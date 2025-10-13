import math
from abc import ABC

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.iterators import ParamFunctor, SectionFunctor


class EllipticalFunctor(ParamFunctor):
    """
    Class to return values for an elliptical planform wing
    """

    def __init__(self, build_params: WingRequest):
        super().__init__(build_params)
        self.a_len: float = self.base_chord/2.0
        self.b_len: float = self.length
        self.alpha_chunk: float = math.pi/(2.0*(self.iterations - 1))

    def chord_func(self):
        """
        Returns chord function for elliptical planform
        Returns:
            lambda for chord(t) = t * math.cos(pi / (2.0 * (iterations - 1)))
        """
        return lambda t: 2.0 * self.a_len * math.cos(t*self.alpha_chunk)

    def twist_func(self):
        """
        return linear twist function from super class
        Returns:

        """
        return super().twist_func()

    def z_func(self):
        """
        Returns z function for elliptical planform
        Returns:
            lambda for z(t) = t * math.sin(pi / (2.0 * (iterations - 1)))
        """
        return lambda t: self.b_len * math.sin(t*self.alpha_chunk)

    def area_func(self):
        return lambda: math.pi*self.a_len*self.b_len


class EllipticalSectionFunctor(SectionFunctor):
    """
    Class to return values for an elliptical planform wing
    """

    def __init__(self, build_params: WingRequest, idx: int):
        super().__init__(build_params=build_params, idx=idx)
        self.a_len: float = self.base_chord/2.0
        self.b_len: float = self.length
        self.alpha_start: float = self.offsets[0] * math.pi/2.0
        alpha_end = self.offsets[1] * math.pi/2.0
        self.alpha_chunk: float = (alpha_end - self.alpha_start)/(self.iterations - 1)

    def chord_func(self):
        """
        Returns chord function for elliptical planform
        Returns:
            lambda for chord(t) = 2 * a_len * math.cos(alpha_start + (t * alpha_chunk))
        """
        return lambda t: 2.0 * self.a_len * math.cos(self.alpha_start + t*self.alpha_chunk)

    def twist_func(self):
        """
        return linear twist function from super class
        Returns:

        """
        return super().twist_func()

    def z_func(self):
        """
        Returns z function for elliptical planform
        Returns:
            lambda for z(t) = b_len * math.sin(alpha_start + t * alpha_chunk)
        """
        return lambda t: self.b_len * math.sin(self.alpha_start + t * self.alpha_chunk)

    def area_func(self):
        """
        Calculate area of elliptical wing chunk
        """
        return lambda: 2.0 * (self.iterations - 1) * self.alpha_chunk * self.a_len * self.b_len


    def calc_offsets(self) -> list[float]:
        """
        Use base implementation
        Returns:

        """
        return super().calc_offsets()


    def normalize_sections(self, section_vals: list[float]) -> list[float]:
        """
        Use base implementation
        Args:
            section_vals:

        Returns:

        """
        return super().normalize_sections(section_vals)