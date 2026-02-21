"""
MTConnect Enumeration Types

Additional enumeration types extracted from the MTConnect normative model
version 2.6. These enums represent standardized values for units, states,
representations, and other categorical values used in MTConnect.

Reference: MTConnect Standard v2.6 Normative Model
Auto-generated from: model_2.6.xml
"""

from enum import Enum, auto

# =============================================================================
# Re-exports from canonical modules (backward compatibility)
# =============================================================================
# These types have dedicated modules. Re-exported here so existing imports
# like 'from mtconnect.types.enums import EventType' continue to work.
from mtconnect.types.event import EventType  # noqa: F401
from mtconnect.types.sample import SampleType  # noqa: F401
from mtconnect.types.condition import ConditionType  # noqa: F401
from mtconnect.types.subtype import DataItemSubType  # noqa: F401
from mtconnect.types.interface_types import (  # noqa: F401
    InterfaceEvent as InterfaceEventEnum,
    InterfaceState as InterfaceStateEnum,
)


################################################################################
# Core Enumerations
################################################################################

class CategoryEnum(Enum):
    """CategoryEnum values from MTConnect model"""

    SAMPLE = auto()  # continuously variable or analog data value. A continuous value can be measure...
    EVENT = auto()  # discrete piece of information from the piece of equipment.
    CONDITION = auto()  # information about the health of a piece of equipment and its ability to funct...


class RepresentationEnum(Enum):
    """RepresentationEnum values from MTConnect model"""

    TIME_SERIES = auto()  # series of sampled data. The data is reported for a specified number of sample...
    VALUE = auto()  # measured value of the sample data. If no DataItem::representation is specifie...
    DATA_SET = auto()  # reported value(s) are represented as a set of key-value pair. Each reported v...
    DISCRETE = auto()  # **DEPRECATED** as DataItem::representation type in *MTConnect Version 1.5*. R...
    TABLE = auto()  # two dimensional set of key-value pair where the Entry represents a row, and t...



################################################################################
# State Enumerations
################################################################################

class ActuatorStateEnum(Enum):
    """ActuatorStateEnum values from MTConnect model"""

    ACTIVE = auto()  # Actuator is operating.
    INACTIVE = auto()  # Actuator is not operating.


class AlarmStateEnum(Enum):
    """AlarmStateEnum values from MTConnect model"""

    INSTANT = auto()
    ACTIVE = auto()
    CLEARED = auto()


class AxisStateEnum(Enum):
    """AxisStateEnum values from MTConnect model"""

    HOME = auto()  # axis is in its home position.
    TRAVEL = auto()  # axis is in motion.
    PARKED = auto()  # axis has been moved to a fixed position and is being maintained in that posit...
    STOPPED = auto()  # axis is stopped.


class BatteryStateEnum(Enum):
    """BatteryStateEnum values from MTConnect model"""

    CHARGED = auto()  # Component is at it's maximum rated charge level.
    CHARGING = auto()  # Component's charge is increasing.
    DISCHARGING = auto()  # Component's charge is decreasing.
    DISCHARGED = auto()  # Component is at it's minimum charge level.


class ChuckStateEnum(Enum):
    """ChuckStateEnum values from MTConnect model"""

    OPEN = auto()  # Chuck is open to the point of a positive confirmation.
    CLOSED = auto()  # Chuck is closed to the point of a positive confirmation.
    UNLATCHED = auto()  # Chuck is not closed to the point of a positive confirmation and not open to t...


class CompositionStateActionEnum(Enum):
    """CompositionStateActionEnum values from MTConnect model"""

    ACTIVE = auto()  # Composition is operating.
    INACTIVE = auto()  # Composition is not operating.


class CompositionStateLateralEnum(Enum):
    """CompositionStateLateralEnum values from MTConnect model"""

    RIGHT = auto()  # position of the Composition is oriented to the right to the point of a positi...
    LEFT = auto()  # position of the Composition is oriented to the left to the point of a positiv...
    TRANSITIONING = auto()  # position of the Composition is not oriented to the right to the point of a po...


class CompositionStateMotionEnum(Enum):
    """CompositionStateMotionEnum values from MTConnect model"""

    OPEN = auto()  # position of the Composition is open to the point of a positive confirmation.
    UNLATCHED = auto()  # position of the Composition is not open to the point of a positive confirmati...
    CLOSED = auto()  # position of the Composition is closed to the point of a positive confirmation.


class CompositionStateSwitchedEnum(Enum):
    """CompositionStateSwitchedEnum values from MTConnect model"""

    ON = auto()  # activation state of the Composition is in an `ON` condition, it is operating,...
    OFF = auto()  # activation state of the Composition is in an `OFF` condition, it is not opera...


class CompositionStateVerticalEnum(Enum):
    """CompositionStateVerticalEnum values from MTConnect model"""

    UP = auto()  # position of the Composition element is oriented in an upward direction to the...
    DOWN = auto()  # position of the Composition element is oriented in a downward direction to th...
    TRANSITIONING = auto()  # position of the Composition element is not oriented in an upward direction to...


class DoorStateEnum(Enum):
    """DoorStateEnum values from MTConnect model"""

    OPEN = auto()  # Door is open to the point of a positive confirmation.
    CLOSED = auto()  # Door is closed to the point of a positive confirmation.
    UNLATCHED = auto()  # Door is not closed to the point of a positive confirmation and not open to th...


class FileStateEnum(Enum):
    """FileStateEnum values from MTConnect model"""

    EXPERIMENTAL = auto()  # used for processes other than production or otherwise defined.
    PRODUCTION = auto()  # used for production processes.
    REVISION = auto()  # content is modified from `PRODUCTION` or `EXPERIMENTAL`.


class LockStateEnum(Enum):
    """LockStateEnum values from MTConnect model"""

    LOCKED = auto()  # mechanism is engaged and preventing the associated Component from being opene...
    UNLOCKED = auto()  # mechanism is disengaged and the associated Component is able to be opened or ...


class PartProcessingStateEnum(Enum):
    """PartProcessingStateEnum values from MTConnect model"""

    NEEDS_PROCESSING = auto()  # part occurrence is not actively being processed, but the processing has not e...
    IN_PROCESS = auto()  # part occurrence is actively being processed.
    PROCESSING_ENDED = auto()  # part occurrence is no longer being processed. A general state when the reason...
    PROCESSING_ENDED_COMPLETE = auto()  # part occurrence has completed processing successfully.
    PROCESSING_ENDED_STOPPED = auto()  # process has been stopped during the processing. The part occurrence will requ...
    PROCESSING_ENDED_ABORTED = auto()  # processing of the part occurrence has come to a premature end.
    PROCESSING_ENDED_LOST = auto()  # terminal state when the part occurrence has been removed from the equipment b...
    PROCESSING_ENDED_SKIPPED = auto()  # part occurrence has been skipped for processing on the piece of equipment.
    PROCESSING_ENDED_REJECTED = auto()  # part occurrence has been processed completely. However, the processing may ha...
    WAITING_FOR_TRANSIT = auto()  # part occurrence is waiting for transit.
    IN_TRANSIT = auto()  # part occurrence is being transported to its destination.
    TRANSIT_COMPLETE = auto()  # part occurrence has been placed at its designated destination.


