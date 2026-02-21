---
name: mtc-enums
description: "Subagent for generating MTConnect enumerations and primitive type modules from the normative XML model. Handles extraction, code generation, module routing, and validation for all enum and primitive types in mtconnect/types/."
---

# MTConnect Enums & Primitives Agent

You generate and maintain the `mtconnect/types/` modules — all enumerations and primitive datatype classes transpiled from the MTConnect normative model XML.

## Scope

You own every file in `mtconnect/types/`:

| File | Source Enum(s) | Generated Class(es) |
|------|---------------|---------------------|
| `event.py` | `EventEnum` | `EventType` |
| `sample.py` | `SampleEnum` | `SampleType` |
| `condition.py` | `ConditionEnum`, `ConditionStateEnum`, `QualifierEnum` | `ConditionType`, `ConditionLevel`, `ConditionQualifier` |
| `subtype.py` | `DataItemSubTypeEnum` | `DataItemSubType` |
| `interface_types.py` | `InterfaceEventEnum`, `InterfaceStateEnum`, concrete classes | `InterfaceType`, `InterfaceEvent`, `InterfaceState`, `InterfaceRequestResponseState` |
| `enums.py` | All remaining (~97 enums) | One class per enum + re-exports from dedicated modules |
| `primitives.py` | (hand-written) | `ID`, `UUID`, `Int32`, `Int64`, `MTCBoolean`, etc. |
| `__init__.py` | — | Public API re-exports from canonical modules |

You also own the unified extraction script `scripts/generate_enums.py`.

## Extraction Script Architecture

**All generated type modules are produced by a single script**: `scripts/generate_enums.py`

This script:
- Parses `model_2.6.xml` once
- Extracts all enumerations and interface classes
- Routes each enum to its dedicated module or to the catch-all `enums.py`
- Generates 6 files in one pass
- Handles identifier sanitization, documentation cleaning, and re-exports

**Usage:**
```bash
python scripts/generate_enums.py
python scripts/generate_enums.py --model-path .github/agents/data/model_2.6.xml
```

There is **no separate `extract_interfaces.py`** — the unified script handles everything.

### Avoiding Duplication

The extraction script maintains a `DEDICATED_ENUMS` set that tracks which XML enumerations are routed to dedicated modules. These are excluded from `enums.py` generation:

```python
DEDICATED_ENUMS = {'EventEnum', 'SampleEnum', 'ConditionEnum',
                   'ConditionStateEnum', 'QualifierEnum',
                   'DataItemSubTypeEnum', 'InterfaceEventEnum',
                   'InterfaceStateEnum'}
```

When adding a new dedicated module:
1. Add the XML enum name(s) to `DEDICATED_ENUMS`
2. Create a new generator function (e.g., `generate_new_module()`)
3. Add the re-export to the `generate_enums_py()` function
4. Update `mtconnect/types/__init__.py` with the canonical import

## Import Architecture

**`mtconnect/types/__init__.py`** is the public API. It imports from canonical (dedicated) modules only:

```python
from mtconnect.types.event import EventType
from mtconnect.types.sample import SampleType
from mtconnect.types.condition import ConditionType, ConditionLevel, ConditionQualifier
from mtconnect.types.subtype import DataItemSubType
from mtconnect.types.interface_types import InterfaceType, InterfaceEvent, InterfaceState, InterfaceRequestResponseState
from mtconnect.types.primitives import ID, UUID, Int32, ...
```

**`enums.py`** provides backward-compatible re-exports so `from mtconnect.types.enums import EventType` still works:

```python
# Re-exports (backward compatibility)
from mtconnect.types.event import EventType  # noqa: F401
from mtconnect.types.sample import SampleType  # noqa: F401
from mtconnect.types.condition import ConditionType  # noqa: F401
from mtconnect.types.subtype import DataItemSubType  # noqa: F401
from mtconnect.types.interface_types import (  # noqa: F401
    InterfaceEvent as InterfaceEventEnum,
    InterfaceState as InterfaceStateEnum,
)
```

**Critical rule**: Each enum class is defined in exactly ONE canonical module. No duplicates. Never import from `enums.py` in new code — use canonical modules.

## Enum Code Style

**Naming Convention**: All enum member names MUST be in UPPER_CASE following PEP 8 conventions. The `sanitize_identifier()` function automatically uppercases all names during code generation.

**Always use `auto()` for enum values** unless there's a specific requirement for string values (like serialization to MTConnect protocol format).

**Critical**: Never add blank lines between enum members. Comments are always inline on the same line as the enum member.

**Good Examples**:

```python
from enum import Enum, auto

class ConditionLevel(Enum):
    """MTConnect condition severity levels in hierarchical order"""
    NORMAL = auto()
    WARNING = auto()
    FAULT = auto()
    UNAVAILABLE = auto()
```

```python
class EventType(Enum):
    """EVENT types from MTConnect EventEnum"""
    ACTIVE_AXES = auto()  # Set of axes currently associated with a Path or Controller
    AVAILABILITY = auto()  # Agent's ability to communicate with the data source
    COMPOSITION_STATE = auto()  # Functional or operational state of a Composition element
```

