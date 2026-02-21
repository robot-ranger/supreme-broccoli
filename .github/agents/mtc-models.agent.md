---
name: mtc-models
description: "Subagent for generating and maintaining MTConnect data model modules — components, data items, assets, configurations, compositions, references, and observation values in mtconnect/models/."
---

# MTConnect Models Agent

You generate and maintain the `mtconnect/models/` modules — the data model layer that represents MTConnect device hierarchies, data items, assets, configurations, observation values, and references.

## Scope

You own every file in `mtconnect/models/`.

**When you need MTConnect standard interpretation** — component semantics, data item meanings, protocol requirements, model relationships, specification clarifications — **consult mtc-expert**. They specialize in MTConnect standards research.

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
Components (base)
├── Controllers         # Collection of controllers
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
- `UUID` is required for Device, optional for other components

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

## Model Generation System

### **CRITICAL: Never Edit Generated Files Directly**

All model files in `mtconnect/models/` (except `__init__.py`) are **AUTO-GENERATED** from the MTConnect normative XMI model at `.github/agents/data/model_2.6.xml`.

**ALWAYS use the generator scripts. NEVER edit output files manually.**

### Generator Scripts

All generators live in `scripts/`:

| Script | Generates | Classes | Lines |
|--------|-----------|---------|-------|
| `generate_components.py` | `components.py` | 126 | ~1186 |
| `generate_data_items.py` | `data_items.py` | 253 | ~760 |
| `generate_configurations.py` | `configurations.py` | 31 | ~440 |
| `generate_compositions.py` | `compositions.py` | 1 | ~155 |
| `generate_references.py` | `references.py` | 3 | ~89 |
| `run_all_generators.py` | **All above** | **419** | **~3330** |

**Regeneration workflow:**

```bash
# Regenerate all models at once
python scripts/run_all_generators.py

# Or individual modules
python scripts/generate_components.py
python scripts/generate_data_items.py
python scripts/generate_configurations.py
python scripts/generate_compositions.py
python scripts/generate_references.py

# Always validate after regeneration
python -c "from mtconnect.models import Component, DataItem; print('OK')"
python -m pytest tests/models/ -v
```

### XMI Model Structure

The normative model at `.github/agents/data/model_2.6.xml` (162,203 lines) contains:

- **Packages**: Top-level namespaces (`uml:Package`)
  - **Component Types**: `EAPK_6BEE6977_1698_498c_87A6_34B5E656F773` — canonical component definitions
  - **DataTypes**, **Asset Information Model**, **Fundamentals**, **MTConnect Protocol**
- **Classes**: `uml:Class` with `xmi:id`, `name`, `isAbstract`, `isLeaf` attributes
- **Enumerations**: `uml:Enumeration` with `ownedLiteral` members
- **Attributes**: `ownedAttribute` with `type`, `lower`/`upper` cardinality
- **Generalizations**: `generalization` with `general` attribute (parent XMI ID)
- **Documentation**: `ownedComment` with `body` attribute

**Namespace handling:**
```python
XMI_NS = 'http://www.omg.org/spec/XMI/20131001'
UML_NS = 'http://www.omg.org/spec/UML/20131001'

# Use namespace for xmi:type attribute
elem.get("{" + XMI_NS + "}type") == "uml:Class"

# NO namespace for child elements
elem.findall("ownedComment")  # ✓
elem.findall("uml:ownedComment")  # ✗
```

### Duplicate Handling

**CRITICAL**: Many classes appear in multiple packages with different attributes. The "Component Types" package contains the **canonical** definitions.

Example: `Chuck` appears in:
- `Component Types` (isLeaf=None, **but should be leaf**)
- `InformationModel` (isLeaf=None)

**Solution**: Generators prioritize Component Types package classes, skip duplicates from other packages.

