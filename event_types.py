"""
MTConnect EVENT Category Types

All EVENT type DataItems from MTConnect v2.6 normative model (EventEnum).
Events report discrete, non-numeric functional states or information with two or more values.

Reference: MTConnect Standard v2.6 Normative Model - EventEnum
"""

from enum import Enum, auto


class EventType(Enum):
    """All EVENT types from MTConnect v2.6 normative model"""
    ACTIVE_AXES = auto()  # Set of axes currently associated with a Path or Controller
    ADAPTER_SOFTWARE_VERSION = auto()  # Adapter software version
    ADAPTER_URI = auto()  # URI of the adapter
    ACTUATOR_STATE = auto()  # Operational state of an apparatus for moving or controlling a mechanism or system
    ALARM_LIMITS = auto()  # Set of limits used to trigger warning or alarm indicators
    APPLICATION = auto()  # Application on a Component
    ASSET_CHANGED = auto()  # AssetId of the Asset that has been changed
    ASSET_REMOVED = auto()  # AssetId of the Asset that has been removed
    AVAILABILITY = auto()  # Agent's ability to communicate with the data source
    AXIS_COUPLING = auto()  # Describes the way axes will be associated to each other
    AXIS_FEEDRATE_OVERRIDE = auto()  # Value of a signal to adjust the feedrate of an individual linear type axis
    AXIS_INTERLOCK = auto()  # State of the axis lockout function when power has been removed
    AXIS_STATE = auto()  # State of a Linear or Rotary component representing an axis
    BLOCK = auto()  # Line of code or command being executed by a Controller entity
    BLOCK_COUNT = auto()  # Total count of blocks of program code executed since execution started
    CHUCK_INTERLOCK = auto()  # State of an interlock function for the associated Chuck component
    CHUCK_STATE = auto()  # Operating state of a mechanism that holds a part or stock material
    CONNECTION_STATUS = auto()  # Status of the connection between an adapter and an agent
    COMPOSITION_STATE = auto()  # Composition operating state
    CONTROL_LIMITS = auto()  # Set of limits used to indicate whether a process variable is stable
    CONTROLLER_MODE = auto()  # Current mode of the Controller component
    CONTROLLER_MODE_OVERRIDE = auto()  # Setting or operator selection that changes equipment behavior
    COUPLED_AXES = auto()  # Set of associated axes
    DATE_CODE = auto()  # Time and date code associated with a material or physical item
    DEVICE_ADDED = auto()  # UUID of new device added to an MTConnect Agent
    DEVICE_REMOVED = auto()  # UUID of a device removed from an MTConnect Agent
    DEVICE_CHANGED = auto()  # UUID of the device whose metadata has changed
    DEVICE_UUID = auto()  # Identifier of another piece of equipment temporarily associated
    DIRECTION = auto()  # Direction of motion
    DOOR_STATE = auto()  # Operational state of a Door component or composition element
    EMERGENCY_STOP = auto()  # State of the emergency stop signal
    END_OF_BAR = auto()  # Indication that end of bar stock has been reached
    EQUIPMENT_MODE = auto()  # Equipment performing specific types of activities
    EXECUTION = auto()  # Operating state of a Component
    FIRMWARE = auto()  # Embedded software of a Component
    FUNCTIONAL_MODE = auto()  # Current intended production status of the Component
    HARDWARE = auto()  # Hardware of a Component
    HARDNESS = auto()  # Hardness of a material
    LIBRARY = auto()  # Software library on a Component
    LINE_LABEL = auto()  # Identifier for a Block of code in a Program
    LINE_NUMBER = auto()  # Position of a block of program code within a control program
    LOAD_COUNT = auto()  # Accumulation of load operation attempts
    MATERIAL = auto()  # Identifier of a material used or consumed in manufacturing
    MATERIAL_LAYER = auto()  # Layers of material applied in additive manufacturing
    MTCONNECT_VERSION = auto()  # Reference version of the MTConnect Standard supported by the adapter
    MESSAGE = auto()  # Information to be transferred from equipment to client software
    NETWORK = auto()  # Network details of a Component
    OPERATOR_ID = auto()  # Identifier of the person currently responsible for operating the equipment
    OPERATING_SYSTEM = auto()  # Operating System of a Component
    PALLET_ID = auto()  # Identifier for a pallet
    PART_COUNT = auto()  # Aggregate count of parts
    PART_DETECT = auto()  # Indication whether a part or work piece has been detected or is present
    PART_GROUP_ID = auto()  # Identifier given to a collection of individual parts
    PART_ID = auto()  # Identifier of a part in a manufacturing operation
    PART_KIND_ID = auto()  # Identifier given to link individual occurrence to a class of parts
    PART_STATUS = auto()  # State or condition of a part
    PART_UNIQUE_ID = auto()  # Identifier given to a distinguishable, individual part
    PATH_FEEDRATE_OVERRIDE = auto()  # Value of a signal to adjust feedrate for axes associated with a Path
    PATH_MODE = auto()  # Operational relationship between Path entities
    POWER_STATE = auto()  # Status of the source of energy or state of enabling signal
    PROCESS_AGGREGATE_ID = auto()  # Identifier given to link individual occurrence to a group of related occurrences
    PROCESS_KIND_ID = auto()  # Identifier given to link individual occurrence to a class of processes
    PROCESS_OCCURRENCE_ID = auto()  # Identifier of a process being executed by the device
    PROCESS_TIME = auto()  # Time and date associated with an activity or event
    PROGRAM = auto()  # Name of the logic or motion program being executed by Controller
    PROGRAM_COMMENT = auto()  # Comment or non-executable statement in the control program
    PROGRAM_EDIT = auto()  # Status of the Controller program editing mode
    PROGRAM_EDIT_NAME = auto()  # Name of the program being edited
    PROGRAM_HEADER = auto()  # Non-executable header section of the control program
    PROGRAM_LOCATION = auto()  # URI for the source file associated with Program
    PROGRAM_LOCATION_TYPE = auto()  # Defines whether program is executed from local memory or outside source
    PROGRAM_NEST_LEVEL = auto()  # Nesting level within control program currently being executed
    ROTATION = auto()  # Three space angular displacement relative to a cartesian coordinate system
    ROTARY_MODE = auto()  # Current operating mode for a Rotary type axis
    ROTARY_VELOCITY_OVERRIDE = auto()  # Percentage change to velocity of programmed velocity for Rotary axis
    SENSOR_ATTACHMENT = auto()  # Attachment between a sensor and an entity
    SERIAL_NUMBER = auto()  # Serial number associated with a Component, Asset, or Device
    SPECIFICATION_LIMITS = auto()  # Set of limits defining acceptable performance range for a variable
    SPINDLE_INTERLOCK = auto()  # Status of the spindle when power removed and free to rotate
    TOOL_ASSET_ID = auto()  # Identifier of an individual tool asset
    TOOL_GROUP = auto()  # Identifier for the tool group associated with a specific tool
    TOOL_NUMBER = auto()  # Identifier assigned by Controller to a cutting tool when in use
    TOOL_OFFSET = auto()  # Reference to the tool offset variables applied to active cutting tool
    TRANSLATION = auto()  # Three space linear displacement relative to a cartesian coordinate system
    UNLOAD_COUNT = auto()  # Accumulation of unload operation attempts
    USER = auto()  # Identifier of the person currently responsible for operating equipment
    VARIABLE = auto()  # Data whose meaning may change over time
    WAIT_STATE = auto()  # Indication of the reason that Execution is reporting WAIT
    WIRE = auto()  # Identifier for the type of wire used as cutting mechanism
    WORKHOLDING_ID = auto()  # Identifier for current workholding or part clamp in use
    WORK_OFFSET = auto()  # Reference to offset variables for a work piece or part


__all__ = ['EventType']
