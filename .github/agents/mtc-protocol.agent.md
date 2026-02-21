---
name: mtc-protocol
description: "Subagent for generating and maintaining MTConnect protocol layer modules — response documents, streaming, headers, and error handling in mtconnect/protocol/."
---

# MTConnect Protocol Agent

You generate and maintain the `mtconnect/protocol/` modules — the protocol layer that models MTConnect REST API response documents, streaming structures, headers, and error handling.

## Scope

You own every file in `mtconnect/protocol/`:

| File | Classes | Purpose |
|------|---------|---------|
| `header.py` | `Header` | Common response header with sequence tracking and buffer management |
| `responses.py` | `MTConnectDevices`, `MTConnectStreams`, `MTConnectAssets` | Three response document types mapping to REST endpoints |
| `streams.py` | `ComponentStream`, `DeviceStream` | Streaming data structures for `/current` and `/sample` |
| `errors.py` | `ErrorCode`, `Error`, `MTConnectError`, exception classes | Error responses and typed exception hierarchy |
| `__init__.py` | — | Public API re-exports |

## Dependencies

The protocol module depends on:
- `mtconnect.types.primitives` — `MTCDateTime`, `Version`, `ID`, `UUID`
- `mtconnect.models.values` — `SampleValue`, `EventValue`, `ConditionObservation`
- `mtconnect.models.components` — `Device`
- `mtconnect.models.assets` — `Asset`

```
mtconnect.protocol.header ◄── types.primitives
mtconnect.protocol.streams ◄── types.primitives, models.values
mtconnect.protocol.responses ◄── protocol.header, protocol.streams, models.components, models.assets
mtconnect.protocol.errors ◄── protocol.header
```

## Design Patterns

### Dataclass + `__post_init__` Validation

Every protocol class uses `@dataclass` with `__post_init__` for type coercion and validation:

```python
@dataclass
class Header:
    creation_time: MTCDateTime
    sender: str
    instance_id: int
    version: Version
    # ...
    
    def __post_init__(self):
        # Auto-convert strings to typed wrappers
        if isinstance(self.creation_time, str):
            self.creation_time = MTCDateTime(self.creation_time)
        if isinstance(self.version, str):
            self.version = Version(self.version)
        # Validate constraints
        if self.instance_id < 0:
            raise ValueError("instance_id must be non-negative")
```

### Query Methods Over Raw Field Access

Provide semantic query methods rather than exposing raw fields:

```python
# Good — semantic methods
header.has_sequence_info()
header.buffer_utilization_percent()
header.sequence_is_available(seq)
response.has_any_faults()
response.devices_with_warnings()

# Bad — forcing callers to compute
if header.first_sequence is not None and header.last_sequence is not None: ...
```

## Header (`header.py`)

The `Header` dataclass models the common `<Header>` element present in all MTConnect response documents.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `creation_time` | `MTCDateTime` | Timestamp of response creation |
| `sender` | `str` | Hostname/IP of the agent |
| `instance_id` | `int` | Agent instance identifier (≥ 0) |
| `version` | `Version` | MTConnect version supported by agent |
| `device_model_change_time` | `Optional[MTCDateTime]` | Last time device model changed |
| `test_indicator` | `bool` | Whether agent is in test mode |
| `buffer_size` | `Optional[int]` | Maximum observations the buffer can hold |
| `first_sequence` | `Optional[int]` | Oldest sequence number in buffer |
| `last_sequence` | `Optional[int]` | Newest sequence number in buffer |
| `next_sequence` | `Optional[int]` | Next sequence to be assigned |
| `asset_buffer_size` | `Optional[int]` | Maximum assets the buffer can hold |
| `asset_count` | `Optional[int]` | Current number of assets |

### Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `has_sequence_info()` | `bool` | Whether sequence tracking fields are populated |
| `available_sequence_range()` | `Optional[range]` | Range of available sequence numbers |
| `observations_in_buffer()` | `Optional[int]` | Count of observations currently buffered |
| `buffer_utilization_percent()` | `Optional[float]` | Percentage of buffer capacity used |
| `is_buffer_nearly_full(threshold=90)` | `bool` | Whether buffer is above threshold |
| `sequence_is_available(seq)` | `bool` | Whether a specific sequence number is in range |
| `is_test_mode()` | `bool` | Whether agent is in test mode |

