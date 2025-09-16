import shapely.geometry

from wingwalker.models.airfoil_section import AirfoilSection
from wingwalker.models.enums import WingType, Planform
from wingwalker.models.full_wing import FullWing


class WingSection(FullWing):
    """
    Class representing a portion of a wing (wing, elevator, rudder, canard, etc).

    The section represented here is intended to be joined with other WingSections to represent a full wing
    """

    def __init__(self, airfoil_sections: list[AirfoilSection], wing_type: WingType = WingType.UNDEFINED, planform: Planform = Planform.UNDEFINED):
        super().__init__(airfoil_sections, wing_type, planform)
