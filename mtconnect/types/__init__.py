"""
MTConnect Type Definitions

All MTConnect enumerations for DataItem types, subtypes, primitives, and other
standard enumerations from the MTConnect v2.6 normative model.

Reference: MTConnect Standard v2.6 Normative Model
"""

# DataItem type enumerations by category
from mtconnect.types.event import EventType
from mtconnect.types.sample import SampleType
from mtconnect.types.condition import ConditionType, ConditionLevel, ConditionQualifier
from mtconnect.types.subtype import DataItemSubType

# Primitive datatypes with validation
from mtconnect.types.primitives import (
    MTCBoolean,
    MTCString,
    MTCInteger,
    MTCFloat,
    MTCDouble,
    MTCBinary,
    Int32,
    Int64,
    UInt32,
    UInt64,
    ID,
    UUID,
    MTCDateTime,
    Version,
    XLinkType,
    XLinkHref,
    XSLang,
    X509,
    MTCArray,
    Float3D,
    Second,
    validate_primitive,
    convert_to_primitive,
)

__all__ = [
    # DataItem types
    "EventType",
    "SampleType",
    "ConditionType",
    "ConditionLevel",
    "ConditionQualifier",
    "DataItemSubType",
    # Primitives
    "MTCBoolean",
    "MTCString",
    "MTCInteger",
    "MTCFloat",
    "MTCDouble",
    "MTCBinary",
    "Int32",
    "Int64",
    "UInt32",
    "UInt64",
    "ID",
    "UUID",
    "MTCDateTime",
    "Version",
    "XLinkType",
    "XLinkHref",
    "XSLang",
    "X509",
    "MTCArray",
    "Float3D",
    "Second",
    "validate_primitive",
    "convert_to_primitive",
]
