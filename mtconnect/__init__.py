"""
MTConnect Python Package

Provides standardized MTConnect v2.6 types, enums, and models for building
adapters, clients, and agents.

Reference: MTConnect Standard v2.6 - https://model.mtconnect.org
"""

__version__ = "2.6.0"

# Re-export key types and enums for convenience
from mtconnect.types import (
    EventType,
    SampleType,
    ConditionType,
    ConditionLevel,
    ConditionQualifier,
    DataItemSubType,
)

__all__ = [
    "__version__",
    "EventType",
    "SampleType",
    "ConditionType",
    "ConditionLevel",
    "ConditionQualifier",
    "DataItemSubType",
]
