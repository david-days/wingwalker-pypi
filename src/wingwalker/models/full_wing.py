import shapely.geometry

from wingwalker.models.airfoil_section import AirfoilSection
from wingwalker.models.enums import WingType, Planform


class FullWing:
    """
    Class respresenting a full "wing" (root to tip) in one complete listing of airfoil sections.
    """
    airfoil_sections: list[AirfoilSection]
    wing_type: WingType
    planform: Planform
    base_chord: float
    end_chord: float = 0.0
    length: float


    def __init__(self, airfoil_sections: list[AirfoilSection], wing_type: WingType=WingType.UNDEFINED, planform: Planform=Planform.UNDEFINED):
        self.airfoil_sections = airfoil_sections
        self.wing_type = wing_type
        self.planform = planform

