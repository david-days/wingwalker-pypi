from enum import IntFlag, Enum

class WingType(IntFlag):
    UNDEFINED = 0
    WING = 0x01
    STABILIZER = 0x02
    LEFT = 0x04
    RIGHT = 0x08
    VERTICAL = 0x10
    HORIZONTAL = 0x20
    ELEVATOR = STABILIZER | HORIZONTAL
    RUDDER = STABILIZER | VERTICAL


class Planform(Enum):
    UNDEFINED = 0
    RECTANGULAR = 1
    ELLIPSE = 2
    GEOMETRIC = 3

class SpecFormat(Enum):
    UNDEFINED = 0
    SELIG = 1
    LEDNICER = 2