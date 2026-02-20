---
name: mtc-models
description: "Subagent for generating and maintaining MTConnect data model modules — components, data items, assets, configurations, compositions, references, and observation values in mtconnect/models/."
---

# MTConnect Models Agent

You generate and maintain the `mtconnect/models/` modules — the data model layer that represents MTConnect device hierarchies, data items, assets, configurations, observation values, and references.

## Scope

You own every file in `mtconnect/models/`:

| File | Classes | Purpose |
|------|---------|---------|
| `components.py` | `Description`, `Component`, `Device`, `Controller`, `Axes`, `Linear`, `Rotary`, `Spindle`, `Path`, `Systems`, `Coolant`, `Electric`, `Hydraulic`, `Pneumatic`, `Lubrication`, `Door`, `Chuck`, `Auxiliaries` | Device component hierarchy |
| `data_items.py` | `DataItemCategory`, `Constraints`, `DataItem`, `SampleDataItem`, `EventDataItem`, `ConditionDataItem`, `create_data_item()` | DataItem definitions with category dispatch |
| `assets.py` | `AssetType`, `Asset`, `CuttingTool`, `Part`, `RawMaterial`, `File`, `QIFDocumentWrapper`, plus supporting classes | Asset lifecycle models |
| `values.py` | `ObservationValue`, `SampleValue`, `EventValue`, `ConditionObservation`, `TimeSeries`, `DataSet`, limits classes | Runtime observation values |
| `configurations.py` | `Configuration`, `CoordinateSystem`, `Specification`, `Motion`, `SolidModel`, limits classes, `ConfigurationRelationship`, `ImageFile`, `PowerSource`, `SensorConfiguration` | Design-time configuration |
| `compositions.py` | `CompositionType`, `Composition` | Component compositions |
| `references.py` | `ComponentRef`, `DataItemRef`, `AssetRef` | By-ID cross-references |
| `__init__.py` | — | Public API re-exports (~50 symbols) |

## Dependencies

The models module depends on:
- `mtconnect.types.primitives` — `ID`, `UUID`, `MTCDateTime`, `Version`, `Second`
- `mtconnect.types.event` / `sample` / `condition` / `subtype` — DataItem type enums
- `mtconnect.types.enums` — Various state/mode/type enums

```
mtconnect.models.configurations ◄── types.primitives, types.enums
mtconnect.models.components ◄── types.primitives, models.configurations, models.data_items (TYPE_CHECKING)
mtconnect.models.data_items ◄── types.primitives, types.{sample,event,condition,subtype}
mtconnect.models.assets ◄── types.primitives
mtconnect.models.values ◄── types.primitives, types.condition, types.subtype
mtconnect.models.compositions ◄── types.primitives
mtconnect.models.references ◄── types.primitives, types.enums
```

**Note**: `components.py` uses `TYPE_CHECKING` guard for `DataItem` to avoid circular imports.

## Design Patterns

### Dataclass + `__post_init__` Validation

Every model class uses `@dataclass` with `__post_init__` for type coercion:

```python
@dataclass
class Component:
    id: ID
    name: str
    uuid: Optional[UUID] = None
    # ...
    
    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = ID(self.id)
        if self.uuid is not None and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)
```

### Category-Dispatched Subclasses

DataItems use fixed `category` fields with type-specific validation:

```python
@dataclass
class SampleDataItem(DataItem):
    def __post_init__(self):
        self.category = DataItemCategory.SAMPLE
        super().__post_init__()
        if self.units is None:
            warnings.warn("SampleDataItem should have units specified")
        if not isinstance(self.type, SampleType):
            raise TypeError(f"Expected SampleType, got {type(self.type)}")
```

### Factory Function

```python
def create_data_item(id, type, category, **kwargs) -> DataItem:
    """Dispatches to correct subclass based on category."""
```

### Design-Time vs Runtime Separation

Configuration limits (design-time, from `/probe`) and value limits (runtime, from `/current`/`/sample`) are deliberately separate class hierarchies:

