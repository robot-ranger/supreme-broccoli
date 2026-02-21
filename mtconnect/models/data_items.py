"""
MTConnect DataItem Models

DataItem definitions representing observation points for data collection from
manufacturing equipment. DataItems are categorized as SAMPLE, EVENT, or CONDITION
and define the type, units, constraints, and metadata for equipment observations.

Reference: MTConnect Standard v2.6 - DataItems Package
Auto-generated from: model_2.6.xml
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Union, TYPE_CHECKING
from enum import Enum

from mtconnect.types.enums import (
    UnitEnum,
    ActuatorStateEnum, AlarmCodeEnum, AlarmSeverityEnum, AlarmStateEnum,
    AvailabilityEnum, AxisCouplingEnum, AxisInterlockEnum, AxisStateEnum,
    BatteryStateEnum, CharacteristicStatusEnum, ChuckInterlockEnum, ChuckStateEnum,
    ConnectionStatusEnum, ControllerModeEnum, ControllerModeOverrideEnum,
    DirectionEnum, DoorStateEnum, EmergencyStopEnum, EndOfBarEnum,
    EquipmentModeEnum, ExecutionEnum, FunctionalModeEnum, InterfaceStateEnum,
    LeakDetectEnum, LockStateEnum, OperatingModeEnum, PartCountTypeEnum,
    PartDetectEnum, PartProcessingStateEnum, PartStatusEnum, PathModeEnum,
    PowerStateEnum, PowerStatusEnum, ProcessStateEnum, ProgramEditEnum,
    ProgramLocationTypeEnum, RotaryModeEnum, SpindleInterlockEnum,
    UncertaintyTypeEnum, ValveStateEnum, WaitStateEnum
)
from mtconnect.types.primitives import ID, MTCFloat, MTCInteger
from mtconnect.types.sample import SampleType
from mtconnect.types.event import EventType
from mtconnect.types.condition import ConditionType
from mtconnect.types.subtype import DataItemSubType


class DataItemCategory(Enum):
    """MTConnect DataItem categories"""
    SAMPLE = "SAMPLE"
    EVENT = "EVENT"
    CONDITION = "CONDITION"


@dataclass
class Constraints:
    """
    Constraints defining valid value ranges or sets for a DataItem.
    """
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    nominal: Optional[float] = None
    values: Optional[List[str]] = None


@dataclass
class DataItem:
    """
    Base class for all MTConnect DataItems.
    
    A DataItem represents a measurement or observation point on a Component.
    """
    id: ID
    type: Union[SampleType, EventType, ConditionType, str]
    category: DataItemCategory
    name: Optional[str] = None
    sub_type: Optional[DataItemSubType] = None
    units: Optional[UnitEnum] = None
    native_units: Optional[UnitEnum] = None
    native_scale: Optional[MTCFloat] = None
    significant_digits: Optional[MTCInteger] = None
    coordinate_system: Optional[ID] = None
    composition_id: Optional[str] = None
    constraints: Optional[Constraints] = None
    discrete: bool = False

    def __post_init__(self):
        """Validate DataItem after initialization"""
        if isinstance(self.id, str):
            self.id = ID(self.id)


@dataclass
class SampleDataItem(DataItem):
    """
    DataItem representing continuously variable numeric measurements.
    
    SAMPLE DataItems report numeric values that vary continuously over time.
    """
    category: DataItemCategory = DataItemCategory.SAMPLE


@dataclass
class EventDataItem(DataItem):
    """
    DataItem representing discrete, non-numeric state or status information.
    
    EVENT DataItems report discrete values that change in response to specific
    occurrences or state transitions.
    """
    category: DataItemCategory = DataItemCategory.EVENT


@dataclass
class ConditionDataItem(DataItem):
    """
    DataItem representing the health status of a Component.
    
    CONDITION DataItems report the operational health and status of equipment.
    """
    category: DataItemCategory = DataItemCategory.CONDITION


# ============================================================================
# SAMPLE DataItems
# ============================================================================


@dataclass
class Acceleration(SampleDataItem):
    """SampleEnum::ACCELERATION"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class AccumulatedTime(SampleDataItem):
    """SampleEnum::ACCUMULATED_TIME"""
    units: UnitEnum = None


@dataclass
class Amperage(SampleDataItem):
    """SampleEnum::AMPERAGE"""
    units: UnitEnum = None


@dataclass
class AmperageAC(SampleDataItem):
    """SampleEnum::AMPERAGE_AC"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class AmperageDC(SampleDataItem):
    """SampleEnum::AMPERAGE_DC"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class Angle(SampleDataItem):
    """SampleEnum::ANGLE"""
    units: UnitEnum = None


@dataclass
class AngularAcceleration(SampleDataItem):
    """SampleEnum::ANGULAR_ACCELERATION"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class AngularDeceleration(SampleDataItem):
    """SampleEnum::ANGULAR_DECELERATION"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class AngularVelocity(SampleDataItem):
    """SampleEnum::ANGULAR_VELOCITY"""
    units: UnitEnum = None


@dataclass
class AssetUpdateRate(SampleDataItem):
    """SampleEnum::ASSET_UPDATE_RATE"""
    units: UnitEnum = None


