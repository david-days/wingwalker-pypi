from typing import Iterator

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.models.airfoil_section import AirfoilSection
from wingwalker.models.airfoil_specs import AirfoilSpecs
from wingwalker.models.enums import WingType, Planform


class WingModel:
    """
    Class representing a full "wing" (root to tip) in one complete listing of airfoil sections.

    Implements iterator functions
    """
    def __init__(self, wing_params: WingRequest, af_specs: AirfoilSpecs, airfoil_sections: list[AirfoilSection]):
        self.airfoil_sections = airfoil_sections
        self.af_specs = af_specs
        self.wing_params = wing_params
        self.base_chord: float = 0.0
        self.end_chord: float = 0.0
        self.span: float = 0.0
        self.area: float = 0.0
        self.notes: str = ''


    @property
    def mac(self)->float:
        return self.area / self.span if self.span != 0.0 else 0.0


    def __str__(self)->str:
        return f'Full Wing: {self.wing_type.name}, Planform: {self.planform.name}, {len(self.airfoil_sections)} sections'

    def __repr__(self)->str:
        r: str = 'Wing Model\n'
        r += '============================\n'
        r += f'Wing Type: {self.wing_params.wing_type}\n'
        r += f'Planform: {self.wing_params.planform}\n'
        r += f'Wing Span: {self.span}\n'
        r += f'Base Cord: {self.base_chord}\n'
        r += f'End Cord: {self.end_chord}\n'
        r += f'Area: {self.area}\n'
        r += f'MAC: {self.mac}\n'
        r += f'Washout: {self.wing_params.twist}\n'
        r += f'Iterations: {self.wing_params.iterations}\n'
        r += '\n'
        r += '----------------------------\n'
        r += 'Airfoil Specifications:\n'
        r += f'Airfoil Name: {self.af_specs.designation}\n'
        r += f'Airfoil Sections: {len(self.airfoil_sections)}\n'
        r += '----------------------------\n'
        r += f'Notes\n'
        r += f' {self.notes}'
        return r

    def __iter__(self)->Iterator[AirfoilSection]:
        self.idx = 0
        return self

    def __next__(self)->AirfoilSection:
        if self.idx >= len(self.airfoil_sections):
            raise StopIteration
        next_section = self.airfoil_sections[self.idx]
        self.idx += 1
        return next_section