| Design-Time (configurations.py) | Runtime (values.py) |
|----------------------------------|---------------------|
| `ConfigSpecificationLimits` | `SpecificationLimitsValue` |
| `ConfigControlLimits` | `ControlLimitsValue` |
| `ConfigAlarmLimits` | `AlarmLimitsValue` |

### References vs Relationships

Two distinct concepts, architecturally separated:
- **References** (`references.py`): By-ID pointers — `ComponentRef`, `DataItemRef`, `AssetRef`
- **Relationships** (`configurations.py`): Equipment associations — `ConfigurationRelationship`

## Components (`components.py`)

### Hierarchy

All component types extend the `Component` base dataclass:

```
Component (base)
├── Device              # Top-level equipment unit
├── Controller          # Main control system
├── Axes                # Collection of axis components
│   ├── Linear          # Linear axes (X, Y, Z, U, V, W)
│   └── Rotary          # Rotary axes (A, B, C)
├── Spindle             # Rotating spindle
├── Path                # Execution path
├── Systems             # Supporting systems container
│   ├── Coolant
│   ├── Electric
│   ├── Hydraulic
│   ├── Pneumatic
│   └── Lubrication
└── Auxiliaries         # Auxiliary equipment container
    ├── Door
    └── Chuck
```

### `Component` Base Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `ID` | Unique identifier (validated/coerced from string) |
| `name` | `str` | Human-readable name |
| `uuid` | `Optional[UUID]` | Universally unique identifier |
| `native_name` | `Optional[str]` | Equipment-specific name |
| `sample_interval` | `Optional[float]` | Minimum sampling interval (ms) |
| `sample_rate` | `Optional[float]` | Sampling rate (Hz) |
| `description` | `Optional[Description]` | Manufacturer/model/serial metadata |
| `configuration` | `Optional[Configuration]` | Design-time configuration |
| `data_items` | `List[DataItem]` | Associated data items |
| `components` | `List[Component]` | Child components (recursive tree) |

### `Description` Dataclass

```python
@dataclass
class Description:
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    station: Optional[str] = None
    description: Optional[str] = None
```

### `Device` — Extends Component

Additional fields:
- `iso_841_class: Optional[str]` — ISO 841 equipment classification
- `mtconnect_version: str = "2.6.0"` — MTConnect version

Methods:
- `add_component(component)` — append to children
- `add_data_item(data_item)` — append to data items

## Data Items (`data_items.py`)

### `DataItemCategory` Enum

```python
class DataItemCategory(Enum):
    SAMPLE = auto()     # Continuously variable numeric data
    EVENT = auto()      # Discrete, non-numeric values
    CONDITION = auto()  # Health status
```

### `DataItem` Base Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `ID` | Unique identifier |
| `type` | `Union[SampleType, EventType, ConditionType, str]` | Type from MTConnect enum |
| `category` | `DataItemCategory` | SAMPLE, EVENT, or CONDITION |
| `name` | `Optional[str]` | Human-readable name |
| `sub_type` | `Optional[DataItemSubType]` | Subtype qualifier (ACTUAL, COMMANDED, etc.) |
| `units` | `Optional[str]` | Measurement units |
| `native_units` | `Optional[str]` | Original equipment units |
| `native_scale` | `Optional[float]` | Conversion factor |
| `significant_digits` | `Optional[int]` | Precision specification |
| `coordinate_system` | `Optional[str]` | Reference frame |
| `composition_id` | `Optional[str]` | Associated composition |
| `constraints` | `Optional[Constraints]` | Min/max/nominal/allowed values |
| `discrete` | `bool` | Whether value changes are discrete |

### Category-Specific Subclasses

| Subclass | Fixed Category | Extra Validation |
|----------|---------------|------------------|
| `SampleDataItem` | `SAMPLE` | Warns if `units` missing; validates `type` is `SampleType` |
| `EventDataItem` | `EVENT` | Warns on units for non-count types; validates `type` is `EventType` |
| `ConditionDataItem` | `CONDITION` | Raises if `units` set; validates `type` is `ConditionType` |

