"""
MTConnect Configuration Models

Configuration information for components including coordinate systems,
specifications, sensor configuration, motion parameters, and solid models.

Reference: MTConnect Standard v2.6 - Configuration
"""

from dataclasses import dataclass, field
from typing import Literal, Optional, List
from mtconnect.types.primitives import ID
from mtconnect.types.enums import CoordinateSystemTypeEnum


@dataclass
class CoordinateSystem:
    """
    Coordinate system definition with origin and transformation.
    
    Defines the spatial reference frame for measurements, providing origin
    position and orientation relative to a parent coordinate system.
    
    Used to transform between machine coordinates, work coordinates, and
    fixture coordinates.
    
    Reference: MTConnect Standard v2.6 - CoordinateSystem (lines 51774-51900 in model_2.6.xml)
    """
    id: ID
    name: Optional[str] = None
    type: Optional[CoordinateSystemTypeEnum] = None
    parent_id_ref: Optional[ID] = None
    origin: Optional[List[float]] = None  # [x, y, z] offset
    transformation: Optional[List[List[float]]] = None  # 4x4 transformation matrix
    native_name: Optional[str] = None
    description: Optional[str] = None
    
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
class ConfigSpecificationLimits:
    """
    Specification limits for Configuration context (design-time).
    
    Design-time specification limits that define acceptable ranges for
    measurements as part of equipment configuration.
    
    Distinct from SpecificationLimitsValue which represents runtime observation data.
    
    Reference: MTConnect Standard v2.6 - SpecificationLimits in Configuration (lines 52843+ in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    nominal: Optional[float] = None
    lower_limit: Optional[float] = None


@dataclass
class ConfigControlLimits:
    """
    Statistical process control limits for Configuration context (design-time).
    
    Design-time control limits for statistical process control representing
    expected natural variation as part of equipment configuration.
    
    Distinct from ControlLimitsValue which represents runtime observation data.
    
    Reference: MTConnect Standard v2.6 - ControlLimits in Configuration (lines 52761+ in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    nominal: Optional[float] = None
    lower_limit: Optional[float] = None


@dataclass
class ConfigAlarmLimits:
    """
    Alarm threshold limits for Configuration context (design-time).
    
    Design-time alarm limits that define thresholds for triggering alerts
    as part of equipment configuration.
    
    Distinct from AlarmLimitsValue which represents runtime observation data.
    
    Reference: MTConnect Standard v2.6 - AlarmLimits in Configuration (lines 52806+ in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    lower_limit: Optional[float] = None


@dataclass
class Specification:
    """
    Design characteristics for a piece of equipment or component.
    
    Defines nominal values, limits, and tolerances for physical or performance
    characteristics of equipment.
    
    Reference: MTConnect Standard v2.6 - Specification (_19_0_3_45f01b9_1580315898400_607214_47155)
    """
    id: Optional[ID] = None
    type: Optional[str] = None  # DataItem type (e.g., LENGTH, FORCE)
    sub_type: Optional[str] = None
    units: Optional[str] = None
    name: Optional[str] = None
    originator: str = "MANUFACTURER"  # MANUFACTURER or USER
    data_item_id_ref: Optional[ID] = None
    composition_id_ref: Optional[ID] = None
    coordinate_system_id_ref: Optional[ID] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    nominal: Optional[float] = None
    upper_limit: Optional[float] = None
    lower_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    # Associated configuration limits
    specification_limits: Optional[ConfigSpecificationLimits] = None
    control_limits: Optional[ConfigControlLimits] = None
    alarm_limits: Optional[ConfigAlarmLimits] = None


@dataclass
class SensorConfiguration:
    """
    Configuration for sensing elements and their calibration.
    
    Provides information about sensor characteristics, calibration,
    and channel configuration.
    
    Reference: MTConnect Standard v2.6 - SensorConfiguration
    """
    pass  # Placeholder for future implementation


@dataclass
class SolidModel:
    """
    3D geometry reference for the component.
    
    References to files with three-dimensional geometry of the Component
    or Composition.
    
    Reference: MTConnect Standard v2.6 - SolidModel
    """
    id: Optional[ID] = None
    solid_model_id_ref: Optional[ID] = None
    item_ref: Optional[str] = None
    href: Optional[str] = None
    media_type: Optional[str] = None
    coordinate_system_id_ref: Optional[ID] = None


@dataclass
class Motion:
    """
    Motion characteristics for moving components.
    
    Describes motion of a Component relative to a coordinate system.
    
    Reference: MTConnect Standard v2.6 - Motion
    """
    id: Optional[ID] = None
    type: Optional[str] = None  # PRISMATIC, REVOLUTE, CONTINUOUS, FIXED
    actuation: Optional[str] = None  # DIRECT, VIRTUAL, NONE
    coordinate_system_id_ref: Optional[ID] = None
    parent_id_ref: Optional[ID] = None
    origin: Optional[List[float]] = None
    axis: Optional[List[float]] = None


@dataclass
class ConfigurationRelationship:
    """
    Association between two pieces of equipment or assets that may function
    independently but together perform a manufacturing operation.
    
    Abstract base for configuration relationships (ComponentRelationship,
    DeviceRelationship, AssetRelationship). 
    
    Reference: MTConnect Standard v2.6 - ConfigurationRelationship
    """
    id: ID
    name: Optional[str] = None
    type: Literal['CHILD', 'PARENT']  # e.g., "MOUNTED_ON",
    criticality: Optional[str] = None  # e.g., "CRITICAL", "NON_CRITICAL"


@dataclass
class ImageFile:
    """
    Image file reference for component visualization.
    
    Reference to an image file for visual representation of a Component.
    
    Reference: MTConnect Standard v2.6 - ImageFile
    """
    id: Optional[ID] = None
    href: Optional[str] = None
    media_type: Optional[str] = None


@dataclass
class PowerSource:
    """
    Power source information for the component.
    
    Description of the power source associated with a Component.
    
    Reference: MTConnect Standard v2.6 - PowerSource
    """
    pass  # Placeholder for future implementation


@dataclass
class Configuration:
    """
    Technical information about a Component describing its physical layout,
    functional characteristics, and relationships with other entities.
    
    Contains coordinate systems, specifications, sensor configuration, motion
    parameters, and other configuration details.
    
    Reference: MTConnect Standard v2.6 - Configuration (EAID_C04DCC77_16E8_4cef_92D4_B777AFC52570)
    """
    coordinate_systems: List[CoordinateSystem] = field(default_factory=list)
    specifications: List[Specification] = field(default_factory=list)
    sensor_configuration: Optional[SensorConfiguration] = None
    solid_model: Optional[SolidModel] = None
    motion: Optional[Motion] = None
    relationships: List[ConfigurationRelationship] = field(default_factory=list)
    image_files: List[ImageFile] = field(default_factory=list)
    power_sources: List[PowerSource] = field(default_factory=list)