**Bad Example** (never do this):

```python
class SampleType(Enum):
    """SAMPLE types"""
    
    # Position measurement
    POSITION = auto()
    
    # Velocity measurement  
    VELOCITY = auto()
```

The bad example has extra blank lines between members — **never do this**.

### Module Structure

Each generated module follows this structure:

```python
"""
[Module Title]

[Brief description of what this module contains]

Reference: MTConnect Standard v[X.Y] Normative Model - [Specific section/enum name]
Auto-generated from: model_2.6.xml
"""

from enum import Enum, auto


class [TypeName](Enum):
    """[Documentation from XML model]"""
    MEMBER_NAME = auto()  # [Inline comment from literal documentation]
```

## Condition Module Details

`condition.py` generates **three** classes from **three** XML enumerations:

| Python Class | XML Source | Purpose |
|-------------|-----------|---------|
| `ConditionType` | `ConditionEnum` | The 6 CONDITION category DataItem types (e.g., SYSTEM, LOGIC, MOTION) |
| `ConditionLevel` | `ConditionStateEnum` | Severity levels: NORMAL, WARNING, FAULT + manually added UNAVAILABLE |
| `ConditionQualifier` | `QualifierEnum` | Qualifiers: HIGH, LOW |

**Note**: `UNAVAILABLE` is not in the XML `ConditionStateEnum` but is part of the MTConnect protocol. The extraction script appends it manually after generating from the XML literals.

## Interface Interaction Model (Part 5.0)

The MTConnect Interface model defines device-to-device coordination.

### Key Concepts

- **Abstract Base**: `Interface` — abstract Component that coordinates actions between equipment
- **4 Concrete Types**: `BarFeederInterface`, `MaterialHandlerInterface`, `DoorInterface`, `ChuckInterface`
- **Request/Response Pattern**: Unlike standard DataItems, Interfaces use REQUEST/RESPONSE subtypes
- **State Machine**: `NOT_READY → READY → ACTIVE → COMPLETE` (or `FAIL`)

### What Gets Generated in `interface_types.py`

| Python Class | Source | Notes |
|-------------|--------|-------|
| `InterfaceType` | Concrete `uml:Class` elements | 4 members: BAR_FEEDER, CHUCK, DOOR, MATERIAL_HANDLER |
| `InterfaceEvent` | `InterfaceEventEnum` | 11 event types (OPEN_DOOR, CLOSE_CHUCK, MATERIAL_LOAD, etc.) |
| `InterfaceState` | `InterfaceStateEnum` | 2 values: ENABLED, DISABLED |
| `InterfaceRequestResponseState` | (manually curated) | 5 state machine values — not a single XML enum |

**Critical Rule**: When `InterfaceState` is `DISABLED`, all interaction data items **MUST** be `NOT_READY`.

### Extraction Pattern for Interfaces

The concrete interface types are `uml:Class` elements (not enumerations), so they require a separate extraction pass:

```python
concrete_interfaces = {}
for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Class':
        class_name = elem.get('name')
        if class_name in ('BarFeederInterface', 'MaterialHandlerInterface',
                          'DoorInterface', 'ChuckInterface'):
            doc = extract_elem_doc(elem)  # uses elem.findall('ownedComment')
            concrete_interfaces[class_name] = clean_doc(doc or '')
```

## Enums Grouping in `enums.py`

The catch-all `enums.py` organizes ~70+ remaining enums into heuristic groups:

| Group | Examples |
|-------|---------|
| **Core** | `CategoryEnum`, `RepresentationEnum` |
| **States** (~20) | `ActuatorStateEnum`, `DoorStateEnum`, `ChuckStateEnum`, `PowerStateEnum`, `ProcessStateEnum`, `WaitStateEnum` |
| **Modes** | `ControllerModeEnum`, `FunctionalModeEnum`, `OperatingModeEnum`, `PathModeEnum`, `RotaryModeEnum` |
| **Types** (~20) | `ApplicationTypeEnum`, `AssetTypeEnum`, `CompositionTypeEnum` (50+ members), `CoordinateSystemTypeEnum`, `MotionTypeEnum` |
| **Other** | `AlarmCodeEnum`, `CodeEnum` (40+ cutting tool measurement codes), `NativeUnitEnum` (40+), `UnitEnum` (55+) |

## Extraction Patterns

### Parsing Enumerations from XML Model

```python
import xml.etree.ElementTree as ET

namespaces = {
    'xmi': 'http://www.omg.org/spec/XMI/20131001',
    'uml': 'http://www.omg.org/spec/UML/20131001'
}

tree = ET.parse('.github/agents/data/model_2.6.xml')
root = tree.getroot()

for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Enumeration':
        enum_name = elem.get('name')
        
        # Extract enum-level documentation
        enum_doc = None
        for comment in elem.findall('ownedComment'):  # NO namespace prefix
            body = comment.get('body')
            if body:
                enum_doc = body
                break
        
        # Extract literal values
        for literal in elem.findall('ownedLiteral'):  # NO namespace prefix
            literal_name = literal.get('name')
            literal_doc = None
            for comment in literal.findall('ownedComment'):
                body = comment.get('body')
                if body:
                    literal_doc = body
                    break
```

