"""
MTConnect Interface Interaction Model Types

Interface types for device-to-device coordination (MTConnect Part 5.0).
Interfaces use a request/response pattern for coordinating actions between equipment.

Reference: MTConnect Standard v2.6 Normative Model - Interface Interaction Model
Package: Interface Interaction Model (line ~42336)
"""

from enum import Enum, auto


class InterfaceType(Enum):
    """Concrete Interface types for device-to-device coordination"""
    BAR_FEEDER = auto()  # Coordinates bar feeder operations pushing stock into equipment
    CHUCK = auto()  # Coordinates chuck operations for workpiece holding
    DOOR = auto()  # Coordinates door operations between equipment
    MATERIAL_HANDLER = auto()  # Coordinates material/tooling loading, unloading, inspection


class InterfaceEvent(Enum):
    """Interface event types from InterfaceEventEnum"""
    CLOSE_CHUCK = auto()  # operating state of the service to close a chuck.
    CLOSE_DOOR = auto()  # operating state of the service to close a door.
    INTERFACE_STATE = auto()  # operational state of an Interface.
    MATERIAL_CHANGE = auto()  # operating state of the service to change the type of material or product bein...
    MATERIAL_FEED = auto()  # operating state of the service to advance material or feed product to a piece...
    MATERIAL_LOAD = auto()  # operating state of the service to load a piece of material or product.
    MATERIAL_RETRACT = auto()  # operating state of the service to remove or retract material or product.
    MATERIAL_UNLOAD = auto()  # operating state of the service to unload a piece of material or product.
    OPEN_CHUCK = auto()  # operating state of the service to open a chuck.
    OPEN_DOOR = auto()  # operating state of the service to open a door.
    PART_CHANGE = auto()  # operating state of the service to change the part or product associated with ...


class InterfaceState(Enum):
    """Interface operational state values"""
    DISABLED = auto()  # Interface is currently not operational.
    ENABLED = auto()  # Interface is currently operational and performing as expected.


class InterfaceRequestResponseState(Enum):
    """
    State machine values for Interface request/response pattern.
    Flow: NOT_READY → READY → ACTIVE → COMPLETE (or FAIL)
    """
    NOT_READY = auto()  # Not prepared to perform service
    READY = auto()  # Ready to request or perform service
    ACTIVE = auto()  # Currently performing action
    COMPLETE = auto()  # Action finished successfully
    FAIL = auto()  # Failure occurred during action
