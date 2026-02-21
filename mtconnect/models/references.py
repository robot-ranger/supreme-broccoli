"""
MTConnect References Model.

Auto-generated from model_2.6.xml - DO NOT EDIT.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from mtconnect.types.primitives import ID

if TYPE_CHECKING:
    from mtconnect.models.components import Component
    from mtconnect.models.data_items import DataItem


__all__ = [
    'ComponentRef',
    'DataItemRef',
    'Reference',
]

@dataclass
class Reference:
    """pointer to information that is associated with another entity defined elsewhere in the MTConnectDevices entity for a piece of equipment."""

    # pointer to the DataItem::id that contains the information to be associated with this entity.
    data_item_id: ID
    # pointer to the `id` of an entity that contains the information to be associated with this entity.
    id_ref: ID
    # pointer to the DataItem::id that contains the information to be associated with this entity.
    ref_data_item_id: ID
    # name of an element or a piece of equipment.
    name: Optional[str] = None

@dataclass
class DataItemRef(Reference):
    """Reference that is a pointer to a DataItem associated with another entity defined for a piece of equipment."""

    # pointer to the DataItem::id that contains the information to be associated with this entity.
    id_ref: DataItem

    def __post_init__(self):
        """Validate required fields."""
        if self.id_ref is None:
            raise ValueError(f'DataItemRef.id_ref is required')

@dataclass
class ComponentRef(Reference):
    """Reference that is a pointer to all of the information associated with another entity defined for a piece of equipment."""

    # pointer to the Component::id that contains the information to be associated with this entity.
    id_ref: Component

    def __post_init__(self):
        """Validate required fields."""
        if self.id_ref is None:
            raise ValueError(f'ComponentRef.id_ref is required')
