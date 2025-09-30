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

    def __str__(self):
        members = [member.name for member in self]
        return ",".join(members) if members else "Undefined"



class Planform(str,Enum):
    UNDEFINED = "undefined"
    RECTANGULAR = "rectangular"
    ELLIPSE = "ellipse"
    GEOMETRIC = "geometric"

class SpecFormat(str, Enum):
    UNDEFINED = "undefined"
    SELIG = "selig"
    LEDNICER = "lednicer"