@dataclass
class AxisFeedrate(SampleDataItem):
    """SampleEnum::AXIS_FEEDRATE"""
    units: UnitEnum = None


@dataclass
class BatteryCapacity(SampleDataItem):
    """SampleEnum::BATTERY_CAPACITY"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class BatteryCharge(SampleDataItem):
    """SampleEnum::BATTERY_CHARGE"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class CapacityFluid(SampleDataItem):
    """SampleEnum::CAPACITY_FLUID"""
    units: UnitEnum = None


@dataclass
class CapacitySpatial(SampleDataItem):
    """SampleEnum::CAPACITY_SPATIAL"""
    units: UnitEnum = None


@dataclass
class ChargeRate(SampleDataItem):
    """SampleEnum::CHARGE_RATE"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class Concentration(SampleDataItem):
    """SampleEnum::CONCENTRATION"""
    units: UnitEnum = None


@dataclass
class Conductivity(SampleDataItem):
    """SampleEnum::CONDUCTIVITY"""
    units: UnitEnum = None


@dataclass
class CuttingSpeed(SampleDataItem):
    """SampleEnum::CUTTING_SPEED"""
    units: UnitEnum = None


@dataclass
class Deceleration(SampleDataItem):
    """SampleEnum::DECELERATION"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class Density(SampleDataItem):
    """SampleEnum::DENSITY"""
    units: UnitEnum = None


@dataclass
class DepositionAccelerationVolumetric(SampleDataItem):
    """SampleEnum::DEPOSITION_ACCELERATION_VOLUMETRIC"""
    units: UnitEnum = None


@dataclass
class DepositionDensity(SampleDataItem):
    """SampleEnum::DEPOSITION_DENSITY"""
    units: UnitEnum = None


@dataclass
class DepositionMass(SampleDataItem):
    """SampleEnum::DEPOSITION_MASS"""
    units: UnitEnum = None


@dataclass
class DepositionRateVolumetric(SampleDataItem):
    """SampleEnum::DEPOSITION_RATE_VOLUMETRIC"""
    units: UnitEnum = None


@dataclass
class DepositionVolume(SampleDataItem):
    """SampleEnum::DEPOSITION_VOLUME"""
    units: UnitEnum = None


@dataclass
class DewPoint(SampleDataItem):
    """SampleEnum::DEW_POINT"""
    units: UnitEnum = None


@dataclass
class Diameter(SampleDataItem):
    """SampleEnum::DIAMETER"""
    units: UnitEnum = None


@dataclass
class DischargeRate(SampleDataItem):
    """SampleEnum::DISCHARGE_RATE"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class Displacement(SampleDataItem):
    """SampleEnum::DISPLACEMENT"""
    units: UnitEnum = None


@dataclass
class DisplacementAngular(SampleDataItem):
    """SampleEnum::DISPLACEMENT_ANGULAR > Note: The displacement vector **MAY** be defined by the motion of the owning Component."""
    units: UnitEnum = None


@dataclass
class DisplacementLinear(SampleDataItem):
    """SampleEnum::DISPLACEMENT_LINEAR > Note: The displacement vector **MAY** be defined by the motion of the owning Component."""
    units: UnitEnum = None


@dataclass
class ElectricalEnergy(SampleDataItem):
    """SampleEnum::ELECTRICAL_ENERGY"""
    units: UnitEnum = None


@dataclass
class EquipmentTimer(SampleDataItem):
    """SampleEnum::EQUIPMENT_TIMER"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class FillHeight(SampleDataItem):
    """SampleEnum::FILL_HEIGHT"""
    units: UnitEnum = None


@dataclass
class FillLevel(SampleDataItem):
    """SampleEnum::FILL_LEVEL"""
    units: UnitEnum = None


@dataclass
class Flow(SampleDataItem):
    """SampleEnum::FLOW"""
    units: UnitEnum = None


@dataclass
class FollowingError(SampleDataItem):
    """SampleEnum::FOLLOWING_ERROR"""
    units: UnitEnum = None


@dataclass
class FollowingErrorAngular(SampleDataItem):
    """SampleEnum::FOLLOWING_ERROR_ANGULAR"""
    units: UnitEnum = None


@dataclass
class FollowingErrorLinear(SampleDataItem):
    """SampleEnum::FOLLOWING_ERROR_LINEAR"""
    units: UnitEnum = None


@dataclass
class Frequency(SampleDataItem):
    """SampleEnum::FREQUENCY"""
    units: UnitEnum = None


@dataclass
class GlobalPosition(SampleDataItem):
    """SampleEnum::GLOBAL_POSITION"""
    units: UnitEnum = None


@dataclass
class GravitationalAcceleration(SampleDataItem):
    """SampleEnum::GRAVITATIONAL_ACCELERATION"""
    units: UnitEnum = None


@dataclass
class GravitationalForce(SampleDataItem):
    """SampleEnum::GRAVITATIONAL_FORCE > Note: $$Mass\times GravitationalAcceleration$$"""
    units: UnitEnum = None


@dataclass
class HumidityAbsolute(SampleDataItem):
    """SampleEnum::HUMIDITY_ABSOLUTE"""
    units: UnitEnum = None


@dataclass
class HumidityRelative(SampleDataItem):
    """SampleEnum::HUMIDITY_RELATIVE"""
    units: UnitEnum = None


