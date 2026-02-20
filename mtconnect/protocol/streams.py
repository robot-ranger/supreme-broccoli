"""
MTConnect Protocol Streams

Stream structures for organizing observation data by device and component.

Reference: MTConnect Standard v2.6 - MTConnectStreams response
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union

from mtconnect.types.primitives import ID, UUID
from mtconnect.models.values import SampleValue, EventValue, ConditionObservation


@dataclass
class ComponentStream:
    """
    Stream of observations from a single Component.
    
    Groups all observations (Samples, Events, Conditions) from a specific
    component in the device hierarchy. Observations are organized by category
    for efficient access.
    
    Example:
        >>> comp_stream = ComponentStream(
        ...     component="Controller",
        ...     component_id="cnc",
        ...     name="Controller",
        ...     samples=[...],
        ...     events=[...],
        ...     condition=[...]
        ... )
    """
    component: str  # Component type (e.g., "Controller", "Linear", "Spindle")
    component_id: ID
    name: Optional[str] = None
    native_name: Optional[str] = None
    uuid: Optional[UUID] = None
    sample_interval: Optional[float] = None
    sample_rate: Optional[float] = None
    
    # Observations organized by category
    samples: List[SampleValue] = field(default_factory=list)
    events: List[EventValue] = field(default_factory=list)
    condition: List[ConditionObservation] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate component stream"""
        if isinstance(self.component_id, str):
            self.component_id = ID(self.component_id)
        
        if self.uuid and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)
    
    def all_observations(self) -> List[Union[SampleValue, EventValue, ConditionObservation]]:
        """Get all observations from this component stream"""
        return self.samples + self.events + self.condition
    
    def observation_count(self) -> int:
        """Get total number of observations in this stream"""
        return len(self.samples) + len(self.events) + len(self.condition)
    
    def has_faults(self) -> bool:
        """Check if any condition observations are faults"""
        return any(cond.is_fault() for cond in self.condition)
    
    def has_warnings(self) -> bool:
        """Check if any condition observations are warnings"""
        return any(cond.is_warning() for cond in self.condition)
    
    def get_sample_by_id(self, data_item_id: str) -> Optional[SampleValue]:
        """Find a sample observation by DataItem ID"""
        for sample in self.samples:
            if str(sample.data_item_id) == data_item_id:
                return sample
        return None
    
    def get_event_by_id(self, data_item_id: str) -> Optional[EventValue]:
        """Find an event observation by DataItem ID"""
        for event in self.events:
            if str(event.data_item_id) == data_item_id:
                return event
        return None


@dataclass
class DeviceStream:
    """
    Stream of all observations from a single Device.
    
    Organizes observations from all components in a device hierarchy,
    providing the complete data stream for one piece of equipment.
    
    Example:
        >>> device_stream = DeviceStream(
        ...     name="Mill-01",
        ...     uuid="M8010W4194N",
        ...     component_streams=[
        ...         ComponentStream(component="Controller", ...),
        ...         ComponentStream(component="Linear", ...),
        ...         ComponentStream(component="Spindle", ...)
        ...     ]
        ... )
    """
    name: str
    uuid: UUID
    component_streams: List[ComponentStream] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate device stream"""
        if isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)
    
    def add_component_stream(self, stream: ComponentStream) -> None:
        """Add a component stream to this device"""
        self.component_streams.append(stream)
    
    def get_component_stream(self, component_id: str) -> Optional[ComponentStream]:
        """Find a component stream by component ID"""
        for stream in self.component_streams:
            if str(stream.component_id) == component_id:
                return stream
        return None
    
    def all_observations(self) -> List[Union[SampleValue, EventValue, ConditionObservation]]:
        """Get all observations from all components"""
        observations = []
        for stream in self.component_streams:
            observations.extend(stream.all_observations())
        return observations
    
    def observation_count(self) -> int:
        """Get total number of observations across all components"""
        return sum(stream.observation_count() for stream in self.component_streams)
    
    def has_faults(self) -> bool:
        """Check if any component has fault conditions"""
        return any(stream.has_faults() for stream in self.component_streams)
    
    def has_warnings(self) -> bool:
        """Check if any component has warning conditions"""
        return any(stream.has_warnings() for stream in self.component_streams)
    
    def components_with_faults(self) -> List[ComponentStream]:
        """Get list of component streams that have faults"""
        return [stream for stream in self.component_streams if stream.has_faults()]
    
    def components_with_warnings(self) -> List[ComponentStream]:
        """Get list of component streams that have warnings"""
        return [stream for stream in self.component_streams if stream.has_warnings()]
