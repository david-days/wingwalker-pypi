import shapely.geometry

from wingwalker.models.enums import WingType, Planform
from wingwalker.models.full_wing import FullWing
from wingwalker.models.wing_section import WingSection


class SectionedWing(FullWing):
    """
    Class respresenting a full wing, but made up of individual subsections for printing/modeling purposes
    """
    wing_sections: list[WingSection]

    def __init__(self, wing_sections: list[WingSection],
                 wing_type: WingType = WingType.UNDEFINED, planform: Planform = Planform.UNDEFINED):
        super().__init__([], wing_type, planform)
        self.wing_sections = wing_sections
