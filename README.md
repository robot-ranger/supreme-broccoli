# supreme-broccoli
ai agent for transpiling mtconnect

## Modules

### MTConnect DataItem Types

- **[event_types.py](event_types.py)** - All EVENT category DataItem types from MTConnect v2.6 normative model
- **[sample_types.py](sample_types.py)** - All SAMPLE category DataItem types from MTConnect v2.6 normative model
- **[condition_types.py](condition_types.py)** - All CONDITION category DataItem types from MTConnect v2.6 normative model
- **[subtype.py](subtype.py)** - All DataItem subType values from MTConnect v2.6 normative model

### MTConnect Primitives

- **[mtconnect_primitives.py](mtconnect_primitives.py)** - Python classes and type aliases for MTConnect primitive datatypes

## Usage

```python
from event_types import EventType
from sample_types import SampleType
from condition_types import ConditionType
from subtype import DataItemSubType

# Example: Use DataItem types
position_type = SampleType.POSITION
execution_type = EventType.EXECUTION
system_condition = ConditionType.SYSTEM

# Example: Use DataItem subtypes
actual_subtype = DataItemSubType.ACTUAL
commanded_subtype = DataItemSubType.COMMANDED
programmed_subtype = DataItemSubType.PROGRAMMED
```

## Reference

Based on MTConnect Standard v2.6 Normative Model
