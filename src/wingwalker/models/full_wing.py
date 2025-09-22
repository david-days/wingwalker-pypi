from typing import Iterator

import shapely.geometry

from wingwalker.models.airfoil_section import AirfoilSection
from wingwalker.models.enums import WingType, Planform


class FullWing:
    """
    Class representing a full "wing" (root to tip) in one complete listing of airfoil sections.

    Implements iterator functions
    """
    def __init__(self, airfoil_sections: list[AirfoilSection], wing_type: WingType=WingType.UNDEFINED, planform: Planform=Planform.UNDEFINED):
        self.airfoil_sections = airfoil_sections
        self.wing_type = wing_type
        self.planform = planform
        self.base_chord: float = 0.0
        self.end_chord: float = 0.0
        self.length: float = 0.0

    def __str__(self)->str:
        return f'Full Wing: {self.wing_type.name}, Planform: {self.planform.name}, {len(self.airfoil_sections)} sections'

    def __repr__(self)->str:
        return f'FullWing(airfoil_sections=[], wing_type={self.wing_type.name}, planform={self.planform.name})'

    def __iter__(self)->Iterator[AirfoilSection]:
        self.idx = 0
        return self

    def __next__(self)->AirfoilSection:
        if self.idx >= len(self.airfoil_sections):
            raise StopIteration
        next_section = self.airfoil_sections[self.idx]
        self.idx += 1
        return next_section