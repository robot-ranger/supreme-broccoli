"""
MTConnect CONDITION Category Types

All CONDITION type DataItems and related enumerations from MTConnect v2.6 normative model.
Conditions represent fault or alarm states with hierarchical severity levels.

Reference: MTConnect Standard v2.6 Normative Model - ConditionEnum
"""

from enum import Enum, auto


class ConditionType(Enum):
    """CONDITION types from MTConnect ConditionEnum"""
    ACTUATOR = auto()  # Indication of a fault associated with an actuator
    COMMUNICATIONS = auto()  # Piece of equipment has experienced a communications failure
    DATA_RANGE = auto()  # Value associated with a measured value or calculated value is out of range
    LOGIC_PROGRAM = auto()  # Error occurred in the logic program or programmable logic controller (PLC)
    MOTION_PROGRAM = auto()  # Error occurred in the motion program associated with a piece of equipment
    SYSTEM = auto()  # General purpose indication associated with electronic component


class ConditionLevel(Enum):
    """MTConnect condition severity levels in hierarchical order"""
    NORMAL = auto()  # No condition exists
    WARNING = auto()  # Cautionary condition that may lead to a fault
    FAULT = auto()  # Failure condition that requires intervention
    UNAVAILABLE = auto()  # Condition status cannot be determined


class ConditionQualifier(Enum):
    """MTConnect condition qualifiers for additional context"""
    HIGH = auto()  # Condition is above acceptable limit
    LOW = auto()  # Condition is below acceptable limit