class PowerStateEnum(Enum):
    """PowerStateEnum values from MTConnect model"""

    ON = auto()  # source of energy for an entity or the enabling signal providing permission fo...
    OFF = auto()  # source of energy for an entity or the enabling signal providing permission fo...


class ProcessStateEnum(Enum):
    """ProcessStateEnum values from MTConnect model"""

    INITIALIZING = auto()  # device is preparing to execute the process occurrence.
    READY = auto()  # process occurrence is ready to be executed.
    ACTIVE = auto()  # process occurrence is actively executing.
    COMPLETE = auto()  # process occurrence is now finished.
    INTERRUPTED = auto()  # process occurrence has been stopped and may be resumed.
    ABORTED = auto()  # process occurrence has come to a premature end and cannot be resumed.


class RequestStateEnum(Enum):
    """RequestStateEnum values from MTConnect model"""

    NOT_READY = auto()  # requester is not ready to make a request.
    READY = auto()  # requester is prepared to make a request, but no request for service is required.
    ACTIVE = auto()  # requester has initiated a request for a service and the service has not yet b...
    FAIL = auto()  # requester has detected a failure condition.


class ResponseStateEnum(Enum):
    """ResponseStateEnum values from MTConnect model"""

    NOT_READY = auto()  # responder is not ready to perform a service.
    READY = auto()  # responder is prepared to react to a request, but no request for service has b...
    ACTIVE = auto()  # responder has detected and accepted a request for a service and is in the pro...
    COMPLETE = auto()  # responder has completed the actions required to perform the service.
    FAIL = auto()  # responder has detected a failure condition.


class SensorStateDetectEnum(Enum):
    """SensorStateDetectEnum values from MTConnect model"""

    DETECTED = auto()  # sensor is active and the threshold has been met.
    NOT_DETECTED = auto()  # sensor is active and ready but the threshold has not been met.
    UNKNOWN = auto()  # sensor is active, but the state cannot be determined. > Note: unknown covers ...


class TaskStateEnum(Enum):
    """TaskStateEnum values from MTConnect model"""

    INACTIVE = auto()
    PREPARING = auto()
    COMMITTING = auto()
    COMMITTED = auto()
    COMPLETE = auto()
    FAIL = auto()


class ValveStateEnum(Enum):
    """ValveStateEnum values from MTConnect model"""

    OPEN = auto()  # ValveState where flow is allowed and the aperture is static. > Note: For a bi...
    OPENING = auto()  # valve is transitioning from a `CLOSED` state to an `OPEN` state.
    CLOSED = auto()  # ValveState where flow is not possible, the aperture is static, and the valve ...
    CLOSING = auto()  # valve is transitioning from an `OPEN` state to a `CLOSED` state.


class WaitStateEnum(Enum):
    """WaitStateEnum values from MTConnect model"""

    POWERING_UP = auto()  # execution is waiting while the equipment is powering up and is not currently ...
    POWERING_DOWN = auto()  # execution is waiting while the equipment is powering down but has not fully r...
    PART_LOAD = auto()  # execution is waiting while one or more discrete workpieces are being loaded.
    PART_UNLOAD = auto()  # execution is waiting while one or more discrete workpieces are being unloaded.
    TOOL_LOAD = auto()  # execution is waiting while a tool or tooling is being loaded.
    TOOL_UNLOAD = auto()  # execution is waiting while a tool or tooling is being unloaded.
    MATERIAL_LOAD = auto()  # execution is waiting while material is being loaded.
    MATERIAL_UNLOAD = auto()  # execution is waiting while material is being unloaded.
    SECONDARY_PROCESS = auto()  # execution is waiting while another process is completed before the execution ...
    PAUSING = auto()  # execution is waiting while the equipment is pausing but the piece of equipmen...
    RESUMING = auto()  # execution is waiting while the equipment is resuming the production cycle but...



################################################################################
# Mode Enumerations
################################################################################

class ControllerModeEnum(Enum):
    """ControllerModeEnum values from MTConnect model"""

    AUTOMATIC = auto()  # Controller is configured to automatically execute a program.
    MANUAL = auto()  # Controller is not executing an active program. It is capable of receiving ins...
    MANUAL_DATA_INPUT = auto()  # operator can enter a series of operations for the Controller to perform. The ...
    SEMI_AUTOMATIC = auto()  # Controller is operating in a mode that restricts the active program from proc...
    EDIT = auto()  # Controller is currently functioning as a programming device and is not capabl...
    FEED_HOLD = auto()  # axes of the device are commanded to stop, but the spindle continues to function.


class ControllerModeOverrideEnum(Enum):
    """ControllerModeOverrideEnum values from MTConnect model"""

    ON = auto()  # ControllerModeOverride is in the `ON` state and the mode override is active.
    OFF = auto()  # ControllerModeOverride is in the `OFF` state and the mode override is inactive.


class EquipmentModeEnum(Enum):
    """EquipmentModeEnum values from MTConnect model"""

    ON = auto()  # equipment is functioning in the mode designated by the `subType`.
    OFF = auto()  # equipment is not functioning in the mode designated by the `subType`.


class FunctionalModeEnum(Enum):
    """FunctionalModeEnum values from MTConnect model"""

    PRODUCTION = auto()  # Component is currently producing product, ready to produce product, or its cu...
    SETUP = auto()  # Component is not currently producing product. It is being prepared or modifie...
    TEARDOWN = auto()  # Component is not currently producing product. Typically, it has completed the...
    MAINTENANCE = auto()  # Component is not currently producing product. It is currently being repaired,...
    PROCESS_DEVELOPMENT = auto()  # Component is being used to prove-out a new process, testing of equipment or p...


class OperatingModeEnum(Enum):
    """OperatingModeEnum values from MTConnect model"""

    AUTOMATIC = auto()  # automatically execute instructions from a recipe or program. > Note: Setpoint...
    MANUAL = auto()  # execute instructions from an external agent or person. > Note 1 to entry: Val...
    SEMI_AUTOMATIC = auto()  # executes a single instruction from a recipe or program. > Note 1 to entry: Se...


class PathModeEnum(Enum):
    """PathModeEnum values from MTConnect model"""

    INDEPENDENT = auto()  # path is operating independently and without the influence of another path.
    MASTER = auto()  # path provides information or state values that influences the operation of ot...
    SYNCHRONOUS = auto()  # physical or logical parts which are not physically connected to each other bu...
    MIRROR = auto()  # axes associated with the path are mirroring the motion of the `MASTER` path.