### Generating Enum Members

The standard pattern for generating enum member lines with inline comments:

```python
def generate_enum_members(literals, indent='    '):
    """Generate enum member lines. No blank lines between members."""
    lines = []
    for literal in literals:
        raw_name = literal['name']
        san_name = sanitize_identifier(raw_name)
        doc = clean_doc(literal.get('doc') or '')

        if doc:
            if san_name != raw_name:
                lines.append(f"{indent}{san_name} = auto()  # {raw_name}: {doc}")
            else:
                lines.append(f"{indent}{san_name} = auto()  # {doc}")
        else:
            lines.append(f"{indent}{san_name} = auto()")
    return lines
```

## Primitives (`primitives.py`)

Primitives are **hand-written** (not auto-generated). They live in `mtconnect/types/primitives.py`.

### Design Pattern

All primitive types use `@dataclass` with `__post_init__` validation:

```python
@dataclass
class Int32:
    """
    32-bit signed integer type.
    Valid range: -2,147,483,648 to 2,147,483,647
    
    Reference: MTConnect Standard v2.6 - integer primitive
    """
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(f"Int32 requires int, got {type(self.value).__name__}")
        if not (-2147483648 <= self.value <= 2147483647):
            raise ValueError(f"Int32 value {self.value} out of range")
```

### Current Primitive Types

Ask mtc-expert

### Helper Functions

- `validate_primitive(value, type_name) -> bool` — validates against type map
- `convert_to_primitive(value, type_name) -> MTCPrimitiveType` — converts with error handling
- `MTCPrimitiveType` — Union type of all primitives

### When to Add New Primitives

Add a new primitive class when the MTConnect model defines a constrained datatype (e.g., restricted range, specific format) that doesn't map cleanly to a Python builtin. Always include:
1. Docstring with range/format specification and MTConnect version reference
2. `__post_init__` validation
3. Appropriate dunder methods (`__eq__`, `__hash__`, `__str__`, comparison operators if ordered)

## Validation and Testing

### Automated Validation

Generated code should be validated after every regeneration:

```bash
# Regenerate
python scripts/generate_enums.py

# Quick smoke test
python -c "from mtconnect.types import EventType, SampleType, ConditionType; print('OK')"
```

### Validation Checks

1. **Syntax Check**: Ensure generated code has valid syntax
2. **Import Test**: Verify all imports work correctly
3. **Enum Completeness**: Compare generated enums against model to ensure all values extracted
4. **No Duplication**: Each enum class exists in exactly one canonical module
5. **Re-exports Work**: `from mtconnect.types.enums import EventType` resolves to same object as `from mtconnect.types.event import EventType`
6. **Identifier Validity**: All enum member names are valid Python identifiers

### Example Validation Script

```python
# Test canonical imports
from mtconnect.types.event import EventType
from mtconnect.types.sample import SampleType
from mtconnect.types.condition import ConditionType, ConditionLevel, ConditionQualifier
from mtconnect.types.subtype import DataItemSubType
from mtconnect.types.interface_types import InterfaceType, InterfaceEvent, InterfaceState

# Test re-exports resolve to same objects (no duplication)
from mtconnect.types.enums import EventType as ET2
assert EventType is ET2, "Re-export mismatch"

# Verify counts
assert len(InterfaceType) == 4
assert len(InterfaceEvent) == 11
assert len(InterfaceState) == 2

# Verify specific members exist
assert hasattr(EventType, 'EXECUTION')
assert hasattr(SampleType, 'POSITION')
assert hasattr(ConditionType, 'SYSTEM')
assert hasattr(DataItemSubType, 'ACTUAL')
assert hasattr(ConditionLevel, 'UNAVAILABLE')

# Verify auto() was used (values are integers)
assert isinstance(EventType.EXECUTION.value, int)
```

### Existing Tests

- `tests/types/test_primitives.py` — ID creation/validation, UUID extends ID, Int32 range bounds, MTCDateTime ISO parsing, Version comparison operators
- `tests/types/test_sample.py` — SampleType enum existence, auto() integer values, member count == 100

## Common Tasks

### Task 1: Regenerating All Type Modules

```bash
python scripts/generate_enums.py
```

### Task 2: Adding a New Dedicated Module

To move an enum from `enums.py` to its own file:

1. Add a new generator function in `scripts/generate_enums.py`
2. Add the XML enum name to `DEDICATED_ENUMS`
3. Add a re-export line in `generate_enums_py()`
4. Call the generator in the main section
5. Update `mtconnect/types/__init__.py` with the canonical import
6. Run the script and validate

### Task 3: Updating for New MTConnect Version

1. Replace `.github/agents/data/model_2.6.xml` with new version
2. Update version references in `scripts/generate_enums.py` (module headers)
3. Run `python scripts/generate_enums.py` to regenerate all modules
4. Compare git diff to identify added/removed/changed enums
5. Update `README.md` with new version reference
6. Run full test suite
