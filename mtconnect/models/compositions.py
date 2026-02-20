"""
MTConnect Composition Models

Composition relationships defining functional elements of Components.

Compositions represent sub-elements that make up a Component, such as the
motor, encoder, and amplifier that comprise a servo axis, or the individual
sensors that make up a sensor array.

Reference: MTConnect Standard v2.6 - Composition Elements
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto

from mtconnect.types.primitives import ID, UUID


class CompositionType(Enum):
    """Types of composition relationships"""
    ACTUATOR = auto()
    AMPLIFIER = auto()
    AXIS = auto()
    BALLSCREW = auto()
    BELT = auto()
    BRAKE = auto()
    CHAIN = auto()
    CHUCK = auto()
    CIRCUIT = auto()
    COMPRESSOR = auto()
    CONTROLLER = auto()
    COOLING_TOWER = auto()
    DEVICE = auto()
    ENCODER = auto()
    ENVIRONMENTAL = auto()
    EXHAUST = auto()
    EXPOSURE_UNIT = auto()
    FEEDER = auto()
    FILTER = auto()
    GALVANOMOTOR = auto()
    HEATING = auto()
    HOPPER = auto()
    HYDRAULIC = auto()
    LINEAR = auto()
    LUBRICATION = auto()
    MATERIAL = auto()
    MOTOR = auto()
    OIL = auto()
    PNEUMATIC = auto()
    PROCESS = auto()
    PROTECTIVE = auto()
    PUMP = auto()
    PULLEY = auto()
    REEL = auto()
    ROTARY = auto()
    SENSOR_UNIT = auto()
    SPINDLE = auto()
    SPREADER = auto()
    STAGE = auto()
    STORAGE = auto()
    STRUCTURE = auto()
    SWITCH = auto()
    TANK = auto()
    TENSIONER = auto()
    TRANSFORMER = auto()
    VACUUM = auto()
    VALVE = auto()
    VISE = auto()
    WASTE = auto()
    WATER = auto()
    WORK_ENVELOPE = auto()


@dataclass
class Composition:
    """
    Composition relationship defining a functional element of a Component.
    
    Compositions represent sub-elements that make up a Component, such as the
    motor, encoder, and amplifier that comprise a servo axis, or the individual
    sensors that make up a sensor array.
    
    Example:
        >>> motor_composition = Composition(
        ...     id="x_motor",
        ...     type=CompositionType.MOTOR,
        ...     name="X-Axis Motor"
        ... )
    """
    id: ID
    type: CompositionType
    name: Optional[str] = None
    uuid: Optional[UUID] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    station: Optional[str] = None
    
    def __post_init__(self):
        """Validate composition"""
        if isinstance(self.id, str):
            self.id = ID(self.id)
        
        if self.uuid and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)