```python
# Component Types package ID
COMP_TYPES_PKG_ID = "EAPK_6BEE6977_1698_498c_87A6_34B5E656F773"

# First pass: collect Component Types classes
comp_types_classes = {}
for pkg_elem in root.iter():
    if is_component_types_package(pkg_elem):
        for cls in pkg_elem.findall("packagedElement"):
            name = cls.get("name")
            xmi_id = cls.get("{" + XMI_NS + "}id")
            comp_types_classes[name] = xmi_id

# Second pass: skip duplicates
for elem in root.iter():
    name = elem.get("name")
    xmi_id = elem.get("{" + XMI_NS + "}id")
    if name in comp_types_classes and xmi_id != comp_types_classes[name]:
        continue  # Skip duplicate
```

### Leaf Component Architecture

**MTConnect Standard Requirement**: Leaf components (terminal nodes in the device tree) **MUST NOT** have `components` or `composition` fields.

**Python Constraint**: Dataclasses inherit all parent fields — cannot remove inherited fields.

**Solution**: Two-tier inheritance

```
ComponentBase (base fields only)
├── Component (adds components: List[Component] field)
│   ├── Axes (non-leaf)
│   ├── Controller (non-leaf)
│   ├── Systems (non-leaf)
│   └── ... (112 non-leaf components)
└── Leaf Components (no components field)
    ├── Motor (isLeaf="true")
    ├── Encoder (isLeaf="true")
    ├── Amplifier (isLeaf="true")
    ├── Table (isLeaf="true")
    ├── Workpiece (isLeaf="true")
    ├── Drain (isLeaf="true")
    ├── Pump (isLeaf="true")
    └── Chuck (manual override, isLeaf not set in v2.6 XMI)
```

**Generator logic:**

```python
def _resolve_parent(info, class_info):
    """Determine whether class inherits ComponentBase or Component."""
    is_leaf = info.get("is_leaf", False)
    
    # Manual override for Chuck (isLeaf not set in v2.6 XMI)
    if info["name"] == "Chuck":
        is_leaf = True
    
    # Leaf → ComponentBase (no components field)
    if is_leaf:
        return "ComponentBase"
    
    # Non-leaf → Component (has components field)
    # Or resolves to specific parent from hierarchy
    for p_id in info["parent_ids"]:
        if p_id == COMPONENT_XMI_ID:
            return "Component"
        p_info = class_info.get(p_id)
        if p_info and _is_component_descendant(p_id, class_info):
            return p_info["name"]
    
    return "Component"  # Default for non-leaf
```

**Verification:**

```python
from mtconnect.models.components import Workpiece, ComponentBase, Component

assert Workpiece.__bases__ == (ComponentBase,)
assert not hasattr(Workpiece, 'components')
```

### Cardinality [0..0] Semantics

When XMI shows `lower="0" upper="0"` for an attribute, it means:
- **Redefined to empty** in this class (typically in leaf components)
- **Do not generate the field** — parent provides it but child overrides to exclude it
- Used for `components` and `composition` in leaf classes

**Generator handling:**

```python
lower, upper = get_cardinality(attr)
if lower == 0 and upper == '0':
    continue  # Skip [0..0] attributes
```

### Manual Overrides

Some XMI attributes are incorrect or missing. Document overrides in generator code:

```python
# Manual override: Chuck is a leaf component per MTConnect standard
# (isLeaf attribute not set in v2.6 XMI but semantically it's a leaf)
if name == "Chuck":
    is_leaf = True
```

### Test Suite

**ALWAYS run tests after regeneration.**

```bash
# All model tests
python -m pytest tests/models/ -v -o addopts=""

# Specific test files
python -m pytest tests/models/test_generation.py -v -o addopts=""
python -m pytest tests/models/test_components.py -v -o addopts=""

# Leaf component architecture validation
python -m pytest tests/models/test_generation.py::TestCardinalityExclusion -v -o addopts=""
```

Key test suites:

| Test Class | Purpose | Tests |
|------------|---------|-------|
| `TestRequiredFieldValidation` | Required field enforcement | 4 |
| `TestCardinalityExclusion` | Leaf components lack `components` field | 6 |
| `TestOptionalVsRequiredFields` | Field optionality correct | 3 |
| `TestTypeCheckingImports` | No circular imports | 3 |
| `TestDataclassFieldOrdering` | Required before optional fields | 3 |
| `TestGeneratedClassCounts` | Expected class counts | 3 |

