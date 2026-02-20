"""
MTConnect Relationship Models

Relationship and reference models representing connections between components,
data items, and assets in the MTConnect information model.

Reference: MTConnect Standard v2.6 - References and Relationships
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

from mtconnect.types.primitives import ID, UUID


class RelationshipType(Enum):
    """Types of relationships between DataItems"""
    LIMIT = "LIMIT"
    OBSERVATION = "OBSERVATION"
    SPECIFICATION_LIMIT = "SPECIFICATION_LIMIT"
    CONTROL_LIMIT = "CONTROL_LIMIT"
    ALARM_LIMIT = "ALARM_LIMIT"
    ATTACHMENT = "ATTACHMENT"


@dataclass
class ComponentRef:
    """
    Reference to a Component by ID or ID path.
    
    Provides a way to reference another Component in the device hierarchy,
    used for associations, compositions, and relationships.
    """
    id_ref: ID
    name: Optional[str] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.id_ref, str):
            self.id_ref = ID(self.id_ref)


@dataclass
class DataItemRef:
    """
    Reference to a DataItem by ID.
    
    Establishes relationships between DataItems, such as pairing a measured value
    with its specification limits, control limits, or alarm thresholds.
    """
    id_ref: ID
    name: Optional[str] = None
    relationship_type: Optional[RelationshipType] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.id_ref, str):
            self.id_ref = ID(self.id_ref)


@dataclass
class AssetRef:
    """
    Reference to an Asset by asset ID.
    
    Associates a Component or DataItem with an Asset, such as linking a Spindle
    component to the currently loaded CuttingTool asset.
    """
    asset_id: ID
    asset_type: Optional[str] = None
    device_uuid: Optional[UUID] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.asset_id, str):
            self.asset_id = ID(self.asset_id)
        
        if self.device_uuid and isinstance(self.device_uuid, str):
            self.device_uuid = UUID(self.device_uuid)


class CompositionType(Enum):
    """Types of composition relationships"""
    ACTUATOR = "ACTUATOR"
    AMPLIFIER = "AMPLIFIER"
    AXIS = "AXIS"
    BALLSCREW = "BALLSCREW"
    BELT = "BELT"
    BRAKE = "BRAKE"
    CHAIN = "CHAIN"
    CHUCK = "CHUCK"
    CIRCUIT = "CIRCUIT"
    COMPRESSOR = "COMPRESSOR"
    CONTROLLER = "CONTROLLER"
    COOLING_TOWER = "COOLING_TOWER"
    DEVICE = "DEVICE"
    ENCODER = "ENCODER"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    EXHAUST = "EXHAUST"
    EXPOSURE_UNIT = "EXPOSURE_UNIT"
    FEEDER = "FEEDER"
    FILTER = "FILTER"
    GALVANOMOTOR = "GALVANOMOTOR"
    HEATING = "HEATING"
    HOPPER = "HOPPER"
    HYDRAULIC = "HYDRAULIC"
    LINEAR = "LINEAR"
    LUBRICATION = "LUBRICATION"
    MATERIAL = "MATERIAL"
    MOTOR = "MOTOR"
    OIL = "OIL"
    PNEUMATIC = "PNEUMATIC"
    PROCESS = "PROCESS"
    PROTECTIVE = "PROTECTIVE"
    PUMP = "PUMP"
    PULLEY = "PULLEY"
    REEL = "REEL"
    ROTARY = "ROTARY"
    SENSOR_UNIT = "SENSOR_UNIT"
    SPINDLE = "SPINDLE"
    SPREADER = "SPREADER"
    STAGE = "STAGE"
    STORAGE = "STORAGE"
    STRUCTURE = "STRUCTURE"
    SWITCH = "SWITCH"
    TANK = "TANK"
    TENSIONER = "TENSIONER"
    TRANSFORMER = "TRANSFORMER"
    VACUUM = "VACUUM"
    VALVE = "VALVE"
    VISE = "VISE"
    WASTE = "WASTE"
    WATER = "WATER"
    WORK_ENVELOPE = "WORK_ENVELOPE"


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


@dataclass
class CoordinateSystem:
    """
    Coordinate system definition with origin and transformation.
    
    Defines the spatial reference frame for measurements, providing origin
    position and orientation relative to a parent coordinate system.
    
    Used to transform between machine coordinates, work coordinates, and
    fixture coordinates.
    """
    id: ID
    name: Optional[str] = None
    type: Optional[str] = None  # MACHINE, WORK, BASE, OBJECT, etc.
    parent_id_ref: Optional[ID] = None
    origin: Optional[List[float]] = None  # [x, y, z] offset
    transformation: Optional[List[List[float]]] = None  # 4x4 transformation matrix
    
    def __post_init__(self):
        """Validate coordinate system"""
        if isinstance(self.id, str):
            self.id = ID(self.id)
        
        if self.parent_id_ref and isinstance(self.parent_id_ref, str):
            self.parent_id_ref = ID(self.parent_id_ref)
        
        if self.origin and len(self.origin) != 3:
            raise ValueError(f"Origin must have 3 components [x,y,z], got {len(self.origin)}")
        
        if self.transformation:
            if len(self.transformation) != 4 or any(len(row) != 4 for row in self.transformation):
                raise ValueError("Transformation must be 4x4 matrix")


@dataclass
class SpecificationLimits:
    """
    Specification limits defining acceptable range for a measurement.
    
    Provides upper and lower specification limits that define the acceptable
    range for a measured value, typically used in quality control and
    inspection processes.
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    lower_limit: Optional[float] = None
    nominal: Optional[float] = None
    
    def is_within_spec(self, value: float) -> bool:
        """Check if a value is within specification limits"""
        if self.upper_limit is not None and value > self.upper_limit:
            return False
        if self.lower_limit is not None and value < self.lower_limit:
            return False
        return True
    
    def is_warning_range(self, value: float) -> bool:
        """Check if a value is in warning range but within spec"""
        if not self.is_within_spec(value):
            return False
        
        if self.upper_warning is not None and value > self.upper_warning:
            return True
        if self.lower_warning is not None and value < self.lower_warning:
            return True
        return False


