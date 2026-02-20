"""
MTConnect DataItem SubType Values

All DataItem subType values from MTConnect v2.6 normative model (DataItemSubTypeEnum).
SubTypes provide additional specificity to DataItem types (e.g., POSITION with subType ACTUAL).

Reference: MTConnect Standard v2.6 Normative Model - DataItemSubTypeEnum
"""

from enum import Enum, auto


class DataItemSubType(Enum):
    """All DataItem subType values from MTConnect v2.6 normative model"""
    ABORTED = auto()  # Actions or activities that were attempted, but terminated before completion
    ABSOLUTE = auto()  # Relating to or derived in the simplest manner from fundamental units
    ACTIVE = auto()  # Relating to logic or motion program currently executing
    ACTION = auto()  # Indication of the operating state of a mechanism
    ACTUAL = auto()  # Reported value of an observation
    ACTIVITY = auto()  # Phase or segment of a recipe or program
    ALL = auto()  # All actions, items, or activities being counted independent of outcome
    ALTERNATING = auto()  # Measurement of alternating voltage or current (DEPRECATED in v1.6)
    A_SCALE = auto()  # A-Scale weighting factor on the frequency scale
    AUXILIARY = auto()  # Multiple locations on bar stock feed indicating end of piece reached
    BAD = auto()  # Actions, items, or activities that do not conform to specification
    BATCH = auto()  # Group of parts produced in a batch
    BINARY = auto()  # Observed as a binary data type
    BOOLEAN = auto()  # Observed as a boolean data type
    BRINELL = auto()  # Scale to measure resistance to deformation of a surface
    B_SCALE = auto()  # B-Scale weighting factor on the frequency scale
    COMMANDED = auto()  # Directive value including adjustments such as offsets or overrides
    COMPLETE = auto()  # Associated with the completion of an activity or event
    CONSUMED = auto()  # Amount of material consumed from object or container during manufacturing
    CONTROL = auto()  # State of enabling signal or control logic for entity function
    C_SCALE = auto()  # C-Scale weighting factor on the frequency scale
    DELAY = auto()  # Elapsed time of a temporary halt of action
    DETECT = auto()  # Indicated by the presence or existence of something
    DIRECT = auto()  # DC current or voltage (DEPRECATED in v1.6)
    DRY_RUN = auto()  # Setting or operator selection to execute test mode
    D_SCALE = auto()  # D-Scale weighting factor on the frequency scale
    ENDED = auto()  # Boundary when an activity or event terminates
    ENUMERATED = auto()  # Observed as a set containing restricted discrete named values
    EXPIRATION = auto()  # Relating to expiration or end of useful life
    FAILED = auto()  # Actions or activities that were attempted but failed
    FIRST_USE = auto()  # Relating to first use of material or physical item
    GATEWAY = auto()  # Gateway for the Component network
    GOOD = auto()  # Actions, items, or activities that conform to specification
    HEAT_TREAT = auto()  # Material heat number
    INCREMENTAL = auto()  # Relating to or derived from the last observation
    INSTALL_DATE = auto()  # Date the hardware or software was installed
    IPV4_ADDRESS = auto()  # IPV4 network address of the Component
    IPV6_ADDRESS = auto()  # IPV6 network address of the Component
    ISO_STEP_EXECUTABLE = auto()  # Reference to an ISO 10303 Executable
    JOG = auto()  # Relating to momentary activation of function or movement
    LATERAL = auto()  # Indication of position of mechanism that may move laterally
    LEEB = auto()  # Scale to measure elasticity of a surface
    LENGTH = auto()  # Reference to a length type tool offset variable
    LICENSE = auto()  # License code to validate or activate hardware or software
    LINE = auto()  # State of the power source
    LINEAR = auto()  # Direction of motion of a linear motion
    LOADED = auto()  # Indication that subparts of equipment are under load
    LOT = auto()  # Group of parts tracked as a lot
    MAC_ADDRESS = auto()  # Media Access Control Address - unique physical address of network hardware
    MACHINE_AXIS_LOCK = auto()  # Setting or operator selection that changes controller behavior
    MAIN = auto()  # Relating to primary logic or motion program currently executing
    MAINTENANCE = auto()  # Relating to maintenance on the piece of equipment
    MANUAL_UNCLAMP = auto()  # State of operator controlled interlock inhibiting unclamp action
    MANUFACTURE = auto()  # Related to production of material or physical item
    MANUFACTURER = auto()  # Corporate identity for maker of hardware or software
    MAXIMUM = auto()  # Maximum value
    MEASURED = auto()  # Actual value that has uncertainty
    MINIMUM = auto()  # Minimum value
    MODEL = auto()  # Model info of the hardware or software
    MOHS = auto()  # Scale to measure resistance to scratching of a surface
    MOTION = auto()  # Indication of open or closed state of a mechanism
    NO_SCALE = auto()  # No weighting factor on the frequency scale
    OPERATION = auto()  # Step of a discrete manufacturing process
    OPERATING = auto()  # Piece of equipment that is powered or performing any activity
    OPERATOR = auto()  # Relating to person currently responsible for operating equipment
    OPTIONAL_STOP = auto()  # Setting or operator selection that changes controller behavior
    ORDER_NUMBER = auto()  # Authorization of a process occurrence
    OVERRIDE = auto()  # Overridden value
    PART = auto()  # Amount included in the part
    PART_FAMILY = auto()  # Group of parts having similarities in geometry, manufacturing, or functions
    PART_NAME = auto()  # Word or set of words by which a part is known or addressed
    PART_NUMBER = auto()  # Particular part design or model
    POWERED = auto()  # Equipment is powered and functioning or required components remain on
    PRIMARY = auto()  # Main or principle
    PROBE = auto()  # Position provided by a measurement probe
    PROCESS = auto()  # Relating to production of part or product on equipment
    PROCESS_NAME = auto()  # Word or set of words by which a process occurrence is known
    PROCESS_PLAN = auto()  # Process plan that a process occurrence belongs to
    PROCESS_STEP = auto()  # Step in the process plan that this occurrence corresponds to
    PROGRAMMED = auto()  # Directive value without offsets and adjustments
    RADIAL = auto()  # Reference to a radial type tool offset variable
    RAPID = auto()  # Performing operation faster or in less time than nominal rate
    RAW_MATERIAL = auto()  # Material that is used to produce parts
    RECIPE = auto()  # Process as part of product production; can be subprocess of larger process
    RELEASE_DATE = auto()  # Date hardware or software was released for general use
    REMAINING = auto()  # Remaining measure or count of an action, object or activity
    REQUEST = auto()  # Request by an Interface for a task
    RESPONSE = auto()  # Response by an Interface to a request for a task
    ROCKWELL = auto()  # Scale to measure resistance to deformation of a surface
    ROTARY = auto()  # Direction of rotary motion using right hand rule convention
    SCHEDULE = auto()  # Identity of control program specifying order of execution of other programs
    SEGMENT = auto()  # Phase of a recipe process
    SERIAL_NUMBER = auto()  # Serial number that uniquely identifies a specific part
    SET_UP = auto()  # Relating to preparation of equipment for production or restoring to neutral state
    SHORE = auto()  # Scale to measure resistance to deformation of a surface
    SINGLE_BLOCK = auto()  # Setting or operator selection that changes controller behavior
    STANDARD = auto()  # Standard measure of an object or an action
    START = auto()  # Boundary when an activity or event commences
    SUBNET_MASK = auto()  # SubNet mask for the Component network
    SWITCHED = auto()  # Indication of activation state of mechanism represented by Composition
    TARGET = auto()  # Goal of the operation or process
    TARGET_COMPLETION = auto()  # Relating to the end or completion of an activity or event
    TOOL_CHANGE_STOP = auto()  # Setting or operator selection that changes controller behavior
    USEABLE = auto()  # Remaining usable measure of an object or action
    UUID = auto()  # Universally unique identifier as specified in ISO 11578 or RFC 4122
    VERSION = auto()  # Version of the hardware or software
    VERTICAL = auto()  # Indication of position of mechanism that may move vertically
    VICKERS = auto()  # Scale to measure resistance to deformation of a surface
    VLAN_ID = auto()  # Layer2 Virtual Local Network (VLAN) ID for Component network
    WASTE = auto()  # Amount discarded
    WIRELESS = auto()  # Identifies whether the connection type is wireless
    WORKING = auto()  # Equipment performing any activity, active and performing function under load or not


__all__ = ['DataItemSubType']
