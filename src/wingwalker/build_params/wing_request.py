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
        self.base_cord: float = 0.0
        self.end_cord: float = 0.0
        self.length: float = 0.0
        self.twist: float = 0.0
        self.sections: list[float] = [1.0]
        self.iterations: int = 10

    def __str__(self)->str:
        return f'{self.name}, {self.wing_type.name}, {self.planform}'

    def __repr__(self)->str:
        r: str = 'Wing Request Specifications'
        r += '============================'
        r += f'Name: {self.name}'
        r += f'Wing Type: {self.wing_type}'
        r += f'Planform: {self.planform}'
        r += f'Spec File: {self.spec_file}'
        r += f'Spec Format: {self.spec_format}'
        r += 'Dimensions'
        r += '----------------------------'
        r += f'Wing Length: {self.length}'
        r += f'Base Cord: {self.base_cord}'
        r += f'End Cord: {self.end_cord}'
        r += f'Washout: {self.twist}'
        r += f'Sections: {self.sections}'
        r += '----------------------------'
        r += f'Notes: {self.notes}'
        return r


    def describe(self)->None:
        """
        Prints out a text block with the request parameters in human-readable format.
        """