**Expected test output:**

```
tests/models/test_generation.py ................ 22 passed
tests/models/test_components.py ................ 26 passed
```

### Workflow Summary

**Making changes:**

1. ✅ **Edit generator script** in `scripts/generate_*.py`
2. ✅ **Run generator** to regenerate model file
3. ✅ **Validate imports** with quick Python check
4. ✅ **Run test suite** to verify correctness
5. ❌ **NEVER edit** generated files directly

**Adding new model classes:**

1. Check if already in XMI model (most MTConnect v2.6 types are)
2. If in XMI: update generator logic to extract it
3. If not in XMI: create static template in generator
4. Regenerate file
5. Add to `__init__.py` exports
6. Write tests

**Debugging generation issues:**

1. Create diagnostic script to examine XMI (see `check_leaf.py` example)
2. Check package membership (Component Types vs others)
3. Verify `xmi:id`, `isLeaf`, `isAbstract` attributes
4. Check parent class via `generalization` element
5. Add debug prints to generator, run, review output
6. Validate with tests

## Implementation Guidelines

### When Adding a New Component Type

1. **Consult mtc-expert** if unclear about component semantics or relationships
2. **Check XMI model first** — most v2.6 components already defined
3. If in XMI: Update `generate_components.py` to extract it
4. If not in XMI: Add as static template to generator
5. **Regenerate** with `python scripts/generate_components.py`
6. Add to `__init__.py` exports
7. **Write test** in `tests/models/test_components.py`
8. **Run test suite** to validate

### When Adding a New Asset Type

1. **Check XMI model first** — Asset types defined in "Asset Information Model" package
2. If in XMI: Create/update generator for asset types (currently manual but follow generator pattern)
3. Create supporting enum/dataclass types first
4. Create the asset class extending `Asset`
5. Add `__post_init__` validation with type coercion
6. Add to `AssetType` enum if not already present
7. Add to `__init__.py` exports
8. **Write tests**
9. **Run test suite** to validate

### When Adding a New Value Type

1. **Check protocol structure** in MTConnect streams response
2. Extend `ObservationValue` base
3. Add `is_unavailable()` method
4. Add category-specific query methods
5. Ensure compatibility with `ComponentStream` in `protocol/streams.py`
6. Add to `__init__.py` exports
7. **Write tests**

### When Modifying Configurations

1. **Never edit** `configurations.py` directly — use `generate_configurations.py`
2. Remember design-time vs runtime separation
3. Configuration classes model `/probe` response structure
4. Value/limits classes model `/current`/`/sample` response values
5. Never mix the two hierarchies
6. **Regenerate** with generator script
7. **Run test suite** to validate

### When Modifying Data Items

1. **Never edit** `data_items.py` directly — use `generate_data_items.py`
2. Check if change affects type enums in `mtconnect/types/`
3. Update generator logic as needed
4. **Regenerate** with `python scripts/generate_data_items.py`
5. **Run test suite** to validate

## Anti-Patterns to Avoid

❌ **Don't** edit generated model files directly  
✅ **Do** edit the generator script, then regenerate

❌ **Don't** skip running tests after regeneration  
✅ **Do** run `pytest tests/models/ -v` every time

❌ **Don't** assume XMI classes are unique by name  
✅ **Do** prioritize Component Types package, handle duplicates

❌ **Don't** make leaf components inherit from `Component`  
✅ **Do** use `ComponentBase` for leaf components (no `components` field)

❌ **Don't** add `components` field to leaf component classes  
✅ **Do** set `isLeaf="true"` in XMI or add manual override in generator

❌ **Don't** mix design-time configuration limits with runtime value limits  
✅ **Do** keep separate hierarchies: `ConfigSpecificationLimits` vs `SpecificationLimitsValue`

❌ **Don't** use circular imports between models modules  
✅ **Do** use `TYPE_CHECKING` guard for forward references

