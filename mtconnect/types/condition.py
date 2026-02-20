"""
MTConnect CONDITION Category Types

All CONDITION type DataItems and related enumerations from MTConnect v2.6
normative model. Conditions represent fault or alarm states with
hierarchical severity levels.

Reference: MTConnect Standard v2.6 Normative Model - ConditionEnum
Auto-generated from: model_2.6.xml
"""

from enum import Enum, auto



class ConditionType(Enum):
    """CONDITION types from MTConnect ConditionEnum"""
    COMMUNICATIONS = auto()  # indication that the piece of equipment has experienced a communications failure.
    DATA_RANGE = auto()  # indication that the value of the data associated with a measured value or a c...
    LOGIC_PROGRAM = auto()  # indication that an error occurred in the logic program or programmable logic ...
    MOTION_PROGRAM = auto()  # indication that an error occurred in the motion program associated with a pie...
    SYSTEM = auto()  # general purpose indication associated with an electronic component of a piece...
    ACTUATOR = auto()  # indication of a fault associated with an actuator.


class ConditionLevel(Enum):
    """MTConnect condition severity levels in hierarchical order"""
    NORMAL = auto()  # condition state that indicates operation within specified limits.
    WARNING = auto()  # condition state that requires concern and supervision and may become hazardou...
    FAULT = auto()  # condition state that requires intervention to continue operation to function ...
    UNAVAILABLE = auto()  # Condition status cannot be determined


class ConditionQualifier(Enum):
    """MTConnect condition qualifiers for additional context"""
    HIGH = auto()  # measured value is greater than the expected value for a process variable.
    LOW = auto()  # measured value is less than the expected value for a process variable.