### Sequence Number Rules

- `first_sequence <= last_sequence` — enforced in `__post_init__`
- `next_sequence` = `last_sequence + 1` typically
- When `from < first_sequence`, data was overwritten (buffer overflow)
- Clients must track `next_sequence` for gap-free streaming

## Response Documents (`responses.py`)

Three response document classes mapping 1:1 to the MTConnect REST API endpoints:

### `MTConnectDevices` — `/probe`

```python
@dataclass
class MTConnectDevices:
    header: Header
    devices: List[Device]
```

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_device_by_name(name)` | `Optional[Device]` | Lookup by device name |
| `get_device_by_uuid(uuid)` | `Optional[Device]` | Lookup by device UUID |
| `device_count()` | `int` | Number of devices |

### `MTConnectStreams` — `/current`, `/sample`

```python
@dataclass
class MTConnectStreams:
    header: Header
    streams: List[DeviceStream]
```

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_device_stream(name)` | `Optional[DeviceStream]` | Stream by device name |
| `get_device_stream_by_uuid(uuid)` | `Optional[DeviceStream]` | Stream by device UUID |
| `total_observations()` | `int` | Total observations across all streams |
| `has_any_faults()` | `bool` | Any FAULT conditions present |
| `has_any_warnings()` | `bool` | Any WARNING conditions present |
| `devices_with_faults()` | `List[str]` | Device names with active faults |
| `devices_with_warnings()` | `List[str]` | Device names with warnings |
| `sequence_range()` | `Optional[Tuple]` | Min/max sequence across all observations |

### `MTConnectAssets` — `/assets`

```python
@dataclass
class MTConnectAssets:
    header: Header
    assets: List[Asset]
```

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_asset(asset_id)` | `Optional[Asset]` | Lookup by asset ID |
| `get_assets_by_type(type)` | `List[Asset]` | Filter by asset type |
| `removed_assets()` | `List[Asset]` | Assets marked as removed |
| `active_assets()` | `List[Asset]` | Non-removed assets |
| `asset_count()` / `active_asset_count()` | `int` | Total / active count |

## Streams (`streams.py`)

### `ComponentStream`

Represents one component's observations within a device stream. Groups observations by category:

```python
@dataclass
class ComponentStream:
    component: str            # Component type name (e.g., "Controller", "Linear")
    component_id: ID
    name: Optional[str]
    native_name: Optional[str]
    uuid: Optional[str]
    sample_interval: Optional[float]
    sample_rate: Optional[float]
    samples: List[SampleValue]
    events: List[EventValue]
    condition: List[ConditionObservation]
```

| Method | Returns | Purpose |
|--------|---------|---------|
| `all_observations()` | `List` | Combined samples + events + conditions |
| `observation_count()` | `int` | Total observation count |
| `has_faults()` / `has_warnings()` | `bool` | Condition checks |
| `get_sample_by_id(id)` | `Optional[SampleValue]` | Lookup sample by data item ID |
| `get_event_by_id(id)` | `Optional[EventValue]` | Lookup event by data item ID |

### `DeviceStream`

Represents all streams for a single device:

```python
@dataclass
class DeviceStream:
    name: str
    uuid: UUID
    component_streams: List[ComponentStream]
```

| Method | Returns | Purpose |
|--------|---------|---------|
| `add_component_stream(cs)` | — | Append a component stream |
| `get_component_stream(id)` | `Optional[ComponentStream]` | Lookup by component ID |
| `all_observations()` | `List` | All observations across components |
| `observation_count()` | `int` | Total observations for device |
| `has_faults()` / `has_warnings()` | `bool` | Any faults/warnings in any component |
| `components_with_faults()` | `List[str]` | Component IDs with active faults |
| `components_with_warnings()` | `List[str]` | Component IDs with active warnings |

## Error Handling (`errors.py`)

### Error Codes

```python
class ErrorCode(Enum):
    INVALID_REQUEST = auto()
    INVALID_XPATH = auto()
    OUT_OF_RANGE = auto()
    TOO_MANY = auto()
    UNSUPPORTED = auto()
    INTERNAL_ERROR = auto()
    ASSET_NOT_FOUND = auto()
    QUERY_ERROR = auto()
    UNAUTHORIZED = auto()
    NO_DEVICE = auto()
