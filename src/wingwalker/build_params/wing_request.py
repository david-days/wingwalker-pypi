import json
import string

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
        self.sections: list[float] = []

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
        r += f'Sections: { self.sections}\n' if len(self.sections) > 0 else '\n'
        r += '----------------------------\n'
        r += f'Notes: {self.notes}\n'
        return r

    @property
    def mirrored(self)->bool:
        return self.wing_type & WingType.RIGHT == WingType.RIGHT

    @property
    def identifier(self)->str:
        name_str = self.name if self.name != '' else 'unk'
        type_str = self.wing_type.__str__().replace(',', '_')
        return f'{name_str}_{self.planform}_{type_str}'

    def __eq__(self, other)->bool:
        if not isinstance(other, WingRequest):
            raise NotImplementedError
        self_array = (
            self.name,
            self.wing_type,
            self.planform,
            self.spec_file,
            self.spec_format,
            self.base_chord,
            self.end_chord,
            self.span,
            self.twist,
            self.iterations,
            self.area
        )
        other_array = (
            other.name,
            other.wing_type,
            other.planform,
            other.spec_file,
            other.spec_format,
            other.base_chord,
            other.end_chord,
            other.span,
            other.twist,
            other.iterations,
            other.area
        )
        return self_array == other_array

    def to_json(self):
        out_dict = dict(self.__dict__)
        w_type: str = ''
        out_dict['wing_type'] = self.wing_type.__str__()
        return json.dumps(out_dict, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, json_str):
        req_dict: dict = json.loads(json_str)
        wtype_val: WingType = WingType.UNDEFINED
        if req_dict['wing_type'] is not None:
            for t in req_dict['wing_type'].split(','):
                for m in WingType.__members__:
                    if m.__eq__(t):
                        wtype_val = wtype_val | WingType.__members__[t]
        req_dict['wing_type'] = wtype_val
        req: WingRequest = WingRequest()
        req.__dict__ = req_dict
        return req