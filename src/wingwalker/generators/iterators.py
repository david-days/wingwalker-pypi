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



class SectionFunctor(ParamFunctor):
    @abstractmethod
    def __init__(self, build_params: WingRequest, idx: int):
        super().__init__(build_params)
        self.sections = self.normalize_sections(build_params.sections)
        self.idx = idx
        self.offsets = self.calc_offsets()

    @abstractmethod
    def normalize_sections(self, section_vals: list[float]) -> list[float]:
        """
        Returns a normalized list of the section values (fractions of the whole on a unit scale)
        Args:
            section_vals: Original values

        Returns:
            Normalized list (array) of the values in the sections
        """
        total = sum(section_vals)
        return [v/total for v in section_vals]

    @abstractmethod
    def calc_offsets(self)->list[float]:
        """
        Calculates the start and end offsets (0.0->1.0) of the current section
        Returns:
            Array holding the starting and ending offset of this section
        """
        if self.idx == 0:
            # Degenerate case of no offset
            return [0.0, self.sections[0]]
        if self.idx == len(self.sections)-1:
            prev_offsets = 1.0 - self.sections[self.idx]
            return [prev_offsets, 1.0]
        offset: float = 0.0
        for idx, sect in enumerate(self.sections):
            offset += sect if idx < self.idx else 0.0
        return [offset, offset + self.sections[self.idx]]

    @abstractmethod
    def chord_func(self):
        """
        method to return a lambda calculating chord(t)

        Returns:
            lambda function calculating chord(t) length for the subsection.  Default is to return
            the base_cord (square wing)
        """
        return lambda x: self.base_chord

    @abstractmethod
    def twist_func(self):
        """
        Chord function for a constant progressive twist along the length of the wing
        twist(t), for this subsection.
        Returns:
            lambda function theta(t) = t * (twist/(iterations - 1))
        """
        twist_dir = -1.0 if self.mirrored else 1.0
        twist_start = self.offsets[0] * twist_dir * self.twist
        twist_end = self.offsets[1] * twist_dir * self.twist
        twist_chunk = (twist_end - twist_start)/(self.iterations - 1)
        return lambda t: twist_start + (t * twist_chunk)

    @abstractmethod
    def z_func(self):
        """
        method to return a lambda calculating z(t)
        Returns:
            lambda function calculating z(t).  Default is to return equal sections
            of length/(iterations - 1)
        """
        z_start = self.offsets[0] * self.length
        z_end = self.offsets[1] * self.length
        l_section = (z_end - z_start) / (self.iterations - 1)
        return lambda t: z_start + (t * l_section)

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