### `Constraints` Dataclass

```python
@dataclass
class Constraints:
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    nominal: Optional[float] = None
    values: Optional[List[str]] = None  # Enumerated allowed values
```

## Assets (`assets.py`)

### Asset Type Hierarchy

```
Asset (base)
├── CuttingTool     # Tool assembly with lifecycle tracking
├── Part            # Workpiece with status tracking
├── RawMaterial     # Stock material with lot tracking
├── File            # File references (NC programs, docs)
└── QIFDocumentWrapper  # Quality measurement data
```

### `Asset` Base Fields

| Field | Type | Description |
|-------|------|-------------|
| `asset_id` | `ID` | Unique asset identifier |
| `timestamp` | `MTCDateTime` | Last modification time |
| `device_uuid` | `Optional[UUID]` | Owning device UUID |
| `removed` | `bool` | Whether asset is removed |
| `description` | `Optional[str]` | Free-text description |

### `CuttingTool` — Key Asset Type

Extends `Asset` with:
- `serial_number`, `tool_id`, `manufacturers`
- `cutting_tool_lifecycle: Optional[CuttingToolLifeCycle]`

Methods: `is_expired()`, `remaining_life_percent()`

#### Supporting Classes

| Class | Purpose |
|-------|---------|
| `ToolLifeType(Enum)` | MINUTES, PART_COUNT, WEAR, CYCLES |
| `ToolLifeDirection(Enum)` | UP, DOWN |
| `CutterStatus(Enum)` | 12 states (NEW through UNKNOWN) |
| `ToolLife` | Life tracking with type, value, direction, warning, limit, initial |
| `Location` | Magazine/spindle/crib location with overlap fields |
| `Measurement` | Tool measurements (code, value, units, min/max/nominal) |
| `CuttingToolLifeCycle` | Aggregates life, location, measurements, status |

### Other Asset Types

| Class | Key Fields |
|-------|-----------|
| `Part` | `part_number`, `serial_number`, `lot_id`, `part_status: PartStatus`, `manufacturing_date`, `first_use_date` |
| `RawMaterial` | `material_type: MaterialType`, `container_id`, `lot_id`, `material` |
| `File` | `media_type`, `application_category/type`, `size`, `version_id`, `state: FileState`, `file_location/name` |
| `QIFDocumentWrapper` | `qif_document_type`, `qif_document` |

## Observation Values (`values.py`)

### `ObservationValue` Base Fields

| Field | Type | Description |
|-------|------|-------------|
| `data_item_id` | `ID` | Reference to DataItem definition |
| `timestamp` | `MTCDateTime` | Observation time |
| `sequence` | `int` | Buffer sequence number |
| `name` | `Optional[str]` | DataItem name |
| `sub_type` | `Optional[str]` | Subtype qualifier |
| `composition_id` | `Optional[str]` | Associated composition |

### Category-Specific Values

| Class | Value Type | Key Methods |
|-------|-----------|-------------|
| `SampleValue` | `Union[float, int, UnavailableType]` | `is_unavailable()`, `numeric_value()` |
| `EventValue` | `Union[str, int, bool, UnavailableType]` | `is_unavailable()`, `string_value()` |
| `ConditionObservation` | `level: ConditionLevel` | `is_normal()`, `is_fault()`, `is_warning()`, `is_unavailable()`, `severity_rank()` |

Additional fields on `SampleValue`: `native_value`, `units`, `native_units`, `sample_rate`, `statistic`, `duration`
Additional fields on `ConditionObservation`: `native_code`, `native_severity`, `qualifier: Optional[ConditionQualifier]`, `message`

### Representation Types

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `TimeSeries` | Time-series sample data | `duration_seconds()`, `timestamp_at_index(i)` |
| `DataSet` | Key-value observation data | `get_numeric(key)`, `get_string(key)` |

### Runtime Limits

