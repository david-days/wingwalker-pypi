import shapely.geometry
import shapely.ops

class AirfoilSection:
    """
    Single cross-section of a wing, holding assigned chord length, z-index, twist and coordinates of that
    particular section
    """
    coords: list[shapely.geometry.Point]
    chord: float
    z_index: float
    twist: float
    spec_name: str

    def __init__(self, coords: list[shapely.geometry.Point], chord: float, z_index: float, twist: float, spec_name: str = "Undefined"):
        self.coords = coords
        self.chord = chord
        self.z_index = z_index
        self.twist = twist
        self.spec_name = spec_name

    def centroid(self)->shapely.geometry.Point:
        poly = shapely.geometry.Polygon(self.coords)
        return poly.centroid