class RotaryModeEnum(Enum):
    """RotaryModeEnum values from MTConnect model"""

    SPINDLE = auto()  # axis is functioning as a spindle.
    INDEX = auto()  # axis is configured to index.
    CONTOUR = auto()  # position of the axis is being interpolated.



################################################################################
# Type Enumerations
################################################################################

class ApplicationTypeEnum(Enum):
    """ApplicationTypeEnum values from MTConnect model"""

    DESIGN = auto()  # computer aided design files or drawings.
    DATA = auto()  # generic data.
    DOCUMENTATION = auto()  # documentation regarding a category of file.
    INSTRUCTIONS = auto()  # user instructions regarding the execution of a task.
    LOG = auto()  # data related to the history of a machine or process.
    PRODUCTION_PROGRAM = auto()  # machine instructions to perform a process.


class AssetTypeEnum(Enum):
    """AssetTypeEnum values from MTConnect model"""

    CUTTINGTOOL = auto()  # CuttingTool: CuttingTool Asset type.
    FILE = auto()  # File: File Asset type.
    QIFDOCUMENTWRAPPER = auto()  # QIFDocumentWrapper: QIFDocumentWrapper Asset type.
    RAWMATERIAL = auto()  # RawMaterial: RawMaterial Asset type.
    CUTTINGTOOLARCHETYPE = auto()  # CuttingToolArchetype
    FILEARCHETYPE = auto()  # FileArchetype


class CapabilityTypeEnum(Enum):
    """CapabilityTypeEnum values from MTConnect model"""

    REACH = auto()
    LOAD = auto()
    CAPACITY = auto()
    VOLUME = auto()
    ROTARY_VELOCITY = auto()
    TOLERANCE = auto()


class CollaboratorTypeEnum(Enum):
    """CollaboratorTypeEnum values from MTConnect model"""

    ROBOT = auto()
    CONVEYOR = auto()
    CNC = auto()
    BUFFER = auto()


class CompositionTypeEnum(Enum):
    """CompositionTypeEnum values from MTConnect model"""

    ACTUATOR = auto()  # Composition composed of a mechanism that moves or controls a mechanical part ...
    AMPLIFIER = auto()  # Composition composed of an electronic component or circuit that amplifies pow...
    BALLSCREW = auto()  # Composition composed of a mechanical structure that transforms rotary motion ...
    BELT = auto()  # Composition composed of an endless flexible band that transmits motion for a ...
    BRAKE = auto()  # Composition composed of a mechanism that slows down or stops a moving object ...
    CHAIN = auto()  # Composition composed of an interconnected series of objects that band togethe...
    CHOPPER = auto()  # Composition composed of a mechanism that breaks material into smaller pieces.
    CHUCK = auto()  # Composition composed of a mechanism that holds a part, stock material, or any...
    CHUTE = auto()  # Composition composed of an inclined channel that conveys material.
    CIRCUIT_BREAKER = auto()  # Composition composed of a mechanism that interrupts an electric circuit.
    CLAMP = auto()  # Composition composed of a mechanism that strengthens, supports, or fastens ob...
    COMPRESSOR = auto()  # Composition composed of a pump or other mechanism that reduces volume and inc...
    DOOR = auto()  # Composition composed of a mechanical mechanism or closure that covers a physi...
    DRAIN = auto()  # Composition composed of a mechanism that allows material to flow for the purp...
    ENCODER = auto()  # Composition composed of a mechanism that measures rotary position.
    EXPOSURE_UNIT = auto()  # Composition composed of a mechanism that emits a type of radiation.
    EXTRUSION_UNIT = auto()  # Composition composed of a mechanism that dispenses liquid or powered materials.
    FAN = auto()  # Composition composed of a mechanism that produces a current of air.
    FILTER = auto()  # Composition composed of a substance or structure that allows liquids or gases...
    GALVANOMOTOR = auto()  # Composition composed of an electromechanical actuator that produces deflectio...
    GRIPPER = auto()  # Composition composed of a mechanism that holds a part, stock material, or any...
    HOPPER = auto()  # Composition composed of a chamber or bin that stores materials temporarily, t...
    LINEAR_POSITION_FEEDBACK = auto()  # Composition composed of a mechanism that measures linear motion or position.
    MOTOR = auto()  # Composition composed of a mechanism that converts electrical, pneumatic, or h...
    OIL = auto()  # Composition composed of a viscous liquid.
    POWER_SUPPLY = auto()  # Composition composed of a unit that provides power to electric mechanisms.
    PULLEY = auto()  # Composition composed of a mechanism or wheel that turns in a frame or block a...
    PUMP = auto()  # Composition composed of an apparatus that raises, drives, exhausts, or compre...
    REEL = auto()  # Composition composed of a rotary storage unit for material.
    SENSING_ELEMENT = auto()  # Composition composed of a mechanism that provides a signal or measured value.
    SPREADER = auto()  # Composition composed of a mechanism that flattens or spreads materials.
    STORAGE_BATTERY = auto()  # Composition composed of one or more cells that converts chemical energy to el...
    SWITCH = auto()  # Composition composed of a mechanism that turns on or off an electric current ...
    TABLE = auto()  # Composition composed of a surface that holds an object or material.
    TANK = auto()  # Composition composed of a receptacle or container that holds material.
    TENSIONER = auto()  # Composition composed of a mechanism that provides or applies a stretch or str...
    TRANSFORMER = auto()  # Composition composed of a mechanism that transforms electric energy from a so...
    VALVE = auto()  # Composition composed of a mechanism that halts or controls the flow of a liqu...
    VAT = auto()  # Composition composed of a container for liquid or powdered materials.
    WATER = auto()  # Composition composed of a fluid.
    WIRE = auto()  # Composition composed of a string like piece or filament of relatively rigid o...
    WORKPIECE = auto()  # Composition composed of an object or material on which a form of work is perf...
    COOLING_TOWER = auto()  # Composition composed of a heat exchange system that uses a fluid to transfer ...
    POT = auto()  # Composition composed of a tool storage location associated with a ToolMagazin...
    STATION = auto()  # Composition composed of a storage or mounting location for a tool associated ...
    TRANSFER_ARM = auto()  # Composition composed of a mechanism that physically moves a tool from one loc...
    TRANSFER_POT = auto()  # Pot for a tool awaiting transfer from a ToolMagazine to spindle or Turret.
    RETURN_POT = auto()  # Pot for a tool removed from spindle or Turret and awaiting for return to a To...
    STAGING_POT = auto()  # Pot for a tool awaiting transfer to a ToolMagazine or Turret from outside of ...
    REMOVAL_POT = auto()  # Pot for a tool to be removed from a ToolMagazine or Turret to a location outs...
    EXPIRED_POT = auto()  # Pot for a tool that is no longer usable for removal from a ToolMagazine or Tu...


