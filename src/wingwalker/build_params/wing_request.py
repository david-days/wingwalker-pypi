from wingwalker.models.enums import WingType, Planform, SpecFormat


class WingRequest(object):
    """
    Class representing the full request for generation of a wing
    """
    def __init__(self):
        self.name: str = ''
        self.notes: str = ''
        self.wing_type: WingType = WingType.UNDEFINED
        self.planform: Planform = Planform.UNDEFINED
        self.spec_file: str = ''
        self.spec_format: SpecFormat = SpecFormat.UNDEFINED
        self.base_chord: float = 0.0
        self.end_chord: float = 0.0
        self.span: float = 0.0
        self.twist: float = 0.0
        self.iterations: int = 10
        self.area: float = 0.0

    def __str__(self)->str:
        return f'{self.name}, {self.wing_type.name}, {self.planform}'

    def __repr__(self)->str:
        r: str = 'Wing Request Specifications\n'
        r += '============================\n'
        r += f'Name: {self.name}\n'
        r += f'Wing Type: {self.wing_type}\n'
        r += f'Planform: {self.planform}\n'
        r += f'Spec File: {self.spec_file}\n'
        r += f'Spec Format: {self.spec_format}\n'
        r += '\n'
        r += 'Dimensions\n'
        r += '----------------------------\n'
        r += f'Wing Span: {self.span}\n'
        r += f'Base Chord: {self.base_chord}\n'
        r += f'End Chord: {self.end_chord}\n'
        r += f'Washout: {self.twist}\n'
        r += f'Iterations: {self.iterations}\n'
        r += '----------------------------\n'
        r += f'Notes: {self.notes}\n'
        return r

    @property
    def mirrored(self)->bool:
        return self.wing_type & WingType.RIGHT == WingType.RIGHT