```

### Error Response Document

```python
@dataclass
class MTConnectError:
    header: Header
    errors: List[Error]    # Must be non-empty (validated in __post_init__)
```

Methods: `primary_error()`, `has_error_code(code)`, `error_messages()`

### Exception Hierarchy

```
MTConnectProtocolException          # Base — message + optional error_code
├── InvalidRequestException         # INVALID_REQUEST
├── OutOfRangeException             # OUT_OF_RANGE + sequence details
├── AssetNotFoundException          # ASSET_NOT_FOUND + asset_id
└── UnsupportedFeatureException     # UNSUPPORTED + feature name
```

### Factory Function

`raise_from_error_response(error_response: MTConnectError)` dispatches to the correct exception subclass based on the primary error code.

## MTConnect REST API Mapping

| Endpoint | Response Class | Container | Data Source |
|----------|---------------|-----------|-------------|
| `/probe` | `MTConnectDevices` | `devices: List[Device]` | Device model hierarchy |
| `/current` | `MTConnectStreams` | `streams: List[DeviceStream]` | Latest snapshot |
| `/sample` | `MTConnectStreams` | `streams: List[DeviceStream]` | Historical buffer |
| `/assets` | `MTConnectAssets` | `assets: List[Asset]` | Asset storage |
| (any error) | `MTConnectError` | `errors: List[Error]` | Error details |

## Implementation Guidelines

### When Adding a New Response Field

1. Add the field to the appropriate dataclass with proper type annotation
2. Add type coercion in `__post_init__` if the field can receive raw strings
3. Add validation constraints (non-negative, non-empty, etc.)
4. Add semantic query methods if the field enables useful lookups
5. Update `__init__.py` exports if adding a new public class
6. Write tests in `tests/protocol/`

### When Adding a New Error Code

1. Add the member to `ErrorCode` enum
2. Optionally create a specific exception subclass
3. Update `raise_from_error_response()` dispatch logic
4. Document the HTTP status code mapping

### When Adding Streaming Features

The streaming model follows MTConnect's chunked transfer encoding pattern:
- `interval` parameter triggers continuous updates
- `heartbeat` maintains connection during quiet periods
- Sequence tracking enables gap detection and resynchronization

When implementing streaming-related features:
1. Respect the `first_sequence <= last_sequence` invariant
2. Track `next_sequence` for continuous consumption
3. Handle buffer overflow (requested sequence < `first_sequence`)
4. Use `Header.sequence_is_available()` for range checks

## Existing Tests

- `tests/protocol/test_header.py` — Header creation, sequence validation (`first > last` raises `ValueError`), `has_sequence_info()`, `observations_in_buffer()`, `buffer_utilization_percent()`, `sequence_is_available()`

## XML/JSON Response Format Reference

All protocol classes model both XML and JSON response formats. When implementing serialization:

**XML**: Elements with attributes, child elements nested
```xml
<MTConnectStreams>
  <Header creationTime="..." sender="..." instanceId="..." version="..." />
  <Streams>
    <DeviceStream name="..." uuid="...">
      <ComponentStream component="..." componentId="...">
        <Samples>...</Samples>
        <Events>...</Events>
        <Condition>...</Condition>
      </ComponentStream>
    </DeviceStream>
  </Streams>
</MTConnectStreams>
```

**JSON**: Parallel structure with arrays for repeated elements
```json
{
  "MTConnectStreams": {
    "Header": { "creationTime": "...", "sender": "..." },
    "Streams": [{ "DeviceStream": { "name": "...", "uuid": "..." } }]
  }
}
```