❌ **Don't** forget to export new classes in `__init__.py`  
✅ **Do** add all public API symbols to `__init__.py` exports

## Test Suite Reference

### Test Files

| Test File | Coverage | Tests |
|-----------|----------|-------|
| `tests/models/test_generation.py` | Generator output validation | 22 |
| `tests/models/test_components.py` | Component instantiation, hierarchy | 26 |
| `tests/protocol/test_header.py` | Protocol headers | 6 |
| `tests/types/test_primitives.py` | Primitive types | 6 |
| `tests/types/test_sample.py` | Sample type enums | 3 |

### Critical Test Classes

**tests/models/test_generation.py:**

- `TestRequiredFieldValidation` — Validates required fields enforced (4 tests)
  - `test_door_requires_door_state` — Door needs door_state relationship
  - `test_interface_requires_interface_state` — Interface needs interface_state
  - `test_part_occurrence_requires_part_id` — PartOccurrence needs part_id
  - `test_door_succeeds_with_required_field` — Valid door creation works

- `TestCardinalityExclusion` — Validates leaf components lack `components` field (6 tests)
  - `test_workpiece_no_compositions` — Workpiece is leaf
  - `test_amplifier_no_compositions` — Amplifier is leaf
  - `test_fan_no_compositions` — Fan is leaf
  - `test_ballscrew_no_compositions` — BallScrew is leaf
  - `test_encoder_no_compositions` — Encoder is leaf
  - `test_drain_no_compositions` — Drain is leaf

- `TestOptionalVsRequiredFields` — Field optionality correct (3 tests)

- `TestTypeCheckingImports` — No circular imports (3 tests)

- `TestDataclassFieldOrdering` — Required fields before optional (3 tests)

- `TestGeneratedClassCounts` — Expected class counts (3 tests)
  - `test_components_generated` — Expects 126 component classes
  - `test_data_items_generated` — Expects 253 data item classes
  - `test_configurations_generated` — Expects 31 configuration classes

**tests/models/test_components.py:**

- Basic instantiation tests for all major component types
- Hierarchy tests (Linear extends Axis, Controller extends System, etc.)
- Leaf component validation (Motor, Encoder, Valve lack `components` field)
- Organizer tests (Axes, Resources, Controllers, Materials)
- Device operations (add_component, add_data_item)

### Running Tests

```bash
# All model tests
python -m pytest tests/models/ -v -o addopts=""

# Specific test class
python -m pytest tests/models/test_generation.py::TestCardinalityExclusion -v -o addopts=""

# Specific test
python -m pytest tests/models/test_components.py::test_motor_leaf -v -o addopts=""

# With coverage
python -m pytest tests/models/ --cov=mtconnect.models --cov-report=term-missing

# Quick validation (no pytest config)
python -m pytest tests/models/ -v -o addopts=""
```

**Note**: Use `-o addopts=""` to override project config that requires `pytest-cov` (which may not be installed).

## Existing Tests

**tests/models/test_components.py** (26 tests):
- Device creation, Device with Description
- `add_component()`, `add_data_item()` methods
- All major component types: Linear, Rotary, Spindle, Controller, Hydraulic, Pneumatic, Stock, Link
- Organizer components: Axes, Resources, Controllers, Materials
- Leaf components: Motor, Encoder, Valve (must inherit ComponentBase, not Component)
- Abstract base validation: Axis, System, Auxiliary, Resource cannot be instantiated directly
- Inheritance hierarchy: Linear extends Axis, Controller extends System, etc.
- Special occurrence types: FeatureOccurrence, ProcessOccurrence, PartOccurrence

**tests/models/test_generation.py** (22 tests):
- Required field validation (Door requires door_state, Interface requires interface_state, etc.)
- Cardinality exclusion (Workpiece, Amplifier, Fan, BallScrew, Encoder, Drain have no `components` field)
- Optional vs required field handling
- TYPE_CHECKING imports work without circular dependency
- Dataclass field ordering (required before optional)
- Expected class counts (126 components, 253 data items, 31 configurations)