@dataclass
class HumiditySpecific(SampleDataItem):
    """SampleEnum::HUMIDITY_SPECIFIC"""
    units: UnitEnum = None


@dataclass
class Length(SampleDataItem):
    """SampleEnum::LENGTH"""
    units: UnitEnum = None


@dataclass
class Level(SampleDataItem):
    """SampleEnum::LEVEL"""
    units: UnitEnum = None


@dataclass
class LinearForce(SampleDataItem):
    """SampleEnum::LINEAR_FORCE"""
    units: UnitEnum = None


@dataclass
class Load(SampleDataItem):
    """SampleEnum::LOAD"""
    units: UnitEnum = None


@dataclass
class Mass(SampleDataItem):
    """SampleEnum::MASS"""
    units: UnitEnum = None


@dataclass
class ObservationUpdateRate(SampleDataItem):
    """SampleEnum::OBSERVATION_UPDATE_RATE"""
    units: UnitEnum = None


@dataclass
class ObservedMeasurement(SampleDataItem):
    """ObservedMeasurement DataItem."""
    pass


@dataclass
class Openness(SampleDataItem):
    """SampleEnum::OPENNESS"""
    units: UnitEnum = None


@dataclass
class Orientation(SampleDataItem):
    """SampleEnum::ORIENTATION"""
    units: UnitEnum = None
    result: Optional[List[float]] = None


@dataclass
class PH(SampleDataItem):
    """SampleEnum::PH"""
    units: UnitEnum = None


@dataclass
class ParticleCount(SampleDataItem):
    """SampleEnum::PARTICLE_COUNT"""
    units: UnitEnum = None


@dataclass
class ParticleSize(SampleDataItem):
    """SampleEnum::PARTICLE_SIZE"""
    units: UnitEnum = None


@dataclass
class PathFeedrate(SampleDataItem):
    """SampleEnum::PATH_FEEDRATE"""
    units: UnitEnum = None


@dataclass
class PathFeedratePerRevolution(SampleDataItem):
    """SampleEnum::PATH_FEEDRATE_PER_REVOLUTION"""
    units: UnitEnum = None


@dataclass
class PathPosition(SampleDataItem):
    """SampleEnum::PATH_POSITION"""
    units: UnitEnum = None
    result: Optional[List[float]] = None


@dataclass
class Position(SampleDataItem):
    """SampleEnum::POSITION"""
    units: UnitEnum = None


@dataclass
class PositionCartesian(SampleDataItem):
    """SampleEnum::POSITION_CARTESIAN"""
    units: UnitEnum = None
    result: Optional[List[float]] = None


@dataclass
class PowerFactor(SampleDataItem):
    """SampleEnum::POWER_FACTOR"""
    units: UnitEnum = None


@dataclass
class Pressure(SampleDataItem):
    """SampleEnum::PRESSURE"""
    units: UnitEnum = None


@dataclass
class PressureAbsolute(SampleDataItem):
    """The force per unit area measured relative to a vacuum."""
    units: UnitEnum = None


@dataclass
class PressurizationRate(SampleDataItem):
    """SampleEnum::PRESSURIZATION_RATE"""
    units: UnitEnum = None


@dataclass
class ProcessTimer(SampleDataItem):
    """SampleEnum::PROCESS_TIMER"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class Resistance(SampleDataItem):
    """SampleEnum::RESISTANCE"""
    units: UnitEnum = None


@dataclass
class Resistivity(SampleDataItem):
    """SampleEnum::RESISTIVITY"""
    units: UnitEnum = None


@dataclass
class RotaryVelocity(SampleDataItem):
    """SampleEnum::ROTARY_VELOCITY"""
    units: UnitEnum = None


@dataclass
class SettlingError(SampleDataItem):
    """SampleEnum::SETTLING_ERROR"""
    units: UnitEnum = None


@dataclass
class SettlingErrorAngular(SampleDataItem):
    """SampleEnum::SETTLING_ERROR_ANGULAR"""
    units: UnitEnum = None


@dataclass
class SettlingErrorLinear(SampleDataItem):
    """SampleEnum::SETTLING_ERROR_LINEAR"""
    units: UnitEnum = None


@dataclass
class SoundLevel(SampleDataItem):
    """SampleEnum::SOUND_LEVEL"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class SpindleSpeed(SampleDataItem):
    """SampleEnum::SPINDLE_SPEED"""
    units: UnitEnum = None


@dataclass
class Strain(SampleDataItem):
    """SampleEnum::STRAIN"""
    units: UnitEnum = None


@dataclass
class Temperature(SampleDataItem):
    """SampleEnum::TEMPERATURE"""
    units: UnitEnum = None


@dataclass
class Tension(SampleDataItem):
    """SampleEnum::TENSION"""
    units: UnitEnum = None


@dataclass
class Tilt(SampleDataItem):
    """SampleEnum::TILT"""
    units: UnitEnum = None


@dataclass
class Torque(SampleDataItem):
    """SampleEnum::TORQUE"""
    units: UnitEnum = None


@dataclass
class Velocity(SampleDataItem):
    """SampleEnum::VELOCITY"""
    units: UnitEnum = None


