"""
MTConnect DataItem Models

DataItem definitions representing observation points for data collection from
manufacturing equipment. DataItems are categorized as SAMPLE, EVENT, or CONDITION
and define the type, units,constraints, and metadata for equipment observations.

Reference: MTConnect Standard v2.6 - Observation Information Model  
"""

from dataclasses import dataclass, field
from typing import Optional, List, Union
from enum import Enum

from mtconnect.types.primitives import ID
from mtconnect.types.sample import SampleType
from mtconnect.types.event import EventType
from mtconnect.types.condition import ConditionType
from mtconnect.types.subtype import DataItemSubType


class DataItemCategory(Enum):
    """MTConnect DataItem categories"""
    SAMPLE = "SAMPLE"
    EVENT = "EVENT"
    CONDITION = "CONDITION"


@dataclass
class Constraints:
    """
    Constraints defining valid value ranges or sets for a DataItem.
    
    Provides validation boundaries including minimum/maximum values and
    nominal values for measurements.
    """
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    nominal: Optional[float] = None
    values: Optional[List[str]] = None


@dataclass
class DataItem:
    """
    Base class for all MTConnect DataItems.
    
    A DataItem represents a measurement or observation point on a Component.
    It defines what is measured (type), how it's measured (category), and any
    constraints or metadata about the measurement.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1623082330438_892066_4246
    """
    id: ID
    type: Union[SampleType, EventType, ConditionType, str]
    category: DataItemCategory
    name: Optional[str] = None
    sub_type: Optional[DataItemSubType] = None
    units: Optional[str] = None
    native_units: Optional[str] = None
    native_scale: Optional[float] = None
    significant_digits: Optional[int] = None
    coordinate_system: Optional[str] = None
    composition_id: Optional[str] = None
    constraints: Optional[Constraints] = None
    discrete: bool = False
    
    def __post_init__(self):
        """Validate DataItem after initialization"""
        if not isinstance(self.id, (ID, str)):
            raise TypeError(f"DataItem id must be ID or str, got {type(self.id)}")
        if isinstance(self.id, str):
            self.id = ID(self.id)
        
        # Validate category matches type
        if isinstance(self.type, SampleType) and self.category != DataItemCategory.SAMPLE:
            raise ValueError(f"SampleType {self.type} requires SAMPLE category")
        if isinstance(self.type, EventType) and self.category != DataItemCategory.EVENT:
            raise ValueError(f"EventType {self.type} requires EVENT category")
        if isinstance(self.type, ConditionType) and self.category != DataItemCategory.CONDITION:
            raise ValueError(f"ConditionType {self.type} requires CONDITION category")


@dataclass
class SampleDataItem(DataItem):
    """
    DataItem representing continuously variable numeric measurements.
    
    SAMPLE DataItems report numeric values that vary continuously over time,
    such as position, velocity, temperature, load, etc. They always have units
    and may include statistical information (average, minimum, maximum, etc.).
    
    Examples: POSITION, TEMPERATURE, VELOCITY, LOAD, AMPERAGE, PRESSURE
    
    Reference: MTConnect Standard v2.6 - SAMPLE category
    """
    category: DataItemCategory = field(default=DataItemCategory.SAMPLE, init=False)
    
    def __post_init__(self):
        """Validate SAMPLE-specific requirements"""
        super().__post_init__()
        
        if not isinstance(self.type, (SampleType, str)):
            raise TypeError(f"SampleDataItem type must be SampleType, got {type(self.type)}")
        
        # SAMPLE DataItems should have units
        if not self.units:
            print(f"Warning: SAMPLE DataItem {self.id} missing units specification")


@dataclass
class EventDataItem(DataItem):
    """
    DataItem representing discrete, non-numeric state or status information.
    
    EVENT DataItems report discrete values that change in response to specific
    occurrences or state transitions. Values are typically strings or enumerations
    rather than continuous numeric measurements.
    
    Examples: EXECUTION, CONTROLLER_MODE, PROGRAM, PART_COUNT, DOOR_STATE
    
    Reference: MTConnect Standard v2.6 - EVENT category
    """
    category: DataItemCategory = field(default=DataItemCategory.EVENT, init=False)
    
    def __post_init__(self):
        """Validate EVENT-specific requirements"""
        super().__post_init__()
        
        if not isinstance(self.type, (EventType, str)):
            raise TypeError(f"EventDataItem type must be EventType, got {type(self.type)}")
        
        # EVENT DataItems typically don't have units (except count types)
        if self.units and 'COUNT' not in str(self.type):
            print(f"Warning: EVENT DataItem {self.id} has units (unusual for non-count events)")


@dataclass
class ConditionDataItem(DataItem):
    """
    DataItem representing the health status of a Component.
    
    CONDITION DataItems report the operational health and status of equipment
    components. They use hierarchical severity levels (NORMAL < WARNING < FAULT < 
    UNAVAILABLE) and can report multiple simultaneous conditions.
    
    Examples: SYSTEM, LOGIC_PROGRAM, MOTION_PROGRAM, ACTUATOR, COMMUNICATIONS
    
    Reference: MTConnect Standard v2.6 - CONDITION category
    """
    category: DataItemCategory = field(default=DataItemCategory.CONDITION, init=False)
    
    def __post_init__(self):
        """Validate CONDITION-specific requirements"""
        super().__post_init__()
        
        if not isinstance(self.type, (ConditionType, str)):
            raise TypeError(f"ConditionDataItem type must be ConditionType, got {type(self.type)}")
        
        # CONDITION DataItems don't have units
        if self.units:
            raise ValueError(f"CONDITION DataItem {self.id} cannot have units")


def create_data_item(
    id: str,
    type: Union[SampleType, EventType, ConditionType, str],
    category: DataItemCategory,
    **kwargs
) -> DataItem:
    """
    Factory function to create the appropriate DataItem subclass based on category.
    
    Args:
        id: Unique identifier for the DataItem
        type: DataItem type (SampleType, EventType, or ConditionType)
        category: Category (SAMPLE, EVENT, or CONDITION)
        **kwargs: Additional DataItem attributes
    
    Returns:
        Appropriate DataItem subclass instance
    
    Example:
        >>> position_item = create_data_item(
        ...     id="x_pos",
        ...     type=SampleType.POSITION,
        ...     category=DataItemCategory.SAMPLE,
        ...     sub_type=DataItemSubType.ACTUAL,
        ...     units="MILLIMETER"
        ... )
    """
    if category == DataItemCategory.SAMPLE:
        return SampleDataItem(id=id, type=type, **kwargs)
    elif category == DataItemCategory.EVENT:
        return EventDataItem(id=id, type=type, **kwargs)
    elif category == DataItemCategory.CONDITION:
        return ConditionDataItem(id=id, type=type, **kwargs)
    else:
        raise ValueError(f"Unknown category: {category}")