class CoordinateSystemTypeEnum(Enum):
    """CoordinateSystemTypeEnum values from MTConnect model"""

    WORLD = auto()  # stationary coordinate system referenced to earth, which is independent of the...
    BASE = auto()  # coordinate system referenced to the base mounting surface. {{cite(ISO 9787:20...
    OBJECT = auto()  # coordinate system referenced to the object. {{cite(ISO 9787:2013
    TASK = auto()  # coordinate system referenced to the site of the task. {{cite(ISO 9787:2013
    MECHANICAL_INTERFACE = auto()  # coordinate system referenced to the mechanical interface. {{cite(ISO 9787:2013
    TOOL = auto()  # coordinate system referenced to the tool or to the end effector attached to t...
    MOBILE_PLATFORM = auto()  # coordinate system referenced to one of the components of a mobile platform. {...
    MACHINE = auto()  # coordinate system referenced to the home position and orientation of the prim...
    CAMERA = auto()  # coordinate system referenced to the sensor which monitors the site of the tas...


class CountDirectionTypeEnum(Enum):
    """
    Enumeration for countDirection types.
    """

    UP = auto()  # tool life counts up from zero to the maximum.
    DOWN = auto()  # tool life counts down from the maximum to zero.


class CriticalityTypeEnum(Enum):
    """CriticalityTypeEnum values from MTConnect model"""

    CRITICAL = auto()  # services or functions provided by the associated element is required for the ...
    NONCRITICAL = auto()  # services or functions provided by the associated element is not required for ...


class CutterStatusTypeEnum(Enum):
    """
    Enumeration for CutterStatus values.
    """

    NEW = auto()  # new tool that has not been used or first use. Marks the start of the tool his...
    AVAILABLE = auto()  # tool is available for use. If this is not present, the tool is currently not ...
    UNAVAILABLE = auto()  # tool is unavailable for use in metal removal.
    ALLOCATED = auto()  # tool is has been committed to a piece of equipment for use and is not availab...
    UNALLOCATED = auto()  # tool has not been committed to a process and can be allocated.
    MEASURED = auto()  # tool has been measured.
    RECONDITIONED = auto()  # tool has been reconditioned.
    USED = auto()  # tool is in process and has remaining tool life.
    EXPIRED = auto()  # tool has reached the end of its useful life.
    BROKEN = auto()  # premature tool failure.
    NOT_REGISTERED = auto()  # tool cannot be used until it is entered into the system.
    UNKNOWN = auto()  # tool is an indeterminate state. This is the default value.


class DataItemRelationshipTypeEnum(Enum):
    """DataItemRelationshipTypeEnum values from MTConnect model"""

    ATTACHMENT = auto()  # reference to a DataItem that associates the values with an external entity.
    COORDINATE_SYSTEM = auto()  # referenced DataItem provides the `id` of the effective Coordinate System.
    LIMIT = auto()  # referenced DataItem provides process limits.
    OBSERVATION = auto()  # referenced DataItem provides the observed values.


class FormatTypeEnum(Enum):
    """
    Enumeration for CuttingToolDefinition format values.
    """

    EXPRESS = auto()  # document will confirm to the ISO 10303 Part 21 standard.
    TEXT = auto()  # document will be a text representation of the tool data.
    UNDEFINED = auto()  # document will be provided in an undefined format.
    XML = auto()  # default value for the definition. The content will be an XML document.


class LocationTypeEnum(Enum):
    """
    Enumeration for Location types
    """

    POT = auto()  # number of the pot in the tool handling system.
    STATION = auto()  # tool location in a horizontal turning machine.
    CRIB = auto()  # location with regard to a tool crib.
    SPINDLE = auto()  # location associated with a spindle.
    TRANSFER_POT = auto()  # location for a tool awaiting transfer from a tool magazine to spindle or a tu...
    RETURN_POT = auto()  # location for a tool removed from a spindle or turret and awaiting return to a...
    STAGING_POT = auto()  # location for a tool awaiting transfer to a tool magazine or turret from outsi...
    REMOVAL_POT = auto()  # location for a tool removed from a tool magazine or turret awaiting transfer ...
    EXPIRED_POT = auto()  # location for a tool that is no longer usable and is awaiting removal from a t...
    END_EFFECTOR = auto()  # location associated with an end effector.


class MediaTypeEnum(Enum):
    """MediaTypeEnum values from MTConnect model"""

    STEP = auto()  # ISO 10303 STEP AP203 or AP242 format.
    STL = auto()  # STereoLithography file format.
    GDML = auto()  # Geometry Description Markup Language.
    OBJ = auto()  # Wavefront OBJ file format.
    COLLADA = auto()  # ISO 17506.
    IGES = auto()  # Initial Graphics Exchange Specification.
    _3DS = auto()  # 3DS: Autodesk file format.
    ACIS = auto()  # Dassault file format.
    X_T = auto()  # Parasolid XT Siemens data interchange format.
    QIF_MBD = auto()  # provides the 3D geometric boundary representation used to associate with prod...


class MotionActuationTypeEnum(Enum):
    """MotionActuationTypeEnum values from MTConnect model"""

    DIRECT = auto()  # movement is initiated by the component.
    VIRTUAL = auto()  # motion is computed and is used for expressing an imaginary movement.
    NONE = auto()  # no actuation of this axis. > Note: Actuation of `NONE` can be either a derive...


class MotionTypeEnum(Enum):
    """MotionTypeEnum values from MTConnect model"""

    PRISMATIC = auto()  # sliding linear motion along an axis with a fixed range of motion.
    CONTINUOUS = auto()  # revolves around an axis with a continuous range of motion.
    REVOLUTE = auto()  # rotates around an axis with a fixed range of motion.
    FIXED = auto()  # axis does not move.


class PartCountTypeEnum(Enum):
    """PartCountTypeEnum values from MTConnect model"""

    EACH = auto()  # count is of individual items.
    BATCH = auto()  # pre-specified group of items.


class PowerSourceTypeEnum(Enum):
    """PowerSourceTypeEnum values from MTConnect model"""

    PRIMARY = auto()  # main or principle.
    SECONDARY = auto()  # alternate or not primary.
    STANDBY = auto()  # held near at hand and ready for use and is uninterruptible.


class ProgramLocationTypeEnum(Enum):
    """ProgramLocationTypeEnum values from MTConnect model"""

    LOCAL = auto()  # managed by the controller.
    EXTERNAL = auto()  # not managed by the controller.


class QIFDocumentTypeEnum(Enum):
    """QIFDocumentTypeEnum values from MTConnect model"""

    MEASUREMENT_RESOURCE = auto()
    PLAN = auto()
    PRODUCT = auto()
    RESULTS = auto()
    RULES = auto()
    STATISTICS = auto()


class RelationshipTypeEnum(Enum):
    """RelationshipTypeEnum values from MTConnect model"""

    PARENT = auto()  # functions as a parent in the relationship with the associated element.
    CHILD = auto()  # functions as a child in the relationship with the associated element.
    PEER = auto()  # functions as a peer which provides equal functionality and capabilities in th...


