"""
MTConnect Models

Structural elements representing MTConnect components, data items, assets,
and their relationships.

Reference: MTConnect Standard v2.6 - Device Information Model
"""

# Component models
from mtconnect.models.components import (
    Component,
    Description,
    Device,
    Controller,
    Axes,
    Linear,
    Rotary,
    Spindle,
    Path,
    Systems,
    Coolant,
    Electric,
    Hydraulic,
    Pneumatic,
    Lubrication,
    Door,
    Chuck,
    Auxiliaries,
)

# DataItem models
from mtconnect.models.data_items import (
    DataItem,
    DataItemCategory,
    Constraints,
    SampleDataItem,
    EventDataItem,
    ConditionDataItem,
    create_data_item,
)

# Asset models
from mtconnect.models.assets import (
    Asset,
    AssetType,
    CuttingTool,
    CuttingToolLifeCycle,
    ToolLife,
    ToolLifeType,
    ToolLifeDirection,
    CutterStatus,
    Location,
    Measurement,
    Part,
    PartStatus,
    RawMaterial,
    MaterialType,
    File,
    FileState,
    QIFDocumentWrapper,
)

# Observation value models
from mtconnect.models.values import (
    ObservationValue,
    SampleValue,
    EventValue,
    ConditionObservation,
    UnavailableType,
    TimeSeries,
    DataSet,
)

# Relationship models
from mtconnect.models.relationships import (
    ComponentRef,
    DataItemRef,
    AssetRef,
    RelationshipType,
    Composition,
    CompositionType,
    CoordinateSystem,
    SpecificationLimits,
    ControlLimits,
    AlarmLimits,
)

__all__ = [
    # Components
    "Component",
    "Description",
    "Device",
    "Controller",
    "Axes",
    "Linear",
    "Rotary",
    "Spindle",
    "Path",
    "Systems",
    "Coolant",
    "Electric",
    "Hydraulic",
    "Pneumatic",
    "Lubrication",
    "Door",
    "Chuck",
    "Auxiliaries",
    # DataItems
    "DataItem",
    "DataItemCategory",
    "Constraints",
    "SampleDataItem",
    "EventDataItem",
    "ConditionDataItem",
    "create_data_item",
    # Assets
    "Asset",
    "AssetType",
    "CuttingTool",
    "CuttingToolLifeCycle",
    "ToolLife",
    "ToolLifeType",
    "ToolLifeDirection",
    "CutterStatus",
    "Location",
    "Measurement",
    "Part",
    "PartStatus",
    "RawMaterial",
    "MaterialType",
    "File",
    "FileState",
    "QIFDocumentWrapper",
    # Values
    "ObservationValue",
    "SampleValue",
    "EventValue",
    "ConditionObservation",
    "UnavailableType",
    "TimeSeries",
    "DataSet",
    # Relationships
    "ComponentRef",
    "DataItemRef",
    "AssetRef",
    "RelationshipType",
    "Composition",
    "CompositionType",
    "CoordinateSystem",
    "SpecificationLimits",
    "ControlLimits",
    "AlarmLimits",
]
