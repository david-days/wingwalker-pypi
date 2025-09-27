from collections.abc import Iterator

from shapely.geometry import Point

class AirfoilSection:
    """
    Single cross-section of a wing, holding assigned chord length, z-index, twist and coordinates of that
    particular section.

    Implements the iterator functions
    """
    def __init__(self, coords: list[Point], chord: float, z_index: float, twist: float, spec_name: str = "Undefined"):
        self.coords = coords
        self.chord = chord
        self.z_index = z_index
        self.twist = twist
        self.spec_name = spec_name

    def __str__(self)->str:
        return f'Airfoil: {self.spec_name}, chord: {self.chord}, z: {self.z_index}, twist: {self.twist}'

    def __iter__(self)->Iterator[Point]:
        self.idx = 0
        return self

    def __next__(self)->Point:
        if self.idx < len(self.coords):
            next_coord = self.coords[self.idx]
            self.idx += 1
            return next_coord
        else:
            raise StopIteration