class RoleTypeEnum(Enum):
    """RoleTypeEnum values from MTConnect model"""

    SYSTEM = auto()  # associated element performs the functions of a System for this element.
    AUXILIARY = auto()  # associated element performs the functions as an `Auxiliary` for this element.


class ScopeTypeEnum(Enum):
    """ScopeTypeEnum values from MTConnect model"""

    ENTITY = auto()  # scope or context is directly upon the source itself.
    VALUE_PROPERTY = auto()  # scope or context is upon a value property of the source.
    PART = auto()  # scope or context is upon a part or a child of the source.


class SpecificationRelationshipTypeEnum(Enum):
    """SpecificationRelationshipTypeEnum values from MTConnect model"""

    LIMIT = auto()  # referenced Specification provides process limits.


class TaskTypeEnum(Enum):
    """TaskTypeEnum values from MTConnect model"""

    MOVE_MATERIAL = auto()
    MATERIAL_UNLOAD = auto()
    TOOL_CHANGE = auto()


class UncertaintyTypeEnum(Enum):
    """UncertaintyTypeEnum values from MTConnect model"""

    COMBINED = auto()  # combined standard uncertainty.
    MEAN = auto()  # standard uncertainty using arithmetic mean or average the observations. {{cit...



################################################################################
# Other Enumerations
################################################################################

class AlarmCodeEnum(Enum):
    """AlarmCodeEnum values from MTConnect model"""

    CRASH = auto()  # spindle crashed.
    JAM = auto()  # component jammed.
    FAILURE = auto()  # component failed.
    FAULT = auto()  # fault occurred on the component.
    STALLED = auto()  # component has stalled and cannot move.
    OVERLOAD = auto()  # component is overloaded.
    ESTOP = auto()  # ESTOP button was pressed.
    MATERIAL = auto()  # problem with the material.
    MESSAGE = auto()  # system message.
    OTHER = auto()  # alarm is not in any of the above categories.


class AlarmSeverityEnum(Enum):
    """AlarmSeverityEnum values from MTConnect model"""

    CRITICAL = auto()
    ERROR = auto()
    WARNING = auto()
    INFORMATION = auto()


class ApplicationCategoryEnum(Enum):
    """ApplicationCategoryEnum values from MTConnect model"""

    ASSEMBLY = auto()  # files regarding the fully assembled product.
    DEVICE = auto()  # device related files.
    HANDLING = auto()  # files relating to the handling of material.
    MAINTENANCE = auto()  # files relating to equipment maintenance.
    PART = auto()  # files relating to a part.
    PROCESS = auto()  # files related to the manufacturing process.
    INSPECTION = auto()  # files related to the quality inspection.
    SETUP = auto()  # files related to the setup of a process.


class AvailabilityEnum(Enum):
    """AvailabilityEnum values from MTConnect model"""

    AVAILABLE = auto()  # data source is active and capable of providing data.
    UNAVAILABLE = auto()  # data source is either inactive or not capable of providing data.


class AxisCouplingEnum(Enum):
    """AxisCouplingEnum values from MTConnect model"""

    TANDEM = auto()  # axes are physically connected to each other and operate as a single unit.
    SYNCHRONOUS = auto()  # axes are not physically connected to each other but are operating together in...
    MASTER = auto()  # axis is the master of the CoupledAxes.
    SLAVE = auto()  # axis is a slave to the CoupledAxes.


class AxisInterlockEnum(Enum):
    """AxisInterlockEnum values from MTConnect model"""

    ACTIVE = auto()  # axis lockout function is activated, power has been removed from the axis, and...
    INACTIVE = auto()  # axis lockout function has not been activated, the axis may be powered, and th...


class CharacteristicStatusEnum(Enum):
    """CharacteristicStatusEnum values from MTConnect model"""

    _PASS = auto()  # PASS: measurement is within acceptable tolerances.
    FAIL = auto()  # measurement is not within acceptable tolerances.
    REWORK = auto()  # failed, but acceptable constraints achievable by utilizing additional manufac...
    SYSTEM_ERROR = auto()  # measurement is indeterminate due to an equipment failure.
    INDETERMINATE = auto()  # measurement cannot be determined.
    NOT_ANALYZED = auto()  # measurement cannot be evaluated.
    BASIC_OR_THEORETIC_EXACT_DIMENSION = auto()  # nominal provided without tolerance limits. {{cite(QIF 3:2018 5.10.2.6
    UNDEFINED = auto()  # status of measurement cannot be determined.


class ChuckInterlockEnum(Enum):
    """ChuckInterlockEnum values from MTConnect model"""

    ACTIVE = auto()  # chuck cannot be unclamped.
    INACTIVE = auto()  # chuck can be unclamped.


class CodeEnum(Enum):
    """CodeEnum values from MTConnect model"""

    BDX = auto()  # largest diameter of the body of a tool item.
    LBX = auto()  # distance measured along the X axis from that point of the item closest to the...
    APMX = auto()  # maximum engagement of the cutting edge or edges with the workpiece measured p...
    DC = auto()  # maximum diameter of a circle on which the defined point Pk of each of the mas...
    DF = auto()  # dimension between two parallel tangents on the outside edge of a flange.
    OAL = auto()  # largest length dimension of the cutting tool including the master insert wher...
    DMM = auto()  # dimension of the diameter of a cylindrical portion of a tool item or an adapt...
    H = auto()  # dimension of the height of the shank.
    LS = auto()  # dimension of the length of the shank.
    LUX = auto()  # maximum length of a cutting tool that can be used in a particular cutting ope...
    LPR = auto()  # dimension from the yz-plane to the furthest point of the tool item or adaptiv...
    WT = auto()  # total weight of the cutting tool in grams. The force exerted by the mass of t...
    LF = auto()  # distance from the gauge plane or from the end of the shank to the furthest po...
    CRP = auto()  # theoretical sharp point of the cutting tool from which the major functional d...
    L = auto()  # theoretical length of the cutting edge of a cutting item over sharp corners.
    DRVA = auto()  # angle between the driving mechanism locator on a tool item and the main cutti...
    WF = auto()  # distance between the cutting reference point and the rear backing surface of ...
    IC = auto()  # diameter of a circle to which all edges of a equilateral and round regular in...
    SIG = auto()  # angle between the major cutting edge and the same cutting edge rotated by 180...
    KAPR = auto()  # angle between the tool cutting edge plane and the tool feed plane measured in...
    PSIR = auto()  # angle between the tool cutting edge plane and a plane perpendicular to the to...
    N_A = auto()  # N/A: angle of the tool with respect to the workpiece for a given process. The valu...
    BS = auto()  # measure of the length of a wiper edge of a cutting item.
    SDLX = auto()  # SDLx: length of a portion of a stepped tool that is related to a corresponding cutt...
    STAX = auto()  # STAx: angle between a major edge on a step of a stepped tool and the same cutting e...
    DCX = auto()  # DCx: diameter of a circle on which the defined point Pk located on this cutting to...
    HF = auto()  # distance from the basal plane of the tool item to the cutting point.
    RE = auto()  # nominal radius of a rounded corner measured in the X Y-plane.
    LFX = auto()  # LFx: distance from the gauge plane or from the end of the shank of the cutting too...
    BCH = auto()  # flat length of a chamfer.
    CHW = auto()  # width of the chamfer.
    W1 = auto()  # insert width when an inscribed circle diameter is not practical.


