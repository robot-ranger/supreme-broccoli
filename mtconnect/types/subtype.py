"""
MTConnect DataItem SubTypes

All DataItem subType values from MTConnect v2.6 normative model.
SubTypes qualify the specific aspect of a DataItem type being measured.

Reference: MTConnect Standard v2.6 Normative Model - DataItemSubTypeEnum
Auto-generated from: model_2.6.xml
"""

from enum import Enum, auto



class DataItemSubType(Enum):
    """DataItem subType values from MTConnect DataItemSubTypeEnum"""
    ABSOLUTE = auto()  # relating to or derived in the simplest manner from the fundamental units or m...
    ACTION = auto()  # indication of the operating state of a mechanism.
    ACTUAL = auto()  # reported value of an observation.
    ALL = auto()  # all actions, items, or activities being counted independent of the outcome.
    ALTERNATING = auto()  # measurement of alternating voltage or current. If not specified further in st...
    A_SCALE = auto()  # A-Scale weighting factor on the frequency scale.
    AUXILIARY = auto()  # when multiple locations on a piece of bar stock being feed by a bar feeder ar...
    BAD = auto()  # actions, items, or activities being counted that do not conform to specificat...
    BRINELL = auto()  # scale to measure the resistance to deformation of a surface.
    B_SCALE = auto()  # B-Scale weighting factor on the frequency scale.
    COMMANDED = auto()  # directive value including adjustments such as an offset or overrides.
    CONSUMED = auto()  # amount of material consumed from an object or container during a manufacturin...
    CONTROL = auto()  # state of the enabling signal or control logic that enables or disables the fu...
    C_SCALE = auto()  # C-Scale weighting factor on the frequency scale.
    DELAY = auto()  # elapsed time of a temporary halt of action.
    DIRECT = auto()  # DC current or voltage. **DEPRECATED** in *Version 1.6*.
    DRY_RUN = auto()  # setting or operator selection used to execute a test mode to confirm the exec...
    D_SCALE = auto()  # D-Scale weighting factor on the frequency scale.
    EXPIRATION = auto()  # relating to the expiration or end of useful life for a material or other phys...
    FIRST_USE = auto()  # relating to the first use of a material or other physical item.
    GOOD = auto()  # actions, items, or activities being counted that conform to specification or ...
    INCREMENTAL = auto()  # relating to or derived from the last observation.
    JOG = auto()  # relating to momentary activation of a function or a movement. **DEPRECATION W...
    LATERAL = auto()  # indication of the position of a mechanism that may move in a lateral direction.
    LEEB = auto()  # scale to measure the elasticity of a surface.
    LENGTH = auto()  # reference to a length type tool offset variable.
    LINE = auto()  # state of the power source.
    LINEAR = auto()  # direction of motion of a linear motion.
    LOADED = auto()  # indication that the subparts of a piece of equipment are under load.
    MACHINE_AXIS_LOCK = auto()  # setting or operator selection that changes the behavior of the controller on ...
    MAIN = auto()  # relating to the primary logic or motion program currently being executed.
    MAINTENANCE = auto()  # relating to maintenance on the piece of equipment.
    MANUAL_UNCLAMP = auto()  # indication of the state of an operator controlled interlock that can inhibit ...
    MANUFACTURE = auto()  # related to the production of a material or other physical item.
    MAXIMUM = auto()  # maximum value.
    MINIMUM = auto()  # minimum value.
    MOHS = auto()  # scale to measure the resistance to scratching of a surface.
    MOTION = auto()  # indication of the open or closed state of a mechanism.
    NO_SCALE = auto()  # no weighting factor on the frequency scale.
    OPERATING = auto()  # piece of equipment that is powered or performing any activity.
    OPERATOR = auto()  # relating to the person currently responsible for operating the piece of equip...
    OPTIONAL_STOP = auto()  # setting or operator selection that changes the behavior of the controller on ...
    OVERRIDE = auto()  # overridden value.
    POWERED = auto()  # piece of equipment is powered and functioning or Component that are required ...
    PRIMARY = auto()  # main or principle.
    PROBE = auto()  # position provided by a measurement probe. **DEPRECATION WARNING**: May be dep...
    PROCESS = auto()  # relating to production of a part or product on a piece of equipment.
    PROGRAMMED = auto()  # directive value without offsets and adjustments.
    RADIAL = auto()  # reference to a radial type tool offset variable.
    RAPID = auto()  # performing an operation faster or in less time than nominal rate.
    REMAINING = auto()  # remaining measure or count of an action, object or activity.
    ROCKWELL = auto()  # scale to measure the resistance to deformation of a surface.
    ROTARY = auto()  # direction of a rotary motion using the right hand rule convention.
    SCHEDULE = auto()  # identity of a control program that is used to specify the order of execution ...
    SET_UP = auto()  # relating to the preparation of a piece of equipment for production or restori...
    SHORE = auto()  # scale to measure the resistance to deformation of a surface.
    SINGLE_BLOCK = auto()  # setting or operator selection that changes the behavior of the controller on ...
    STANDARD = auto()  # standard measure of an object or an action.
    START = auto()  # boundary when an activity or an event commences.
    SWITCHED = auto()  # indication of the activation state of a mechanism represented by a Composition.
    TARGET = auto()  # goal of the operation or process.
    TARGET_COMPLETION = auto()  # relating to the end or completion of an activity or event.
    TOOL_CHANGE_STOP = auto()  # setting or operator selection that changes the behavior of the controller on ...
    USEABLE = auto()  # remaining usable measure of an object or action.
    VERTICAL = auto()  # indication of the position of a mechanism that may move in a vertical direction.
    VICKERS = auto()  # scale to measure the resistance to deformation of a surface.
    WORKING = auto()  # piece of equipment performing any activity, the equipment is active and perfo...
    IPV4_ADDRESS = auto()  # IPV4 network address of the Component.
    IPV6_ADDRESS = auto()  # IPV6 network address of the Component.
    GATEWAY = auto()  # Gateway for the Component network.
    SUBNET_MASK = auto()  # SubNet mask for the Component network.
    VLAN_ID = auto()  # layer2 Virtual Local Network (VLAN) ID for the Component network.
    MAC_ADDRESS = auto()  # Media Access Control Address. The unique physical address of the network hard...
    WIRELESS = auto()  # identifies whether the connection type is wireless.
    LICENSE = auto()  # license code to validate or activate the hardware or software.
    VERSION = auto()  # version of the hardware or software.
    RELEASE_DATE = auto()  # date the hardware or software was released for general use.
    INSTALL_DATE = auto()  # date the hardware or software was installed.
    MANUFACTURER = auto()  # corporate identity for the maker of the hardware or software.
    UUID = auto()  # universally unique identifier as specified in ISO 11578 or RFC 4122.
    SERIAL_NUMBER = auto()  # serial number that uniquely identifies a specific part.
    RAW_MATERIAL = auto()  # material that is used to produce parts.
    LOT = auto()  # group of parts tracked as a lot.
    BATCH = auto()  # group of parts produced in a batch.
    HEAT_TREAT = auto()  # material heat number.
    PART_NUMBER = auto()  # particular part design or model.
    PART_FAMILY = auto()  # group of parts having similarities in geometry, manufacturing process, and/or...
    PART_NAME = auto()  # word or set of words by which a part is known, addressed, or referred to.
    PROCESS_STEP = auto()  # step in the process plan that this occurrence corresponds to.
    PROCESS_PLAN = auto()  # process plan that a process occurrence belongs to.
    ORDER_NUMBER = auto()  # authorization of a process occurrence.
    PROCESS_NAME = auto()  # word or set of words by which a process being executed (process occurrence) b...
    ISO_STEP_EXECUTABLE = auto()  # reference to a ISO 10303 Executable.
    COMPLETE = auto()  # associated with the completion of an activity or event.
    ACTIVE = auto()  # relating to logic or motion program currently executing.
    FAILED = auto()  # actions or activities that were attempted , but failed to complete or resulte...
    ABORTED = auto()  # actions or activities that were attempted, but terminated before they could b...
    ENDED = auto()  # boundary when an activity or an event terminates.
    WASTE = auto()  # amount discarded.
    PART = auto()  # amount included in the part.
    REQUEST = auto()  # request by an Interface for a task.
    RESPONSE = auto()  # response by an Interface to a request for a task.
    ACTIVITY = auto()  # phase or segment of a recipe or program.
    SEGMENT = auto()  # phase of a recipe process.
    RECIPE = auto()  # process as part of product production; can be a subprocess of a larger process.
    OPERATION = auto()  # step of a discrete manufacturing process.
    BINARY = auto()  # observed as a binary data type.
    BOOLEAN = auto()  # observed as a boolean data type.
    ENUMERATED = auto()  # observed as a set containing a restricted number of discrete values where eac...
    DETECT = auto()  # indicated by the presence or existence of something.
    MODEL = auto()  # model info of the hardware or software.
    MEASURED = auto()  # {{def(DataItemSubType::ACTUAL that has uncertainty.
    GAS = auto()  # fluid that has no definite shape or volume.
    LIQUID = auto()  # fluid that has a definite volume but no definite shape.
    SOLID = auto()  # matter that has a definite shape and a definite volume.