@dataclass
class Viscosity(SampleDataItem):
    """SampleEnum::VISCOSITY"""
    units: UnitEnum = None


@dataclass
class VoltAmpere(SampleDataItem):
    """SampleEnum::VOLT_AMPERE"""
    units: UnitEnum = None


@dataclass
class VoltAmpereReactive(SampleDataItem):
    """SampleEnum::VOLT_AMPERE_REACTIVE"""
    units: UnitEnum = None


@dataclass
class Voltage(SampleDataItem):
    """SampleEnum::VOLTAGE"""
    units: UnitEnum = None


@dataclass
class VoltageAC(SampleDataItem):
    """SampleEnum::VOLTAGE_AC"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class VoltageDC(SampleDataItem):
    """SampleEnum::VOLTAGE_DC"""
    units: UnitEnum = None
    sub_type: DataItemSubType = None


@dataclass
class VolumeFluid(SampleDataItem):
    """SampleEnum::VOLUME_FLUID"""
    units: UnitEnum = None


@dataclass
class VolumeSpatial(SampleDataItem):
    """SampleEnum::VOLUME_SPATIAL"""
    units: UnitEnum = None


@dataclass
class Wattage(SampleDataItem):
    """SampleEnum::WATTAGE"""
    units: UnitEnum = None


@dataclass
class XDimension(SampleDataItem):
    """SampleEnum::X_DIMENSION"""
    units: UnitEnum = None


@dataclass
class YDimension(SampleDataItem):
    """SampleEnum::Y_DIMENSION"""
    units: UnitEnum = None


@dataclass
class ZDimension(SampleDataItem):
    """SampleEnum::Z_DIMENSION"""
    units: UnitEnum = None


# ============================================================================
# EVENT DataItems
# ============================================================================


@dataclass
class ActivationCount(EventDataItem):
    """EventEnum::ACTIVATION_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class ActiveAxes(EventDataItem):
    """EventEnum::ACTIVE_AXES"""
    result: List[str] = field(default_factory=list)


@dataclass
class ActivePowerSource(EventDataItem):
    """EventEnum::ACTIVE_POWER_SOURCE"""
    result: Optional[str] = None  # name of the power source referring to Configuration PowerSource::value.


@dataclass
class ActuatorState(EventDataItem):
    """EventEnum::ACTUATOR_STATE"""
    result: Optional[ActuatorStateEnum] = None


@dataclass
class AdapterSoftwareVersion(EventDataItem):
    """EventEnum::ADAPTER_SOFTWARE_VERSION"""
    pass


@dataclass
class AdapterURI(EventDataItem):
    """EventEnum::ADAPTER_URI"""
    pass


@dataclass
class Alarm(EventDataItem):
    """EventEnum::ALARM"""
    code: AlarmCodeEnum = None  # type of alarm.
    severity: AlarmSeverityEnum = None  # severity of the alarm.
    native_code: str = None  # native code for the piece of equipment.
    state: AlarmStateEnum = None  # state of the alarm.
    lang: Optional[str] = None  # specifies the language of the alarm text. See IETF RFC 4646 (http://www.ietf.org/rfc/rfc4646.txt).


@dataclass
class AlarmLimit(EventDataItem):
    """EventEnum::ALARM_LIMIT"""
    pass


@dataclass
class AlarmLimits(EventDataItem):
    """EventEnum::ALARM_LIMITS"""
    pass


@dataclass
class Application(EventDataItem):
    """EventEnum::APPLICATION"""
    sub_type: DataItemSubType = None


@dataclass
class AssetAdded(EventDataItem):
    """EventEnum::ASSET_ADDED"""
    asset_type: Optional[str] = None  # type of Asset added. See Asset Information Model for details on the Asset model.
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class AssetChanged(EventDataItem):
    """EventEnum::ASSET_CHANGED"""
    asset_type: Optional[str] = None  # type of Asset changed. See Asset Information Model for details on the Asset model.
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class AssetCount(EventDataItem):
    """EventEnum::ASSET_COUNT"""
    result: Optional[int] = None


@dataclass
class AssetRemoved(EventDataItem):
    """EventEnum::ASSET_REMOVED"""
    asset_type: Optional[str] = None  # type of Asset removed. See Asset Information Model for details on the Asset model.
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class AssociatedAssetId(EventDataItem):
    """EventEnum::ASSOCIATED_ASSET_ID If defined as a DataSet or Table: * `key` **MUST** be an {(block(Asset)}} type. Examples: CuttingTool, Fixture, File. * `value` **MUST** be the corresponding Asset::assetId."""
    pass


@dataclass
class Availability(EventDataItem):
    """EventEnum::AVAILABILITY"""
    result: Optional[AvailabilityEnum] = None


@dataclass
class AxisCoupling(EventDataItem):
    """EventEnum::AXIS_COUPLING"""
    result: Optional[AxisCouplingEnum] = None


@dataclass
class AxisFeedrateOverride(EventDataItem):
    """EventEnum::AXIS_FEEDRATE_OVERRIDE"""
    result: Optional[float] = None


@dataclass
class AxisInterlock(EventDataItem):
    """EventEnum::AXIS_INTERLOCK"""
    result: Optional[AxisInterlockEnum] = None


