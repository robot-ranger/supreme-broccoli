# MTConnect Python Package

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MTConnect Version](https://img.shields.io/badge/MTConnect-v2.6-green.svg)](https://model.mtconnect.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Foundation library providing MTConnect v2.6 types, enums, and models for Python.**

This package offers standardized Python representations of MTConnect protocol elements, enabling developers to build adapters, clients, agents, and validation tools with proper type safety and MTConnect standard compliance.

## Features

- ✅ **Complete Type Enumerations**: All 105 enums from MTConnect v2.6 model (SAMPLE, EVENT, CONDITION types, units, states, representations, etc.)
- ✅ **Primitive Datatypes**: Type-safe wrappers for MTConnect primitives (ID, UUID, Int32, DateTime, Version, etc.)
- ✅ **Component Models**: Device hierarchy classes (Device, Controller, Axes, Linear, Rotary, Spindle, etc.)
- ✅ **DataItem Models**: Sample, Event, and Condition data item definitions with validation
- ✅ **Asset Models**: CuttingTool, Part, RawMaterial, File, QIFDocumentWrapper with lifecycle tracking
- ✅ **Observation Values**: Type-safe observation classes with timestamps and sequence tracking
- ✅ **Protocol Structures**: MTConnectDevices, MTConnectStreams, MTConnectAssets response documents
- ✅ **Error Handling**: Standard error codes and exception classes

## Installation

```bash
# Clone the repository (until published to PyPI)
git clone https://github.com/username/mtconnect.git
cd mtconnect

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Using Type Enumerations

```python
from mtconnect.types import SampleType, EventType, ConditionType, DataItemSubType

# DataItem types by category
position_type = SampleType.POSITION
execution_state = EventType.EXECUTION
system_condition = ConditionType.SYSTEM

# DataItem subtypes
actual = DataItemSubType.ACTUAL
commanded = DataItemSubType.COMMANDED
```

### Creating Components

```python
from mtconnect.models import Device, Controller, Linear, Description
from mtconnect.types.primitives import ID, UUID

# Create a device
device = Device(
    id=ID("mill"),
    name="Mill-01",
    uuid=UUID("M8010W4194N"),
    description=Description(
        manufacturer="ACME Corp",
        model="CNC-5000",
        serial_number="SN12345"
    )
)

# Add components
controller = Controller(id=ID("cnc-controller"), name="Controller")
x_axis = Linear(id=ID("x"), name="X", native_name="X-Axis")

device.add_component(controller)
device.add_component(x_axis)
```

### Defining DataItems

```python
from mtconnect.models import SampleDataItem, EventDataItem, DataItemCategory
from mtconnect.types import SampleType, EventType, DataItemSubType

# Create a SAMPLE DataItem for position
position_item = SampleDataItem(
    id=ID("x_pos"),
    type=SampleType.POSITION,
    sub_type=DataItemSubType.ACTUAL,
    units="MILLIMETER",
    name="X Actual Position"
)

# Create an EVENT DataItem for execution state
exec_item = EventDataItem(
    id=ID("exec"),
    type=EventType.EXECUTION,
    name="Controller Execution"
)
```

### Working with Observations

```python
from mtconnect.models import SampleValue, EventValue
from mtconnect.types.primitives import ID, MTCDateTime

# Create a sample observation
position_obs = SampleValue(
    data_item_id=ID("x_pos"),
    timestamp=MTCDateTime("2026-02-19T10:30:45.123Z"),
    sequence=12345,
    value=150.5,
    units="MILLIMETER"
)

# Create an event observation
exec_obs = EventValue(
    data_item_id=ID("exec"),
    timestamp=MTCDateTime("2026-02-19T10:30:45.123Z"),
    sequence=12346,
    value="ACTIVE"
)
```

### Creating Assets

```python
from mtconnect.models import CuttingTool, CuttingToolLifeCycle, ToolLife
from mtconnect.models import ToolLifeType, ToolLifeDirection
from mtconnect.types.primitives import ID, MTCDateTime

# Create a cutting tool asset
tool = CuttingTool(
    asset_id=ID("T12"),
    timestamp=MTCDateTime("2026-02-19T10:00:00Z"),
    serial_number="ST-12345",
    cutting_tool_lifecycle=CuttingToolLifeCycle(
        tool_life=ToolLife(
            type=ToolLifeType.MINUTES,
            value=45.5,
            count_direction=ToolLifeDirection.UP,
            limit=120.0
        ),
        program_tool_number="12"
    )
)

# Check tool life
if tool.is_expired():
    print("Tool has exceeded its life limit")
remaining = tool.remaining_life_percent()
print(f"Remaining tool life: {remaining:.1f}%")
```

### Working with Protocol Responses

```python
from mtconnect.protocol import Header, MTConnectStreams, DeviceStream
from mtconnect.types.primitives import MTCDateTime, Version, UUID

# Create a header
header = Header(
    creation_time=MTCDateTime("2026-02-19T10:30:00Z"),
    sender="agent-hostname",
    instance_id=1234567890,
    version=Version("2.6.0"),
    buffer_size=10000,
    first_sequence=1000,
    last_sequence=5000,
    next_sequence=5001
)

# Check buffer status
if header.is_buffer_nearly_full():
    print(f"Buffer utilization: {header.buffer_utilization_percent():.1f}%")

# Check sequence availability
if not header.sequence_is_available(500):
    print("Requested sequence out of range")
```

## Package Structure

```
mtconnect/
├── __init__.py           # Main package exports
├── types/                # Type enumerations and primitives
│   ├── primitives.py     # MTConnect primitive datatypes
│   ├── sample.py         # SAMPLE category types
│   ├── event.py          # EVENT category types
│   ├── condition.py      # CONDITION category types
│   ├── subtype.py        # DataItem subtypes
│   └── enums.py          # Additional enums (units, states, etc.)
├── models/               # MTConnect structural elements
│   ├── components.py     # Device, Controller, Axes, etc.
│   ├── data_items.py     # DataItem definitions
│   ├── assets.py         # CuttingTool, Part, etc.
│   ├── values.py         # Observation value classes
│   └── relationships.py  # References and compositions
└── protocol/             # REST API structures
    ├── header.py         # Response header
    ├── responses.py      # Response documents
    ├── streams.py        # Stream organization
    └── errors.py         # Error handling
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=mtconnect --cov-report=html
```

### Type Checking

```bash
# Run mypy
mypy mtconnect/
```

### Linting

```bash
# Run ruff
ruff check mtconnect/

# Auto-fix issues
ruff check --fix mtconnect/
```

## Extracting Enums from Model

The package includes a script to extract enumerations from the MTConnect normative model:

```bash
# Extract all enums
python scripts/extract_enums.py

# Extract specific enums
python scripts/extract_enums.py --enum-names UnitEnum StatisticEnum

# Specify output location
python scripts/extract_enums.py --output-dir custom/path --output-file my_enums.py
```

## Use Cases

This library is designed as a foundation for:

- **MTConnect Adapters**: Use types and models to validate and format adapter data
- **MTConnect Clients**: Parse responses with proper type safety and validation
- **MTConnect Agents**: Build agent implementations with standard-compliant data structures
- **Testing Tools**: Validate MTConnect documents and data against standard requirements
- **Data Analysis**: Work with MTConnect data using well-defined Python objects

## Reference

- **MTConnect Standard**: https://www.mtconnect.org/
- **MTConnect Model v2.6**: https://model.mtconnect.org/
- **Normative Model**: Included in `.github/agents/data/model_2.6.xml`

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `pytest`
2. Code is type-checked: `mypy mtconnect/`
3. Code is linted: `ruff check mtconnect/`
4. New features include tests and documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built from the MTConnect v2.6 normative model maintained by the MTConnect Institute.