class ConnectionStatusEnum(Enum):
    """ConnectionStatusEnum values from MTConnect model"""

    CLOSED = auto()  # no connection at all.
    LISTEN = auto()  # agent is waiting for a connection request from an adapter.
    ESTABLISHED = auto()  # open connection. The normal state for the data transfer phase of the connection.


class CoordinateSystemEnum(Enum):
    """CoordinateSystemEnum values from MTConnect model"""

    MACHINE = auto()  # unchangeable coordinate system that has machine zero as its origin.
    WORK = auto()  # coordinate system that represents the working area for a particular workpiece...


class DirectionEnum(Enum):
    """DirectionEnum values from MTConnect model"""

    CLOCKWISE = auto()  # clockwise rotation using the right-hand rule.
    COUNTER_CLOCKWISE = auto()  # counter-clockwise rotation using the right-hand rule.
    POSITIVE = auto()
    NEGATIVE = auto()


class DirectionLinearEnum(Enum):
    """DirectionLinearEnum values from MTConnect model"""

    POSITIVE = auto()  # linear position is increasing.
    NEGATIVE = auto()  # linear position is decreasing.
    NONE = auto()  # no direction.


class DirectionRotaryEnum(Enum):
    """DirectionRotaryEnum values from MTConnect model"""

    CLOCKWISE = auto()  # clockwise rotation using the right-hand rule.
    COUNTER_CLOCKWISE = auto()  # counter-clockwise rotation using the right-hand rule.
    NONE = auto()  # no direction.


class EmergencyStopEnum(Enum):
    """EmergencyStopEnum values from MTConnect model"""

    ARMED = auto()  # emergency stop circuit is complete and the piece of equipment, component, or ...
    TRIGGERED = auto()  # operation of the piece of equipment, component, or composition is inhibited.


class EndOfBarEnum(Enum):
    """EndOfBarEnum values from MTConnect model"""

    YES = auto()  # EndOfBar has been reached.
    NO = auto()  # EndOfBar has not been reached.


class ErrorCodeEnum(Enum):
    """ErrorCodeEnum values from MTConnect model"""

    ASSET_NOT_FOUND = auto()  # request for information specifies an Asset that is not recognized by the agent.
    INTERNAL_ERROR = auto()  # agent experienced an error while attempting to published the requested inform...
    INVALID_REQUEST = auto()  # request contains information that was not recognized by the agent.
    INVALID_URI = auto()  # URI provided was incorrect.
    INVALID_XPATH = auto()  # XPath identified in the request for information could not be parsed correctly...
    NO_DEVICE = auto()  # identity of the Device specified in the request for information is not associ...
    OUT_OF_RANGE = auto()  # request for information specifies streaming data that includes sequence numbe...
    QUERY_ERROR = auto()  # agent was unable to interpret the query. The query parameters do not contain ...
    TOO_MANY = auto()  # `count` parameter provided in the request for information requires either of ...
    UNAUTHORIZED = auto()  # requester does not have sufficient permissions to access the requested inform...
    UNSUPPORTED = auto()  # valid request was provided, but the agent does not support the feature or typ...


class ExceptionCodeEnum(Enum):
    """ExceptionCodeEnum values from MTConnect model"""

    TYPE_MISMATCH = auto()  # scope value type is mismatched. > Note: For example, a `string` instead of an...
    NOT_FOUND = auto()  # scope is missing a property or a part.
    DEPRECATED = auto()  # scope has been deprecated.
    EXTENDED = auto()  # scope is considered an extension of the MTConnect Standard.
    OUT_OF_RANGE = auto()  # scope is not within the expected range.
    DUPLICATE_ENTRY = auto()  # scope is a duplicate or has duplicate properties or parts.
    INVALID_FORMAT = auto()  # scope has either an invalid format or does not conform to the expected pattern.


class ExecutionEnum(Enum):
    """ExecutionEnum values from MTConnect model"""

    READY = auto()  # Component is ready to execute instructions. It is currently idle.
    ACTIVE = auto()  # Component is actively executing an instruction.
    INTERRUPTED = auto()  # Component suspends the execution of the program due to an external signal. Ac...
    FEED_HOLD = auto()  # motion of the active axes are commanded to stop at their current position.
    STOPPED = auto()  # Component program is not `READY` to execute.
    OPTIONAL_STOP = auto()  # command from the program has intentionally interrupted execution. The Compone...
    PROGRAM_STOPPED = auto()  # command from the program has intentionally interrupted execution. Action is r...
    PROGRAM_COMPLETED = auto()  # program completed execution.
    WAIT = auto()  # Component suspends execution while a secondary operation executes. Execution ...
    PROGRAM_OPTIONAL_STOP = auto()  # program has been intentionally optionally stopped using an M01 or similar cod...


class FilterEnum(Enum):
    """FilterEnum values from MTConnect model"""

    MINIMUM_DELTA = auto()  # new value **MUST NOT** be reported for a data item unless the measured value ...
    PERIOD = auto()  # data reported for a data item is provided on a periodic basis. The `PERIOD` f...


class FormEnum(Enum):
    """FormEnum values from MTConnect model"""

    BAR = auto()
    SHEET = auto()
    BLOCK = auto()
    CASTING = auto()
    POWDER = auto()
    LIQUID = auto()
    GEL = auto()
    FILAMENT = auto()
    GAS = auto()


class GuardResult(Enum):
    """GuardResult values from MTConnect model"""

    _CONTINUE = auto()  # CONTINUE
    SKIP = auto()
    RUN = auto()


class LeakDetectEnum(Enum):
    """LeakDetectEnum values from MTConnect model"""

    DETECTED = auto()  # leak is currently being detected.
    NOT_DETECTED = auto()  # leak is currently not being detected.


class MaintenanceListDirectionEnum(Enum):
    """MaintenanceListDirectionEnum values from MTConnect model"""

    UP = auto()
    DOWN = auto()


class MaintenanceListIntervalEnum(Enum):
    """MaintenanceListIntervalEnum values from MTConnect model"""

    ABSOLUTE = auto()
    INCREMENTAL = auto()