@dataclass
class AxisState(EventDataItem):
    """EventEnum::AXIS_STATE"""
    result: Optional[AxisStateEnum] = None


@dataclass
class BatteryState(EventDataItem):
    """EventEnum::BATTERY_STATE"""
    result: Optional[BatteryStateEnum] = None


@dataclass
class Block(EventDataItem):
    """EventEnum::BLOCK"""
    pass


@dataclass
class BlockCount(EventDataItem):
    """EventEnum::BLOCK_COUNT"""
    result: Optional[int] = None


@dataclass
class CharacteristicPersistentId(EventDataItem):
    """EventEnum::CHARACTERISTIC_PERSISTENT_ID"""
    result: Optional[ID] = None


@dataclass
class CharacteristicStatus(EventDataItem):
    """EventEnum::CHARACTERISTIC_STATUS"""
    result: Optional[CharacteristicStatusEnum] = None


@dataclass
class ChuckInterlock(EventDataItem):
    """EventEnum::CHUCK_INTERLOCK"""
    result: Optional[ChuckInterlockEnum] = None


@dataclass
class ChuckState(EventDataItem):
    """EventEnum::CHUCK_STATE"""
    result: Optional[ChuckStateEnum] = None


@dataclass
class ClockTime(EventDataItem):
    """EventEnum::CLOCK_TIME"""
    result: Optional[datetime] = None


@dataclass
class CloseChuck(EventDataItem):
    """InterfaceEventEnum::CLOSE_CHUCK"""
    sub_type: DataItemSubType = None


@dataclass
class CloseDoor(EventDataItem):
    """InterfaceEventEnum::CLOSE_DOOR"""
    sub_type: DataItemSubType = None


@dataclass
class Code(EventDataItem):
    """EventEnum::CODE"""
    pass


@dataclass
class ComponentData(EventDataItem):
    """tabular EventEnum::COMPONENT_DATA If the Component multiplicity can be determined, the device model **MUST** use a fixed set of Components. ComponentData **MUST** provide a DataItem Definition."""
    pass


@dataclass
class CompositionState(EventDataItem):
    """EventEnum::COMPOSITION_STATE"""
    sub_type: DataItemSubType = None


@dataclass
class ConnectionStatus(EventDataItem):
    """EventEnum::CONNECTION_STATUS"""
    result: Optional[ConnectionStatusEnum] = None


@dataclass
class ControlLimit(EventDataItem):
    """EventEnum::CONTROL_LIMIT"""
    pass


@dataclass
class ControlLimits(EventDataItem):
    """EventEnum::CONTROL_LIMITS"""
    pass


@dataclass
class ControllerMode(EventDataItem):
    """EventEnum::CONTROLLER_MODE"""
    result: Optional[ControllerModeEnum] = None


@dataclass
class ControllerModeOverride(EventDataItem):
    """EventEnum::CONTROLLER_MODE_OVERRIDE"""
    result: Optional[ControllerModeOverrideEnum] = None
    sub_type: DataItemSubType = None


@dataclass
class CoupledAxes(EventDataItem):
    """EventEnum::COUPLED_AXES"""
    result: List[str] = field(default_factory=list)


@dataclass
class CycleCount(EventDataItem):
    """EventEnum::CYCLE_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class DateCode(EventDataItem):
    """EventEnum::DATE_CODE"""
    result: Optional[datetime] = None


@dataclass
class DeactivationCount(EventDataItem):
    """EventEnum::DEACTIVATION_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class DeviceAdded(EventDataItem):
    """EventEnum::DEVICE_ADDED"""
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class DeviceChanged(EventDataItem):
    """EventEnum::DEVICE_CHANGED"""
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class DeviceRemoved(EventDataItem):
    """EventEnum::DEVICE_REMOVED"""
    hash: Optional[str] = None  # condensed message digest from a secure one-way hash function. FIPS PUB 180-4


@dataclass
class DeviceUuid(EventDataItem):
    """EventEnum::DEVICE_UUID"""
    pass


@dataclass
class Direction(EventDataItem):
    """EventEnum::DIRECTION"""
    result: Optional[DirectionEnum] = None
    sub_type: DataItemSubType = None


@dataclass
class DoorState(EventDataItem):
    """EventEnum::DOOR_STATE"""
    result: Optional[DoorStateEnum] = None


@dataclass
class EmergencyStop(EventDataItem):
    """EventEnum::EMERGENCY_STOP"""
    result: Optional[EmergencyStopEnum] = None


@dataclass
class EndOfBar(EventDataItem):
    """EventEnum::END_OF_BAR"""
    result: Optional[EndOfBarEnum] = None
    sub_type: DataItemSubType = None


@dataclass
class EquipmentMode(EventDataItem):
    """EventEnum::EQUIPMENT_MODE"""
    result: Optional[EquipmentModeEnum] = None
    sub_type: DataItemSubType = None


@dataclass
class Execution(EventDataItem):
    """EventEnum::EXECUTION"""
    result: Optional[ExecutionEnum] = None


@dataclass
class FeatureMeasurement(EventDataItem):
    """tabular representation of EventEnum::FEATURE_MEASUREMENT FeatureMeasurement **MAY** include a characteristic in which case it **MAY** include a `CHARACTERISTIC_STATUS`."""
    pass


