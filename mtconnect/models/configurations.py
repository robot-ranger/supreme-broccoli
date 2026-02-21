"""
MTConnect Configuration Models

Configuration information for components including coordinate systems,
specifications, sensor configuration, motion parameters, and solid models.

Reference: MTConnect Standard v2.6 - Configuration Package
Auto-generated from: model_2.6.xml
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Union, TYPE_CHECKING

from mtconnect.types.primitives import ID, MTCFloat
from mtconnect.types.enums import (
    CoordinateSystemTypeEnum, MotionActuationTypeEnum, MotionTypeEnum,
    OriginatorEnum, UnitEnum, RelationshipTypeEnum, MediaTypeEnum
)
from mtconnect.types.subtype import DataItemSubType
from mtconnect.types.sample import SampleType
from mtconnect.types.event import EventType
from mtconnect.types.condition import ConditionType

if TYPE_CHECKING:
    from mtconnect.models.components import Description



@dataclass
class CoordinateSystem:
    """reference system that associates a unique set of n parameters with each point in an n-dimensional space. ISO 10303-218:2004"""
    id: ID  # unique identifier for the coordinate system.
    type: CoordinateSystemTypeEnum  # type of coordinate system.
    name: Optional[str] = None  # name of the coordinate system.
    native_name: Optional[str] = None  # manufacturer's name or users name for the coordinate system.
    parent_id_ref: Optional[ID] = None  # pointer to the CoordinateSystem::id.
    origin: Optional[Origin] = None
    transformation: Optional[Transformation] = None
    uuid: Optional[UUID] = None  # UUID for the coordinate system.
    description: Optional[str] = None  # natural language description of the CoordinateSystem.

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.type is None:
            raise ValueError('type is required [1..1]')


@dataclass
class Origin:
    """coordinates of the origin position of a coordinate system."""
    value: Optional[OriginDataSet] = None


@dataclass
class Transformation:
    """process of transforming to the origin position of the coordinate system from a parent coordinate system using Translation and Rotation."""
    translation: Optional[Translation] = None
    rotation: Optional[Rotation] = None


@dataclass
class Rotation:
    """rotations about X, Y, and Z axes are expressed in A, B, and C respectively within a 3-dimensional vector."""
    value: Optional[RotationDataSet] = None


@dataclass
class Translation:
    """translations along X, Y, and Z axes are expressed as x,y, and z respectively within a 3-dimensional vector."""
    value: Optional[TranslationDataSet] = None


@dataclass
class Motion:
    """movement of the component relative to a coordinate system."""
    actuation: MotionActuationTypeEnum  # describes if this component is actuated directly or indirectly as a result of other motion.
    coordinate_system_id_ref: ID  # coordinate system within which the kinematic motion occurs.
    id: ID  # unique identifier for this element.
    type: MotionTypeEnum  # type of motion.
    parent_id_ref: Optional[ID] = None  # pointer to the Motion::id. The kinematic chain connects all components using the parent relations. All motion is connected to the motion of the parent. The first node in the chain will not have a parent.
    axis: Optional[Axis] = None
    origin: Optional[Origin] = None
    transformation: Optional[Transformation] = None
    description: Optional[str] = None  # textual description for Motion.

    def __post_init__(self):
        if isinstance(self.coordinate_system_id_ref, str):
            self.coordinate_system_id_ref = ID(self.coordinate_system_id_ref)
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.actuation is None:
            raise ValueError('actuation is required [1..1]')
        if self.coordinate_system_id_ref is None:
            raise ValueError('coordinateSystemIdRef is required [1..1]')
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.type is None:
            raise ValueError('type is required [1..1]')


@dataclass
class Axis:
    """axis along or around which the Component moves relative to a coordinate system."""
    value: Optional[AxisDataSet] = None


@dataclass
class Specification:
    """design characteristics for a piece of equipment."""
    type: DataItemTypeEnum  # same as DataItem::type. See DataItem Types.
    originator: OriginatorEnum  # reference to the creator of the Specification.
    sub_type: Optional[DataItemSubType] = None  # same as DataItem::subType. See DataItem.
    data_item_id_ref: Optional[ID] = None  # reference to the DataItem::id associated with this entity.
    units: Optional[UnitEnum] = None  # same as DataItem::units. See DataItem.
    composition_id_ref: Optional[ID] = None  # reference to the Composition::id associated with this entity.
    name: Optional[str] = None  # Specification::name provides additional meaning and differentiates between Specification entities.
    coordinate_system_id_ref: Optional[ID] = None  # references the CoordinateSystem for geometric Specification elements.
    id: Optional[ID] = None  # unique identifier for this Specification.
    maximum: Optional[Maximum] = None
    upper_limit: Optional[UpperLimit] = None
    lower_warning: Optional[LowerWarning] = None
    lower_limit: Optional[LowerLimit] = None
    upper_warning: Optional[UpperWarning] = None
    nominal: Optional[Nominal] = None
    minimum: Optional[Minimum] = None

    def __post_init__(self):
        if self.type is None:
            raise ValueError('type is required [1..1]')
        if self.originator is None:
            raise ValueError('originator is required [1..1]')


@dataclass
class ProcessSpecification(Specification):
    """Specification that provides information used to assess the conformance of a variable to process requirements."""
    specification_limits: Optional[SpecificationLimits] = None
    control_limits: Optional[ControlLimits] = None
    alarm_limits: Optional[AlarmLimits] = None


@dataclass
class ControlLimits:
    """set of limits that is used to indicate whether a process variable is stable and in control."""
    upper_limit: Optional[UpperLimit] = None
    upper_warning: Optional[UpperWarning] = None
    lower_warning: Optional[LowerWarning] = None
    nominal: Optional[Nominal] = None
    lower_limit: Optional[LowerLimit] = None


@dataclass
class AlarmLimits:
    """set of limits that is used to trigger warning or alarm indicators."""
    upper_limit: Optional[UpperLimit] = None
    upper_warning: Optional[UpperWarning] = None
    lower_limit: Optional[LowerLimit] = None
    lower_warning: Optional[LowerWarning] = None


@dataclass
class SpecificationLimits:
    """set of limits that define a range of values designating acceptable performance for a variable."""
    upper_limit: Optional[UpperLimit] = None
    nominal: Optional[Nominal] = None
    lower_limit: Optional[LowerLimit] = None


@dataclass
class UpperWarning:
    """upper boundary indicating increased concern and supervision may be required."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class UpperLimit:
    """upper conformance boundary for a variable. > Note: immediate concern or action may be required."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class Maximum:
    """numeric upper constraint."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class LowerLimit:
    """lower conformance boundary for a variable. > Note: immediate concern or action may be required."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class LowerWarning:
    """lower boundary indicating increased concern and supervision may be required."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class Minimum:
    """numeric lower constraint."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class Nominal:
    """numeric target or expected value."""
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError('value is required [1..1]')


@dataclass
class SensorConfiguration:
    """configuration for a Sensor."""
    firmware_version: str  # Version number for the sensor unit as specified by the manufacturer.
    calibration_date: Optional[datetime] = None  # Date upon which the sensor unit was last calibrated.
    calibration_initials: Optional[str] = None  # The initials of the person verifying the validity of the calibration data.
    next_calibration_date: Optional[datetime] = None  # Date upon which the sensor unit is next scheduled to be calibrated.
    channel: List[Channel] = field(default_factory=list)

    def __post_init__(self):
        if self.firmware_version is None:
            raise ValueError('FirmwareVersion is required [1..1]')


@dataclass
class Channel:
    """sensing element of a Sensor."""
    number: str  # unique identifier that will only refer to a specific sensing element.
    is_channel_of: SensorConfiguration
    calibration_date: Optional[datetime] = None  # Date upon which the sensor unit was last calibrated to the sensor element.
    calibration_initials: Optional[str] = None  # The initials of the person verifying the validity of the calibration data.
    name: Optional[str] = None  # name of the specific sensing element.
    next_calibration_date: Optional[datetime] = None  # Date upon which the sensor element is next scheduled to be calibrated with the sensor unit.
    description: Optional[str] = None  # textual description for Channel.

    def __post_init__(self):
        if self.number is None:
            raise ValueError('number is required [1..1]')
        if self.is_channel_of is None:
            raise ValueError('isChannelOf is required [1..1]')


@dataclass
class ConfigurationRelationship:
    """association between two pieces of equipment or assets that may function independently but together perform a manufacturing operation."""
    id: ID  # unique identifier for this ConfigurationRelationship.
    type: RelationshipTypeEnum  # defines the authority that this piece of equipment has relative to the associated piece of equipment.
    name: Optional[str] = None  # name associated with this ConfigurationRelationship.
    criticality: Optional[CriticalityTypeEnum] = None  # defines whether the services or functions provided by the associated piece of equipment is required for the operation of this piece of equipment.

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.type is None:
            raise ValueError('type is required [1..1]')


@dataclass
class ComponentRelationship(ConfigurationRelationship):
    """ConfigurationRelationship that describes the association between a Component or an Asset and another {{block(Component)."""
    id_ref: ID = None  # reference to the associated Component.

    def __post_init__(self):
        if isinstance(self.id_ref, str):
            self.id_ref = ID(self.id_ref)
        if self.id_ref is None:
            raise ValueError('idRef is required [1..1]')


@dataclass
class DeviceRelationship(ConfigurationRelationship):
    """ConfigurationRelationship that describes the association between a Component or an Asset and a {{block(Device)."""
    device_uuid_ref: UUID = None  # reference to the Device::uuid of the associated piece of equipment.
    href: Optional[xlinkhref] = None  # URI identifying the agent that is publishing information for the associated piece of equipment.
    role: Optional[RoleTypeEnum] = None  # defines the services or capabilities that the referenced piece of equipment provides relative to this piece of equipment.
    xlink_type: Optional[xlinktype] = None  # `xlink:type`**MUST** have a fixed value of `locator` as defined in W3C XLink 1.1 https://www.w3.org/TR/xlink11/.

    def __post_init__(self):
        if isinstance(self.device_uuid_ref, str):
            self.device_uuid_ref = ID(self.device_uuid_ref)
        if self.device_uuid_ref is None:
            raise ValueError('deviceUuidRef is required [1..1]')


@dataclass
class AssetRelationship(ConfigurationRelationship):
    """ConfigurationRelationship that describes the association between a Component or an Asset and another Asset."""
    asset_id_ref: ID = None  # uuid of the related Asset.
    asset_type: str = None  # type of Asset being referenced.
    href: Optional[xlinkhref] = None  # URI reference to the associated Asset.

    def __post_init__(self):
        if isinstance(self.asset_id_ref, str):
            self.asset_id_ref = ID(self.asset_id_ref)
        if self.asset_id_ref is None:
            raise ValueError('assetIdRef is required [1..1]')
        if self.asset_type is None:
            raise ValueError('assetType is required [1..1]')


@dataclass
class Configuration:
    """technical information about an entity describing its physical layout, functional characteristics, and relationships with other entities."""
    is_configuration_for: Component
    solid_model: Optional[SolidModel] = None
    sensor_configuration: Optional[SensorConfiguration] = None
    motion: Optional[Motion] = None
    relationship: List[ConfigurationRelationship] = field(default_factory=list)
    coordinate_system: List[CoordinateSystem] = field(default_factory=list)
    specification: List[Specification] = field(default_factory=list)
    image_file: List[ImageFile] = field(default_factory=list)
    power_source: List[PowerSource] = field(default_factory=list)

    def __post_init__(self):
        if self.is_configuration_for is None:
            raise ValueError('isConfigurationFor is required [1..1]')


@dataclass
class Configuration:
    """technical information about an entity describing its physical layout, functional characteristics, and relationships with other entities."""
    is_configuration_for: Component
    solid_model: Optional[SolidModel] = None
    sensor_configuration: Optional[SensorConfiguration] = None
    motion: Optional[Motion] = None
    relationship: List[ConfigurationRelationship] = field(default_factory=list)
    coordinate_system: List[CoordinateSystem] = field(default_factory=list)
    specification: List[Specification] = field(default_factory=list)
    image_file: List[ImageFile] = field(default_factory=list)
    power_source: List[PowerSource] = field(default_factory=list)

    def __post_init__(self):
        if self.is_configuration_for is None:
            raise ValueError('isConfigurationFor is required [1..1]')


@dataclass
class SolidModel:
    """references to a file with the three-dimensional geometry of the Component or Composition."""
    id: ID  # unique identifier for this element.
    media_type: MediaTypeEnum  # format of the referenced document.
    transformation: Optional[Transformation] = None
    scale: Optional[Scale] = None
    solid_model_id_ref: Optional[ID] = None  # associated model file if an item reference is used.
    href: Optional[str] = None  # URL giving the location of the SolidModel. If not present, the model referenced in the SolidModel::solidModelIdRef is used. SolidModel::href is of type `xlink:href` from the W3C XLink specification.
    item_ref: Optional[str] = None  # reference to the item within the model within the related geometry. A SolidModel::solidModelIdRef **MUST** be given. > Note: `Item` defined in ASME Y14.100 - A nonspecific term used to denote any unit or product, including materials, parts, assemblies, equipment, accessories, and computer software.
    coordinate_system_id_ref: Optional[ID] = None  # reference to the coordinate system for this SolidModel.
    native_units: Optional[UnitEnum] = None  # same as DataItem::nativeUnits. See DataItem.
    units: Optional[UnitEnum] = None  # same as DataItem::units. See DataItem.

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.media_type is None:
            raise ValueError('mediaType is required [1..1]')


@dataclass
class Scale:
    """either a single multiplier applied to all three dimensions or a three space multiplier given in the X, Y, and Z dimensions in the coordinate system used for the SolidModel."""
    value: Optional[ScaleDataSet] = None


@dataclass
class ImageFile:
    """reference to a file containing an image of the Component."""
    id: ID  # unique identifier of the image file.
    href: str  # URL giving the location of the image file.
    media_type: str  # mime type of the image file.
    name: Optional[str] = None  # description of the image file.

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.href is None:
            raise ValueError('href is required [1..1]')
        if self.media_type is None:
            raise ValueError('mediaType is required [1..1]')


@dataclass
class PowerSource:
    """potential energy sources for the Component."""
    type: PowerSourceTypeEnum  # type of the power source.
    id: ID  # unique identifier for the power source.
    value: str  # name of the power source.
    component_id_ref: Optional[ID] = None  # reference to the Component providing observations about the power source.
    order: Optional[int] = None  # optional precedence for a given power source.

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.type is None:
            raise ValueError('type is required [1..1]')
        if self.id is None:
            raise ValueError('id is required [1..1]')
        if self.value is None:
            raise ValueError('value is required [1..1]')
