"""
MTConnect Observation Value Models

Value classes representing actual observations from equipment, including samples,
events, and conditions with timestamps, sequence numbers, and validation.

Reference: MTConnect Standard v2.6 - Observation Information Model
"""

from dataclasses import dataclass, field
from typing import Optional, Union
from datetime import datetime
from enum import Enum

from mtconnect.types.primitives import ID, MTCDateTime
from mtconnect.types.condition import ConditionLevel, ConditionQualifier
from mtconnect.types.subtype import DataItemSubType


class UnavailableType(Enum):
    """Special marker for unavailable data"""
    UNAVAILABLE = "UNAVAILABLE"


@dataclass
class Observation:
    """
    Base class for all observation values.
    
    Represents a single observation from a DataItem with timestamp and sequence
    number for ordering and tracking in the data stream.
    """
    data_item_id: ID
    timestamp: MTCDateTime
    sequence: int
    name: Optional[str] = field(default=None)
    sub_type: Optional[DataItemSubType] = field(default=None)
    composition_id: Optional[ID] = field(default=None)
    
    def __post_init__(self):
        """Validate observation after initialization"""
        if isinstance(self.data_item_id, str):
            self.data_item_id = ID(self.data_item_id)
        
        if isinstance(self.timestamp, str):
            self.timestamp = MTCDateTime(self.timestamp)
        
        if not isinstance(self.sequence, int) or self.sequence < 0:
            raise ValueError(f"Sequence must be non-negative integer, got {self.sequence}")


@dataclass
class Sample(Observation):
    """
    SAMPLE observation value representing a numeric measurement.
    
    Contains numeric values for continuously variable measurements such as
    position, temperature, velocity, etc. May be UNAVAILABLE if the data
    source is disconnected or not providing data.
    
    Example:
        >>> temp = Sample(
        ...     data_item_id="spindle_temp",
        ...     timestamp=MTCDateTime("2026-02-19T10:30:00Z"),
        ...     sequence=12345,
        ...     value=45.7,
        ...     native_value=45.7,
        ...     units="CELSIUS"
        ... )
    """
    value: Union[float, int, UnavailableType] = field(default=UnavailableType.UNAVAILABLE)
    native_value: Optional[Union[float, int]] = field(default=None)
    units: Optional[str] = field(default=None)
    native_units: Optional[str] = field(default=None)
    sample_rate: Optional[float] = field(default=None)
    statistic: Optional[str] = field(default=None)  # AVERAGE, MINIMUM, MAXIMUM, etc.
    duration: Optional[float] = field(default=None)  # Duration for statistical samples
    
    def is_unavailable(self) -> bool:
        """Check if this observation is unavailable"""
        return self.value == UnavailableType.UNAVAILABLE
    
    def numeric_value(self) -> Optional[float]:
        """Get the numeric value, or None if unavailable"""
        if self.is_unavailable():
            return None
        return float(self.value)


@dataclass
class Event(Observation):
    """
    EVENT observation value representing discrete state or status.
    
    Contains string or enumerated values for discrete information such as
    execution state, program name, controller mode, etc. May be UNAVAILABLE
    if the data source is disconnected.
    
    Example:
        >>> exec_state = Event(
        ...     data_item_id="controller_exec",
        ...     timestamp=MTCDateTime("2026-02-19T10:30:00Z"),
        ...     sequence=12346,
        ...     value="ACTIVE"
        ... )
    """
    value: Union[str, int, bool, UnavailableType] = field(default=UnavailableType.UNAVAILABLE)
    native_value: Optional[Union[str, int, bool]] = field(default=None)
    
    def is_unavailable(self) -> bool:
        """Check if this observation is unavailable"""
        return self.value == UnavailableType.UNAVAILABLE
    
    def string_value(self) -> Optional[str]:
        """Get the string value, or None if unavailable"""
        if self.is_unavailable():
            return None
        return str(self.value)


@dataclass
class Condition(Observation):
    """
    CONDITION observation representing health status.
    
    Contains condition level (NORMAL, WARNING, FAULT, UNAVAILABLE), native code,
    and message describing the condition. Multiple conditions can exist
    simultaneously for a single DataItem.
    
    Example:
        >>> temp_fault = Condition(

        ...     data_item_id="spindle_temp_cond",
        ...     timestamp=MTCDateTime("2026-02-19T10:30:00Z"),
        ...     sequence=12347,
        ...     level=ConditionLevel.FAULT,
        ...     native_code="T1234",
        ...     native_severity="5",
        ...     qualifier=ConditionQualifier.HIGH,
        ...     message="Spindle temperature exceeds maximum limit"
        ... )
    """
    level: ConditionLevel = field(default=ConditionLevel.UNAVAILABLE)
    native_code: Optional[str] = field(default=None)
    native_severity: Optional[str] = field(default=None)
    qualifier: Optional[ConditionQualifier] = field(default=None)
    message: Optional[str] = field(default=None)
    
    def is_normal(self) -> bool:
        """Check if condition is normal (healthy)"""
        return self.level == ConditionLevel.NORMAL
    
    def is_fault(self) -> bool:
        """Check if condition is a fault"""
        return self.level == ConditionLevel.FAULT
    
    def is_warning(self) -> bool:
        """Check if condition is a warning"""
        return self.level == ConditionLevel.WARNING
    
    def is_unavailable(self) -> bool:
        """Check if condition monitoring is unavailable"""
        return self.level == ConditionLevel.UNAVAILABLE
    
    def severity_rank(self) -> int:
        """
        Get numeric severity rank for comparison.
        
        Returns:
            0 for NORMAL, 1 for WARNING, 2 for FAULT, 3 for UNAVAILABLE
        """
        severity_map = {
            ConditionLevel.NORMAL: 0,
            ConditionLevel.WARNING: 1,
            ConditionLevel.FAULT: 2,
            ConditionLevel.UNAVAILABLE: 3
        }
        return severity_map.get(self.level, 3)