@dataclass
class ControlLimits:
    """
    Statistical process control limits (UCL/LCL).
    
    Provides upper and lower control limits for statistical process control,
    representing the expected natural variation of a process. Values outside
    these limits may indicate the process is out of control.
    """
    upper_control_limit: Optional[float] = None
    upper_warning_limit: Optional[float] = None
    lower_warning_limit: Optional[float] = None
    lower_control_limit: Optional[float] = None
    
    def is_in_control(self, value: float) -> bool:
        """Check if a value indicates process is in control"""
        if self.upper_control_limit is not None and value > self.upper_control_limit:
            return False
        if self.lower_control_limit is not None and value < self.lower_control_limit:
            return False
        return True


@dataclass
class AlarmLimits:
    """
    Alarm threshold limits for triggering alerts.
    
    Defines upper and lower limits that trigger alarms when exceeded,
    used for equipment monitoring and fault detection.
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    lower_limit: Optional[float] = None
    
    def check_alarm(self, value: float) -> Optional[str]:
        """
        Check if value triggers an alarm.
        
        Returns:
            "UPPER_LIMIT", "UPPER_WARNING", "LOWER_WARNING", "LOWER_LIMIT", or None
        """
        if self.upper_limit is not None and value > self.upper_limit:
            return "UPPER_LIMIT"
        if self.upper_warning is not None and value > self.upper_warning:
            return "UPPER_WARNING"
        if self.lower_limit is not None and value < self.lower_limit:
            return "LOWER_LIMIT"
        if self.lower_warning is not None and value < self.lower_warning:
            return "LOWER_WARNING"
        return None