| Class | Fields | Key Method |
|-------|--------|-----------|
| `SpecificationLimitsValue` | `upper_limit`, `nominal`, `lower_limit` | `is_within_spec(value)` |
| `ControlLimitsValue` | `upper/lower_limit`, `upper/lower_warning`, `nominal` | `is_in_control(value)` |
| `AlarmLimitsValue` | `upper/lower_limit`, `upper/lower_warning` | `check_alarm(value)` → trigger string or None |

## Configurations (`configurations.py`)

### `Configuration` — Top-Level Container

```python
@dataclass
class Configuration:
    coordinate_systems: List[CoordinateSystem]
    specifications: List[Specification]
    sensor_configuration: Optional[SensorConfiguration]
    solid_model: Optional[SolidModel]
    motion: Optional[Motion]
    relationships: List[ConfigurationRelationship]
    image_files: List[ImageFile]
    power_sources: List[PowerSource]
```

### Key Configuration Classes

| Class | Key Fields |
|-------|-----------|
| `CoordinateSystem` | `id: ID`, `type: CoordinateSystemTypeEnum`, `parent_id_ref`, `origin: List[float]` (3-element), `transformation: List[List[float]]` (4×4 matrix) |
| `Specification` | `id`, `type`, `sub_type`, `units`, `originator`, `data_item_id_ref`, nested limits objects |
| `Motion` | `id`, `type` (PRISMATIC/REVOLUTE/CONTINUOUS/FIXED), `actuation` (DIRECT/VIRTUAL/NONE), `coordinate_system_id_ref`, `origin`, `axis` |
| `SolidModel` | `id`, `solid_model_id_ref`, `item_ref`, `href`, `media_type`, `coordinate_system_id_ref` |
| `ConfigurationRelationship` | `id: ID`, `name`, `type: Literal['CHILD', 'PARENT']`, `criticality` |
| `ImageFile` | `id`, `href`, `media_type` |

### Design-Time Limits

| Class | Fields |
|-------|--------|
| `ConfigSpecificationLimits` | `upper_limit`, `nominal`, `lower_limit` |
| `ConfigControlLimits` | `upper_limit`, `upper_warning`, `lower_warning`, `nominal`, `lower_limit` |
| `ConfigAlarmLimits` | `upper_limit`, `upper_warning`, `lower_warning`, `lower_limit` |

## Compositions (`compositions.py`)

- `CompositionType(Enum)` — 52 members (ACTUATOR through WORK_ENVELOPE)
- `Composition` — `id: ID`, `type: CompositionType`, `name`, `uuid`, `manufacturer`, `model`, `serial_number`, `station`

## References (`references.py`)

By-ID pointers for cross-referencing within the device model:

| Class | Fields | Purpose |
|-------|--------|---------|
| `ComponentRef` | `id_ref: ID`, `name` | Points to a Component |
| `DataItemRef` | `id_ref: ID`, `name`, `relationship_type: Optional[DataItemRelationshipTypeEnum]` | Points to a DataItem |
| `AssetRef` | `asset_id: ID`, `asset_type`, `device_uuid: Optional[UUID]` | Points to an Asset |

## Implementation Guidelines

### When Adding a New Component Type

1. Create a new class extending `Component` (usually `pass` body unless extra fields needed)
2. Add to `__init__.py` exports
3. Add test in `tests/models/test_components.py`

### When Adding a New Asset Type

1. Create supporting enum/dataclass types first
2. Create the asset class extending `Asset`
3. Add `__post_init__` validation with type coercion
4. Add to `AssetType` enum if not already present
5. Add to `__init__.py` exports

### When Adding a New Value Type

1. Extend `ObservationValue` base
2. Add `is_unavailable()` method
3. Add category-specific query methods
4. Ensure compatibility with `ComponentStream` in `protocol/streams.py`

### When Modifying Configurations

1. Remember design-time vs runtime separation
2. Configuration classes model `/probe` response structure
3. Value/limits classes model `/current`/`/sample` response values
4. Never mix the two hierarchies

## Existing Tests

- `tests/models/test_components.py` — Device creation, Device with Description, `add_component()`, Linear creation, Spindle creation