@dataclass
class TimeSeries:
    """
    Time series data representation for high-frequency sampling.
    
    Provides an efficient representation of multiple samples at a fixed rate,
    reducing the overhead of individual timestamps and metadata for each value.
    """
    sample_count: int
    sample_rate: float  # Samples per second
    values: list[float]
    
    def __post_init__(self):
        """Validate time series"""
        if len(self.values) != self.sample_count:
            raise ValueError(f"Expected {self.sample_count} values, got {len(self.values)}")
        
        if self.sample_rate <= 0:
            raise ValueError(f"Sample rate must be positive, got {self.sample_rate}")
    
    def duration_seconds(self) -> float:
        """Calculate total duration of the time series"""
        return self.sample_count / self.sample_rate
    
    def timestamp_at_index(self, start_time: datetime, index: int) -> datetime:
        """Calculate timestamp for a specific sample index"""
        if index < 0 or index >= self.sample_count:
            raise IndexError(f"Index {index} out of range [0, {self.sample_count})")
        
        offset_seconds = index / self.sample_rate
        from datetime import timedelta
        return start_time + timedelta(seconds=offset_seconds)


@dataclass
class DataSet:
    """
    Data set representation for key-value pairs.
    
    Provides a collection of related measurements as key-value pairs, useful
    for structured data like transformation matrices, multiple related values,
    or configuration parameters.
    """
    entries: dict[str, Union[float, int, str]]
    
    def get_numeric(self, key: str) -> Optional[float]:
        """Get a numeric value from the dataset"""
        value = self.entries.get(key)
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def get_string(self, key: str) -> Optional[str]:
        """Get a string value from the dataset"""
        value = self.entries.get(key)
        return str(value) if value is not None else None


@dataclass
class SpecificationLimitsValue:
    """
    Specification limits as an EVENT observation value (runtime data).
    
    Runtime observation data for specification limits that define acceptable
    ranges for measurements. This is the observed/reported limit data from
    equipment, distinct from ConfigSpecificationLimits in Configuration.
    
    Reference: MTConnect Standard v2.6 - SpecificationLimits EVENT type (lines 27449-27470 in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    nominal: Optional[float] = None
    lower_limit: Optional[float] = None
    
    def is_within_spec(self, value: float) -> bool:
        """Check if a value is within specification limits"""
        if self.upper_limit is not None and value > self.upper_limit:
            return False
        if self.lower_limit is not None and value < self.lower_limit:
            return False
        return True


@dataclass
class ControlLimitsValue:
    """
    Statistical process control limits as an EVENT observation value (runtime data).
    
    Runtime observation data for statistical process control limits indicating
    whether a process variable is stable and in control. This is the observed/
    reported limit data from equipment, distinct from ConfigControlLimits.
    
    Reference: MTConnect Standard v2.6 - ControlLimits EVENT type (lines 27429-27448 in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    nominal: Optional[float] = None
    lower_limit: Optional[float] = None
    
    def is_in_control(self, value: float) -> bool:
        """Check if a value indicates process is in control"""
        if self.upper_limit is not None and value > self.upper_limit:
            return False
        if self.lower_limit is not None and value < self.lower_limit:
            return False
        return True


@dataclass
class AlarmLimitsValue:
    """
    Alarm threshold limits as an EVENT observation value (runtime data).
    
    Runtime observation data for alarm limits used to trigger warning or alarm
    indicators. This is the observed/reported limit data from equipment,
    distinct from ConfigAlarmLimits in Configuration.
    
    Reference: MTConnect Standard v2.6 - AlarmLimits EVENT type (lines 27409-27428 in model_2.6.xml)
    """
    upper_limit: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    lower_limit: Optional[float] = None
    
    def check_alarm(self, value: float) -> Optional[str]:
        """
        Check if value triggers an alarm.
        
        Returns:
            "UPPER_LIMIT", "UPPER_WARNING", "LOWER_WARNING", "LOWER_LIMIT", or None
        """
        if self.upper_limit is not None and value > self.upper_limit:
            return "UPPER_LIMIT"
        if self.upper_warning is not None and value > self.upper_warning:
            return "UPPER_WARNING"
        if self.lower_limit is not None and value < self.lower_limit:
            return "LOWER_LIMIT"
        if self.lower_warning is not None and value < self.lower_warning:
            return "LOWER_WARNING"
        return None