class NativeUnitEnum(Enum):
    """NativeUnitEnum values from MTConnect model"""

    CENTIPOISE = auto()  # viscosity in centipoise.
    DEGREE_MINUTE = auto()  # DEGREE/MINUTE: rotational velocity in degree per minute.
    FAHRENHEIT = auto()  # temperature in Fahrenheit.
    FOOT = auto()  # length in foot.
    FOOT_MINUTE = auto()  # FOOT/MINUTE: speed in foot per minute.
    FOOT_SECOND = auto()  # FOOT/SECOND: speed in foot per second.
    FOOT_SECOND_2 = auto()  # FOOT/SECOND^2: acceleration in foot per second squared.
    FOOT_3D = auto()  # point in space identified by X, Y, and Z positions and represented by a space...
    GALLON_MINUTE = auto()  # GALLON/MINUTE: volumetric flow in gallon per minute.
    HOUR = auto()  # time in hour.
    INCH = auto()  # length in inch.
    INCH_MINUTE = auto()  # INCH/MINUTE: speed in inch per minute.
    INCH_SECOND = auto()  # INCH/SECOND: speed in inch per second.
    INCH_SECOND_2 = auto()  # INCH/SECOND^2: acceleration in inch per second squared.
    INCH_POUND = auto()  # torque in inch pound.
    INCH_3D = auto()  # point in space identified by X, Y, and Z positions and represented by a space...
    KELVIN = auto()  # temperature in Kelvin.
    KILOWATT = auto()  # power in kilowatt.
    KILOWATT_HOUR = auto()  # energy in kilowatt-hour.
    LITER_MINUTE = auto()  # LITER/MINUTE: volumetric flow in liter per minute.
    MILLIMETER_MINUTE = auto()  # MILLIMETER/MINUTE: speed in millimeter per minute.
    MINUTE = auto()  # time in minute.
    OTHER = auto()  # unsupported unit.
    POUND = auto()  # mass in pound.
    POUND_INCH_2 = auto()  # POUND/INCH^2: pressure in pound per square inch (PSI).
    RADIAN = auto()  # angle in radian.
    RADIAN_MINUTE = auto()  # RADIAN/MINUTE: angular velocity in radian per minute.
    RADIAN_SECOND = auto()  # RADIAN/SECOND: angular velocity in radian per second.
    RADIAN_SECOND_2 = auto()  # RADIAN/SECOND^2: angular acceleration in radian per second squared.
    BAR = auto()  # pressure in bar.
    TORR = auto()  # pressure in torr.
    MILLIMETER_MERCURY = auto()  # pressure in millimeter of mercury (mmHg).
    PASCAL_MINUTE = auto()  # PASCAL/MINUTE: pressurization rate in pascal per minute.
    GRAVITATIONAL_FORCE = auto()  # `MASS` times `GRAVITATIONAL_ACCELERATION` (g).
    GRAVITATIONAL_ACCELERATION = auto()  # acceleration relative to earth's gravity given in meter per second squared. >...
    AMPERE_HOUR = auto()  # electric charge in ampere hour.
    CUBIC_FOOT_HOUR = auto()  # CUBIC_FOOT/HOUR: change of geometric volume in cubic foot per hour.
    CUBIC_FOOT_MINUTE = auto()  # CUBIC_FOOT/MINUTE: change of geometric volume in cubic foot per minute.
    SQUARE_INCH = auto()  # geometric area in inch squared.
    CUBIC_FOOT = auto()  # geometric volume in cubic foot.
    INCH_REVOLUTION = auto()  # INCH/REVOLUTION: feedrate per revolution in inch per revolution.
    MICROMETER = auto()  # length in micrometer.
    RANKINE = auto()  # temperature in Rankine.
    MICROTORR = auto()  # pressure in microtorr.


class NetworkWirelessEnum(Enum):
    """NetworkWirelessEnum values from MTConnect model"""

    YES = auto()
    NO = auto()


class OriginatorEnum(Enum):
    """OriginatorEnum values from MTConnect model"""

    MANUFACTURER = auto()  # manufacturer of a piece of equipment or Component.
    USER = auto()  # owner or implementer of a piece of equipment or Component.


class PartDetectEnum(Enum):
    """PartDetectEnum values from MTConnect model"""

    PRESENT = auto()  # part or work piece is detected or is present.
    NOT_PRESENT = auto()  # part or work piece is not detected or is not present.


class PartStatusEnum(Enum):
    """PartStatusEnum values from MTConnect model"""

    _PASS = auto()  # PASS: part conforms to given requirements.
    FAIL = auto()  # part does not conform to some given requirements.


class PowerStatusEnum(Enum):
    """PowerStatusEnum values from MTConnect model"""

    ON = auto()
    OFF = auto()


class ProgramEditEnum(Enum):
    """ProgramEditEnum values from MTConnect model"""

    ACTIVE = auto()  # Controller is in the program edit mode.
    READY = auto()  # Controller is capable of entering the program edit mode and no function is in...
    NOT_READY = auto()  # Controller is being inhibited by a function from entering the program edit mode.


class QualityEnum(Enum):
    """QualityEnum values from MTConnect model"""

    VALID = auto()  # observation is valid against the MTConnect Standard.
    UNVERIFIABLE = auto()  # observation cannot be validated.
    INVALID = auto()  # observation is not valid against the MTConnect Standard according to the vali...


class QueryParameterEnum(Enum):
    """QueryParameterEnum values from MTConnect model"""

    DEVICE = auto()  # device: See `device` parameter of Agent::Operation types.
    DEVICETYPE = auto()  # deviceType: See `deviceType` parameter of Agent::Operation types.
    PATH = auto()  # path: See `path` parameter of Agent::Operation types.
    _FROM = auto()  # from: See `from` parameter of Agent::Operation types.
    COUNT = auto()  # count: See `count` parameter of Agent::Operation types.
    INTERVAL = auto()  # interval: See `interval` parameter of Agent::Operation types.
    HEARTBEAT = auto()  # heartbeat: See `heartbeat` parameter of Agent::Operation types.


class ResetTriggerEnum(Enum):
    """ResetTriggerEnum values from MTConnect model"""

    ACTION_COMPLETE = auto()  # observation of the DataItem that is measuring an action or operation is to be...
    ANNUAL = auto()  # observation of the DataItem is to be reset at the end of a 12-month period.
    DAY = auto()  # observation of the DataItem is to be reset at the end of a 24-hour period.
    LIFE = auto()  # observation of the DataItem is not reset and accumulates for the entire life ...
    MAINTENANCE = auto()  # observation of the DataItem is to be reset upon completion of a maintenance e...
    MONTH = auto()  # observation of the DataItem is to be reset at the end of a monthly period.
    POWER_ON = auto()  # observation of the DataItem is to be reset when power was applied to the piec...
    SHIFT = auto()  # observation of the DataItem is to be reset at the end of a work shift.
    WEEK = auto()  # observation of the DataItem is to be reset at the end of a 7-day period.