@dataclass
class FeaturePersisitentId(EventDataItem):
    """EventEnum::FEATURE_PERSISTENT_ID"""
    result: Optional[ID] = None


@dataclass
class Firmware(EventDataItem):
    """EventEnum::FIRMWARE"""
    sub_type: DataItemSubType = None


@dataclass
class FixtureId(EventDataItem):
    """EventEnum::FIXTURE_ID"""
    pass


@dataclass
class FunctionalMode(EventDataItem):
    """EventEnum::FUNCTIONAL_MODE"""
    result: Optional[FunctionalModeEnum] = None


@dataclass
class Hardness(EventDataItem):
    """EventEnum::HARDNESS"""
    result: Optional[float] = None
    sub_type: DataItemSubType = None


@dataclass
class Hardware(EventDataItem):
    """EventEnum::HARDWARE"""
    sub_type: DataItemSubType = None


@dataclass
class HostName(EventDataItem):
    """EventEnum::HOST_NAME"""
    pass


@dataclass
class InterfaceState(EventDataItem):
    """InterfaceEventEnum::INTERFACE_STATE When the InterfaceState is `DISABLED`, the state of all data items that are specific for the interaction model associated with that Interface **MUST** be set to `NOT_READY`."""
    result: Optional[InterfaceStateEnum] = None


@dataclass
class LeakDetect(EventDataItem):
    """EventEnum::LEAK_DETECT"""
    result: Optional[LeakDetectEnum] = None


@dataclass
class Library(EventDataItem):
    """EventEnum::LIBRARY"""
    sub_type: DataItemSubType = None


@dataclass
class Line(EventDataItem):
    """EventEnum::LINE"""
    pass


@dataclass
class LineLabel(EventDataItem):
    """EventEnum::LINE_LABEL"""
    pass


@dataclass
class LineNumber(EventDataItem):
    """EventEnum::LINE_NUMBER"""
    result: Optional[int] = None


