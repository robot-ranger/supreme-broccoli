"""
MTConnect Models

Structural elements representing MTConnect components, data items, assets,
compositions, and references.

Relationships (ConfigurationRelationship) exist only in configurations.

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

# Configuration models
from mtconnect.models.configurations import (
    Configuration,
    Specification,
    SensorConfiguration,
    SolidModel,
    Motion,
    ConfigurationRelationship,
    ImageFile,
    PowerSource,
    CoordinateSystem,
    ConfigSpecificationLimits,
    ConfigControlLimits,
    ConfigAlarmLimits,
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
    SpecificationLimitsValue,
    ControlLimitsValue,
    AlarmLimitsValue,
)

# Composition models
from mtconnect.models.compositions import (
    Composition,
    CompositionType,
)

# Reference models
from mtconnect.models.references import (
    ComponentRef,
    DataItemRef,
    AssetRef,
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
    # Configuration
    "Configuration",
    "Specification",
    "SensorConfiguration",
    "SolidModel",
    "Motion",
    "ConfigurationRelationship",
    "ImageFile",
    "PowerSource",
    "CoordinateSystem",
    "ConfigSpecificationLimits",
    "ConfigControlLimits",
    "ConfigAlarmLimits",
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
    "SpecificationLimitsValue",
    "ControlLimitsValue",
    "AlarmLimitsValue",
    # References
    "ComponentRef",
    "DataItemRef",
    "AssetRef",
    # Compositions
    "Composition",
    "CompositionType",
]
