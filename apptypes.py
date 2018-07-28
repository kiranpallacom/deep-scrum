
from enum import IntEnum, unique

@unique
class Priority(IntEnum):
    LOW=1
    MEDIUM=2
    HIGH=3
    IMMEDIATE=4

@unique
class Points(IntEnum):
    XXS=1
    XS=2
    S=3
    M=5
    L=8
    XL=13
    XXL=21

@unique
class Status(IntEnum):
    OPEN=1
    PLANNED=2
    DONE=4
    IN_PROGRESS=3
    VOID=0