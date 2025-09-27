from shapely.geometry import Point, LineString, Polygon

class AirfoilSpecs(object):
    """
    Class representing the parsed airfoil specifications.

    Include methods to generate shapely.geometry structures for further processing and
    design.
    """
    def __init__(self, src: str, designation: str=None, x: list[float]=None, y: list[float]=None):
        self.src = src
        self.designation = designation
        self.x = x
        self.y = y
        if self.x is None:
            self.x = []
        if self.y is None:
            self.y = []

    def __str__(self)->str:
        return f'Airfoil \'{self.designation}\', src={self.src}, # points={len(self.x)}'

    def __repr__(self)->str:
        return f'AirfoilSpecs(src={self.src})'

    def trace(self, c_len: float = 1.0, z: float = 0.0, mirror: bool = False):
        """
        Generator function for shapely Points.  If non-default values are given for c_len and z,  then the
        points are scaled and elevated along the z axis, accordingly

        Args:
            mirror:
            c_len: length of chord to which the points should be scaled.  Default is 1.0 (unit scaling)
            z: Position of the points along the 3d z-axis. Default is 0.0 (equivalent to 2D points)
            mirror: Generate mirror image about the X axis of the original spec
        Returns:
            yields shapely.geometry.Points in order
        """
        mirror_val = -1.0 if mirror else 1.0
        for i in range(0, len(self.x)):
            yield Point(self.x[i] * c_len, self.y[i] * c_len * mirror_val, z)

    def to_line(self, c_len: float = 1.0, z: float = 0.0, mirror: bool = False)->LineString:
        """
        Function to create a shapely.geometry.LineString instance representing a path
        around the airfoil surface.

        Args:
            c_len: length of chord to which the line should be scaled.  Default is 1.0 (unit scaling)
            z: Position of the line along the 3d z-axis. Default is 0.0 (equivalent to 2D line)
            mirror: Generate mirror image about the X axis of the original spec
        Returns:
            A shapely.geometry.LineString instance containing the ordered points
        """
        coords = []
        for p in self.trace(c_len, z, mirror):
            coords.append(p)
        return LineString(coords)

    def to_poly(self, c_len: float = 1.0, z: float = 0.0, mirror: bool = False)->Polygon:
        """
        Function to create a shapely.geometry.Polygon instance representing a face
        of the airfoil cross-section.

        Args:
            c_len: length of chord to which the line should be scaled.  Default is 1.0 (unit scaling)
            z: Position of the line along the 3d z-axis. Default is 0.0 (equivalent to 2D polygon)
            mirror: Generate mirror image about the X axis of the original spec
        Returns:
            A shapely.geometry.Polygon instance containing the ordered points
        """
        coords = []
        for p in self.trace(c_len, z, mirror):
            coords.append(p)
        return Polygon(coords)

    def centroid(self, c_len: float = 1.0, z: float = 0.0, mirror: bool = False)->Point:
        """
        Find the centroid of the airfoil trace.
        Args:
            c_len: length of the chord for this section
            z: Position of this section along the z-axies
            mirror: Generate mirror image about the X axis of the original spec

        Returns:
            shapely.geometry.Point for the centroid of the airfoil trace
        """
        return self.to_poly(c_len=c_len, z=z, mirror=mirror).centroid