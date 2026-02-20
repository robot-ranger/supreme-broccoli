"""
MTConnect Observation Value Models

Value classes representing actual observations from equipment, including samples,
events, and conditions with timestamps, sequence numbers, and validation.

Reference: MTConnect Standard v2.6 - Observation Information Model
"""

from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime
from enum import Enum

from mtconnect.types.primitives import ID, MTCDateTime
from mtconnect.types.condition import ConditionLevel, ConditionQualifier


class UnavailableType(Enum):
    """Special marker for unavailable data"""
    UNAVAILABLE = "UNAVAILABLE"


@dataclass
class ObservationValue:
    """
    Base class for all observation values.
    
    Represents a single observation from a DataItem with timestamp and sequence
    number for ordering and tracking in the data stream.
    """
    data_item_id: ID
    timestamp: MTCDateTime
    sequence: int
    name: Optional[str] = None
    sub_type: Optional[str] = None
    composition_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate observation after initialization"""
        if isinstance(self.data_item_id, str):
            self.data_item_id = ID(self.data_item_id)
        
        if isinstance(self.timestamp, str):
            self.timestamp = MTCDateTime(self.timestamp)
        
        if not isinstance(self.sequence, int) or self.sequence < 0:
            raise ValueError(f"Sequence must be non-negative integer, got {self.sequence}")


@dataclass
class SampleValue(ObservationValue):
    """
    SAMPLE observation value representing a numeric measurement.
    
    Contains numeric values for continuously variable measurements such as
    position, temperature, velocity, etc. May be UNAVAILABLE if the data
    source is disconnected or not providing data.
    
    Example:
        >>> temp = SampleValue(
        ...     data_item_id="spindle_temp",
        ...     timestamp=MTCDateTime("2026-02-19T10:30:00Z"),
        ...     sequence=12345,
        ...     value=45.7,
        ...     native_value=45.7,
        ...     units="CELSIUS"
        ... )
    """
    value: Union[float, int, UnavailableType]
    native_value: Optional[Union[float, int]] = None
    units: Optional[str] = None
    native_units: Optional[str] = None
    sample_rate: Optional[float] = None
    statistic: Optional[str] = None  # AVERAGE, MINIMUM, MAXIMUM, etc.
    duration: Optional[float] = None  # Duration for statistical samples
    
    def is_unavailable(self) -> bool:
        """Check if this observation is unavailable"""
        return self.value == UnavailableType.UNAVAILABLE
    
    def numeric_value(self) -> Optional[float]:
        """Get the numeric value, or None if unavailable"""
        if self.is_unavailable():
            return None
        return float(self.value)


@dataclass
class EventValue(ObservationValue):
    """
    EVENT observation value representing discrete state or status.
    
    Contains string or enumerated values for discrete information such as
    execution state, program name, controller mode, etc. May be UNAVAILABLE
    if the data source is disconnected.
    
    Example:
        >>> exec_state = EventValue(
        ...     data_item_id="controller_exec",
        ...     timestamp=MTCDateTime("2026-02-19T10:30:00Z"),
        ...     sequence=12346,
        ...     value="ACTIVE"
        ... )
    """
    value: Union[str, int, bool, UnavailableType]
    native_value: Optional[Union[str, int, bool]] = None
    
    def is_unavailable(self) -> bool:
        """Check if this observation is unavailable"""
        return self.value == UnavailableType.UNAVAILABLE
    
    def string_value(self) -> Optional[str]:
        """Get the string value, or None if unavailable"""
        if self.is_unavailable():
            return None
        return str(self.value)


@dataclass
class ConditionObservation(ObservationValue):
    """
    CONDITION observation representing health status.
    
    Contains condition level (NORMAL, WARNING, FAULT, UNAVAILABLE), native code,
    and message describing the condition. Multiple conditions can exist
    simultaneously for a single DataItem.
    
    Example:
        >>> temp_fault = ConditionObservation(
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
    level: ConditionLevel
    native_code: Optional[str] = None
    native_severity: Optional[str] = None
    qualifier: Optional[ConditionQualifier] = None
    message: Optional[str] = None
    
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
