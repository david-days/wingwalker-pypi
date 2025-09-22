from typing import Iterator

import shapely.geometry

from wingwalker.models.enums import WingType, Planform
from wingwalker.models.full_wing import FullWing
from wingwalker.models.wing_section import WingSection


class SectionedWing(FullWing):
    """
    Class representing a full wing, but made up of individual subsections for printing/modeling purposes

    Implements iterator functions to walk through wing sections
    """
    def __init__(self, wing_sections: list[WingSection],
                 wing_type: WingType = WingType.UNDEFINED,
                 planform: Planform = Planform.UNDEFINED):
        super().__init__([], wing_type, planform)
        self.wing_sections = wing_sections

    def __iter__(self)->Iterator[WingSection]:
        self.sect_idx = 0
        return self

    def __next__(self)->WingSection:
        if self.sect_idx >= len(self.wing_sections):
            raise StopIteration
        next_section = self.wing_sections[self.sect_idx]
        self.sect_idx += 1
        return next_section
