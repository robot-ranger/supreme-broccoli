"""
MTConnect CONDITION Category Types

All CONDITION type DataItems from MTConnect v2.6 normative model (ConditionEnum).
Conditions report the health status of components with hierarchical severity levels.

Condition severity hierarchy: NORMAL < WARNING < FAULT < UNAVAILABLE

Reference: MTConnect Standard v2.6 Normative Model - ConditionEnum
"""

from enum import Enum, auto


class ConditionType(Enum):
    """All CONDITION types from MTConnect v2.6 normative model"""
    ACTUATOR = auto()  # Indication of a fault associated with an actuator
    COMMUNICATIONS = auto()  # Indication that equipment has experienced a communications failure
    DATA_RANGE = auto()  # Indication that measured value or calculation is outside expected range
    LOGIC_PROGRAM = auto()  # Indication of error in logic program or PLC
    MOTION_PROGRAM = auto()  # Indication of error in motion program
    SYSTEM = auto()  # General purpose indication of electronic component fault


class ConditionLevel(Enum):
    """MTConnect condition severity levels in hierarchical order"""
    NORMAL = auto()  # Normal operating state
    WARNING = auto()  # Warning condition that may require attention
    FAULT = auto()  # Fault condition requiring intervention
    UNAVAILABLE = auto()  # Status unavailable or unknown


__all__ = ['ConditionType', 'ConditionLevel']


class ConditionQualifier(Enum):
    """Optional qualifiers for condition values"""
    HIGH = auto()
    LOW = auto()


__all__ = ['ConditionType', 'ConditionLevel', 'ConditionQualifier']