@dataclass
class LoadCount(EventDataItem):
    """EventEnum::LOAD_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class LocationAddress(EventDataItem):
    """EventEnum::LOCATION_ADDRESS"""
    pass


@dataclass
class LocationNarrative(EventDataItem):
    """EventEnum::LOCATION_NARRATIVE"""
    pass


@dataclass
class LocationSpatialGeographic(EventDataItem):
    """EventEnum::LOCATION_SPATIAL_GEOGRAPHIC"""
    pass


@dataclass
class LockState(EventDataItem):
    """EventEnum::LOCK_STATE"""
    result: Optional[LockStateEnum] = None


@dataclass
class MtconnectEvent(EventDataItem):
    """observation of either a state or discrete value of the Component."""
    pass


@dataclass
class MTConnectVersion(EventDataItem):
    """EventEnum::MTCONNECT_VERSION"""
    pass


@dataclass
class MaintenanceList(EventDataItem):
    """EventEnum::MAINTENANCE_LIST If MaintenanceList::result::Interval `key` is not provided, it is assumed `ABSOLUTE`. If MaintenanceList::result::Direction `key` is not provided, it is assumed `UP`. If MaintenanceList::result::Units `key` is not provided, it is assumed to be `COUNT`."""
    pass


@dataclass
class Material(EventDataItem):
    """EventEnum::MATERIAL"""
    pass


@dataclass
class MaterialChange(EventDataItem):
    """InterfaceEventEnum::MATERIAL_CHANGE"""
    sub_type: DataItemSubType = None


@dataclass
class MaterialFeed(EventDataItem):
    """InterfaceEventEnum::MATERIAL_FEED"""
    sub_type: DataItemSubType = None


@dataclass
class MaterialLayer(EventDataItem):
    """EventEnum::MATERIAL_LAYER"""
    result: Optional[int] = None


@dataclass
class MaterialLoad(EventDataItem):
    """InterfaceEventEnum::MATERIAL_LOAD"""
    sub_type: DataItemSubType = None


@dataclass
class MaterialRetract(EventDataItem):
    """InterfaceEventEnum::MATERIAL_RETRACT"""
    sub_type: DataItemSubType = None


@dataclass
class MaterialUnload(EventDataItem):
    """InterfaceEventEnum::MATERIAL_UNLOAD"""
    sub_type: DataItemSubType = None


@dataclass
class MeasurementType(EventDataItem):
    """EventEnum::MEASUREMENT_TYPE Examples: `POINT`, `RADIUS`, `ANGLE`, `LENGTH`, etc."""
    pass


@dataclass
class MeasurementUnits(EventDataItem):
    """EventEnum::MEASUREMENT_UNITS"""
    pass


@dataclass
class MeasurementValue(EventDataItem):
    """EventEnum::MEASUREMENT_VALUE"""
    result: Optional[float] = None


@dataclass
class Message(EventDataItem):
    """EventEnum::MESSAGE"""
    native_code: Optional[str] = None  # control system local identification of the information being transferred.


@dataclass
class Network(EventDataItem):
    """EventEnum::NETWORK"""
    sub_type: DataItemSubType = None


@dataclass
class NetworkPort(EventDataItem):
    """EventEnum::NETWORK_PORT"""
    result: Optional[int] = None


@dataclass
class OpenChuck(EventDataItem):
    """InterfaceEventEnum::OPEN_CHUCK"""
    sub_type: DataItemSubType = None


@dataclass
class OpenDoor(EventDataItem):
    """InterfaceEventEnum::OPEN_DOOR"""
    sub_type: DataItemSubType = None


@dataclass
class OperatingMode(EventDataItem):
    """EventEnum::OPERATING_MODE"""
    result: Optional[OperatingModeEnum] = None


@dataclass
class OperatingSystem(EventDataItem):
    """EventEnum::OPERATING_SYSTEM"""
    sub_type: DataItemSubType = None


@dataclass
class OperatorId(EventDataItem):
    """EventEnum::OPERATOR_ID"""
    pass


@dataclass
class PalletId(EventDataItem):
    """EventEnum::PALLET_ID"""
    pass


@dataclass
class PartChange(EventDataItem):
    """InterfaceEventEnum::PART_CHANGE"""
    sub_type: DataItemSubType = None


@dataclass
class PartCount(EventDataItem):
    """EventEnum::PART_COUNT"""
    result: Optional[int] = None
    sub_type: DataItemSubType = None


@dataclass
class PartCountType(EventDataItem):
    """EventEnum::PART_COUNT_TYPE"""
    result: Optional[PartCountTypeEnum] = None


@dataclass
class PartDetect(EventDataItem):
    """EventEnum::PART_DETECT"""
    result: Optional[PartDetectEnum] = None


@dataclass
class PartGroupId(EventDataItem):
    """EventEnum::PART_GROUP_ID If no DataItem::subType is specified, `UUID` is default."""
    sub_type: DataItemSubType = None


@dataclass
class PartId(EventDataItem):
    """EventEnum::PART_ID"""
    pass


@dataclass
class PartIndex(EventDataItem):
    """EventEnum::PART_INDEX"""
    result: Optional[int] = None


@dataclass
class PartKindId(EventDataItem):
    """EventEnum::PART_KIND_ID If no DataItem::subType is specified, `UUID` is default."""
    sub_type: DataItemSubType = None


@dataclass
class PartNumber(EventDataItem):
    """EventEnum::PART_NUMBER"""
    pass


@dataclass
class PartProcessingState(EventDataItem):
    """EventEnum::PART_PROCESSING_STATE"""
    result: Optional[PartProcessingStateEnum] = None


@dataclass
class PartStatus(EventDataItem):
    """EventEnum::PART_STATUS If unique identifier is given, part status is for that individual. If group identifier is given without a unique identifier, then the status is assumed to be for the whole group."""
    result: Optional[PartStatusEnum] = None


@dataclass
class PartUniqueId(EventDataItem):
    """EventEnum::PART_UNIQUE_ID If no DataItem::subType is specified, `UUID` is default."""
    sub_type: DataItemSubType = None


@dataclass
class PathFeedrateOverride(EventDataItem):
    """EventEnum::PATH_FEEDRATE_OVERRIDE"""
    result: Optional[float] = None


@dataclass
class PathMode(EventDataItem):
    """EventEnum::PATH_MODE"""
    result: Optional[PathModeEnum] = None


@dataclass
class PowerState(EventDataItem):
    """EventEnum::POWER_STATE"""
    result: Optional[PowerStateEnum] = None


@dataclass
class PowerStatus(EventDataItem):
    """EventEnum::POWER_STATUS"""
    result: Optional[PowerStatusEnum] = None


@dataclass
class ProcessAggregateId(EventDataItem):
    """EventEnum::PROCESS_AGGREGATE_ID"""
    pass


@dataclass
class ProcessKindId(EventDataItem):
    """EventEnum::PROCESS_KIND_ID"""
    pass


@dataclass
class ProcessOccurrenceId(EventDataItem):
    """EventEnum::PROCESS_OCCURRENCE_ID"""
    pass


@dataclass
class ProcessState(EventDataItem):
    """EventEnum::PROCESS_STATE"""
    result: Optional[ProcessStateEnum] = None


@dataclass
class ProcessTime(EventDataItem):
    """EventEnum::PROCESS_TIME"""
    sub_type: DataItemSubType = None


@dataclass
class Program(EventDataItem):
    """EventEnum::PROGRAM"""
    pass


@dataclass
class ProgramComment(EventDataItem):
    """EventEnum::PROGRAM_COMMENT"""
    pass


@dataclass
class ProgramEdit(EventDataItem):
    """EventEnum::PROGRAM_EDIT"""
    result: Optional[ProgramEditEnum] = None


@dataclass
class ProgramEditName(EventDataItem):
    """EventEnum::PROGRAM_EDIT_NAME"""
    pass


@dataclass
class ProgramHeader(EventDataItem):
    """EventEnum::PROGRAM_HEADER"""
    sub_type: DataItemSubType = None


@dataclass
class ProgramLocation(EventDataItem):
    """EventEnum::PROGRAM_LOCATION"""
    pass


@dataclass
class ProgramLocationType(EventDataItem):
    """EventEnum::PROGRAM_LOCATION_TYPE"""
    result: Optional[ProgramLocationTypeEnum] = None


@dataclass
class ProgramNestLevel(EventDataItem):
    """EventEnum::PROGRAM_NEST_LEVEL If an initial value is not defined, the nesting level associated with the highest or initial nesting level of the program **MUST** default to zero (0)."""
    result: Optional[int] = None


@dataclass
class RotaryMode(EventDataItem):
    """EventEnum::ROTARY_MODE"""
    result: Optional[RotaryModeEnum] = None


@dataclass
class RotaryVelocityOverride(EventDataItem):
    """EventEnum::ROTARY_VELOCITY_OVERRIDE This command represents a percentage change to the velocity calculated by a logic or motion program or set by a switch for a Rotary type axis."""
    result: Optional[float] = None


@dataclass
class Rotation(EventDataItem):
    """EventEnum::ROTATION"""
    units: UnitEnum = None
    result: Optional[List[float]] = None


@dataclass
class SensorAttachment(EventDataItem):
    """EventEnum::SENSOR_ATTACHMENT"""
    pass


@dataclass
class SensorState(EventDataItem):
    """EventEnum::SENSOR_STATE"""
    sub_type: DataItemSubType = None


@dataclass
class SerialNumber(EventDataItem):
    """EventEnum::SERIAL_NUMBER"""
    pass


@dataclass
class SpecificationLimit(EventDataItem):
    """EventEnum::SPECIFICATION_LIMIT"""
    pass


@dataclass
class SpecificationLimits(EventDataItem):
    """EventEnum::SPECIFICATION_LIMITS"""
    pass


@dataclass
class SpindleInterlock(EventDataItem):
    """EventEnum::SPINDLE_INTERLOCK"""
    result: Optional[SpindleInterlockEnum] = None


@dataclass
class Thickness(EventDataItem):
    """EventEnum::THICKNESS"""
    sub_type: DataItemSubType = None
    result: Optional[float] = None


@dataclass
class ToolAssetId(EventDataItem):
    """EventEnum::TOOL_ASSET_ID"""
    pass


@dataclass
class ToolCuttingItem(EventDataItem):
    """EventEnum::TOOL_CUTTING_ITEM"""
    pass


@dataclass
class ToolGroup(EventDataItem):
    """EventEnum::TOOL_GROUP"""
    pass


@dataclass
class ToolId(EventDataItem):
    """EventEnum::TOOL_ID"""
    pass


@dataclass
class ToolNumber(EventDataItem):
    """EventEnum::TOOL_NUMBER"""
    pass


@dataclass
class ToolOffset(EventDataItem):
    """EventEnum::TOOL_OFFSET"""
    result: Optional[float] = None
    sub_type: DataItemSubType = None


@dataclass
class ToolOffsets(EventDataItem):
    """tabular representation of EventEnum::TOOL_OFFSETS"""
    pass


@dataclass
class TransferCount(EventDataItem):
    """EventEnum::TRANSFER_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class Translation(EventDataItem):
    """EventEnum::TRANSLATION"""
    units: UnitEnum = None
    result: Optional[List[float]] = None