class ResetTriggeredEnum(Enum):
    """ResetTriggeredEnum values from MTConnect model"""

    ACTION_COMPLETE = auto()  # Observation::result is measuring an action or operation was reset upon comple...
    ANNUAL = auto()  # Observation::result was reset at the end of a 12-month period.
    DAY = auto()  # Observation::result was reset at the end of a 24-hour period.
    MAINTENANCE = auto()  # Observation::result was reset upon completion of a maintenance event.
    MANUAL = auto()  # Observation::result was reset based on a physical reset action.
    MONTH = auto()  # Observation::result was reset at the end of a monthly period.
    POWER_ON = auto()  # Observation::result was reset when power was applied to the piece of equipmen...
    SHIFT = auto()  # Observation::result was reset at the end of a work shift.
    WEEK = auto()  # Observation::result was reset at the end of a 7-day period.


class SeverityEnum(Enum):
    """SeverityEnum values from MTConnect model"""

    FATAL = auto()  # exception violates compliance with the MTConnect Standard and validation can ...
    ERROR = auto()  # exception violates compliance with the MTConnect Standard.
    WARNING = auto()  # exception **MAY** violate compliance with the MTConnect Standard.
    INFO = auto()  # exception is considered informative.


class SpindleInterlockEnum(Enum):
    """SpindleInterlockEnum values from MTConnect model"""

    ACTIVE = auto()  # power has been removed and the spindle cannot be operated.
    INACTIVE = auto()  # spindle has not been deactivated.


class StatisticEnum(Enum):
    """StatisticEnum values from MTConnect model"""

    AVERAGE = auto()  # mathematical average value calculated for the data item during the calculatio...
    KURTOSIS = auto()  # **DEPRECATED** in *Version 1.6*. ~~A measure of the "peakedness" of a probabi...
    MAXIMUM = auto()  # maximum or peak value recorded for the data item during the calculation period.
    MEDIAN = auto()  # middle number of a series of numbers.
    MINIMUM = auto()  # minimum value recorded for the data item during the calculation period.
    MODE = auto()  # number in a series of numbers that occurs most often.
    RANGE = auto()  # difference between the maximum and minimum value of a data item during the ca...
    ROOT_MEAN_SQUARE = auto()  # mathematical Root Mean Square (RMS) value calculated for the data item during...
    STANDARD_DEVIATION = auto()  # statistical Standard Deviation value calculated for the data item during the ...


class ToolLifeEnum(Enum):
    """ToolLifeEnum values from MTConnect model"""

    MINUTES = auto()  # tool life measured in minutes. All units for minimum, maximum, and nominal **...
    PART_COUNT = auto()  # tool life measured in parts. All units for minimum, maximum, and nominal **MU...
    WEAR = auto()  # tool life measured in tool wear. Wear **MUST** be provided in millimeters as ...


class UnitEnum(Enum):
    """UnitEnum values from MTConnect model"""

    AMPERE = auto()  # electric current in ampere.
    CELSIUS = auto()  # temperature in degree Celsius.
    COUNT = auto()  # count of something.
    DECIBEL = auto()  # sound level in decibel.
    DEGREE = auto()  # angle in degree.
    DEGREE_3D = auto()  # space-delimited, floating-point representation of the angular rotation in deg...
    DEGREE_SECOND = auto()  # DEGREE/SECOND: angular velocity in degree per second.
    DEGREE_SECOND_2 = auto()  # DEGREE/SECOND^2: angular acceleration in degree per second squared.
    HERTZ = auto()  # frequency in cycles per second.
    JOULE = auto()  # energy in joule.
    KILOGRAM = auto()  # mass in kilogram.
    LITER = auto()  # volume in liter.
    LITER_SECOND = auto()  # LITER/SECOND: volumetric flow in liter per second.
    MICRO_RADIAN = auto()  # tilt in micro radian.
    MILLIMETER = auto()  # length in millimeter.
    MILLIMETER_3D = auto()  # point in space identified by X, Y, and Z positions and represented by a space...
    MILLIMETER_REVOLUTION = auto()  # MILLIMETER/REVOLUTION: feedrate per revolution in millimeter per revolution.
    MILLIMETER_SECOND = auto()  # MILLIMETER/SECOND: speed in millimeter per second.
    MILLIMETER_SECOND_2 = auto()  # MILLIMETER/SECOND^2: acceleration in millimeter per second squared.
    NEWTON = auto()  # force in newton.
    NEWTON_METER = auto()  # torque in newton-meter.
    OHM = auto()  # electrical resistance in ohm.
    PASCAL = auto()  # pressure or stress in pascal.
    PASCAL_SECOND = auto()  # viscosity in pascal-second.
    PERCENT = auto()  # amount in or for every hundred.
    PH = auto()  # acidity or alkalinity of a solution in pH.
    REVOLUTION_MINUTE = auto()  # REVOLUTION/MINUTE: rotational velocity in revolution per minute.
    SECOND = auto()  # time in second.
    SIEMENS_METER = auto()  # SIEMENS/METER: electrical conductivity in siemens per meter.
    VOLT = auto()  # electric potential, electric potential difference or electromotive force in v...
    VOLT_AMPERE = auto()  # apparent power in an electrical circuit, equal to the product of root-mean-sq...
    VOLT_AMPERE_REACTIVE = auto()  # reactive power in an AC electrical circuit (commonly referred to as VAR) in v...
    WATT = auto()  # power in watt.
    WATT_SECOND = auto()  # electrical energy in watt-second
    GRAM_CUBIC_METER = auto()  # GRAM/CUBIC_METER: density in gram per cubic meter.
    CUBIC_MILLIMETER = auto()  # geometric volume in millimeter.
    CUBIC_MILLIMETER_SECOND = auto()  # CUBIC_MILLIMETER/SECOND: change of geometric volume per second.
    CUBIC_MILLIMETER_SECOND_2 = auto()  # CUBIC_MILLIMETER/SECOND^2: change in geometric volume per second squared.
    MILLIGRAM = auto()  # mass in milligram.
    MILLIGRAM_CUBIC_MILLIMETER = auto()  # MILLIGRAM/CUBIC_MILLIMETER: density in milligram per cubic millimeter.
    MILLILITER = auto()  # volume in milliliter.
    COUNT_SECOND = auto()  # COUNT/SECOND: frequency in count per second.
    PASCAL_SECOND_2 = auto()  # PASCAL/SECOND: pressurization rate in pascal per second.
    UNIT_VECTOR_3D = auto()  # 3D Unit Vector. Space delimited list of three floating point numbers.
    REVOLUTION_SECOND_2 = auto()  # REVOLUTION/SECOND^2: rotational acceleration in revolution per second squared.
    REVOLUTION_SECOND = auto()  # REVOLUTION/SECOND: rotational velocity in revolution per second.
    GRAM = auto()  # mass in gram.
    METER_SECOND_2 = auto()  # METER/SECOND^2: acceleration in meter per second squared.
    COULOMB = auto()  # electric charge in coulomb.
    CUBIC_METER = auto()  # geometric volume in meter.
    SQUARE_MILLIMETER = auto()  # geometric area in millimeter.
    OHM_METER = auto()  # resistivity in ohm-meter.