@dataclass
class Uncertainty(EventDataItem):
    """EventEnum::UNCERTAINTY"""
    result: Optional[float] = None


@dataclass
class UncertaintyType(EventDataItem):
    """EventEnum::UNCERTAINTY_TYPE"""
    result: Optional[UncertaintyTypeEnum] = None


@dataclass
class UnloadCount(EventDataItem):
    """EventEnum::UNLOAD_COUNT"""
    sub_type: DataItemSubType = None
    result: Optional[int] = None


@dataclass
class User(EventDataItem):
    """EventEnum::USER"""
    sub_type: DataItemSubType = None


@dataclass
class ValveState(EventDataItem):
    """EventEnum::VALVE_STATE"""
    result: Optional[ValveStateEnum] = None


@dataclass
class Variable(EventDataItem):
    """EventEnum::VARIABLE"""
    pass


@dataclass
class WaitState(EventDataItem):
    """EventEnum::WAIT_STATE When Execution::result is not `WAIT`, Observation::isUnavailable of WaitState **MUST** be `true`."""
    result: Optional[WaitStateEnum] = None


@dataclass
class Wire(EventDataItem):
    """EventEnum::WIRE"""
    pass


@dataclass
class WorkOffset(EventDataItem):
    """EventEnum::WORK_OFFSET"""
    pass


@dataclass
class WorkOffsets(EventDataItem):
    """tabular representation of EventEnum::WORK_OFFSETS"""
    pass


@dataclass
class WorkholdingId(EventDataItem):
    """EventEnum::WORKHOLDING_ID"""
    pass


# ============================================================================
# CONDITION DataItems
# ============================================================================


@dataclass
class Actuator(ConditionDataItem):
    """ConditionEnum::ACTUATOR"""
    pass


@dataclass
class Communications(ConditionDataItem):
    """ConditionEnum::COMMUNICATIONS"""
    pass


@dataclass
class DataRange(ConditionDataItem):
    """ConditionEnum::DATA_RANGE"""
    pass


@dataclass
class LogicProgram(ConditionDataItem):
    """ConditionEnum::LOGIC_PROGRAM"""
    pass


@dataclass
class MotionProgram(ConditionDataItem):
    """ConditionEnum::MOTION_PROGRAM"""
    pass


@dataclass
class System(ConditionDataItem):
    """ConditionEnum::SYSTEM"""
    pass
