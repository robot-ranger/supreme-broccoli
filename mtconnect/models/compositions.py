"""
MTConnect Compositions Model.

Auto-generated from model_2.6.xml - DO NOT EDIT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, List
from uuid import UUID

from mtconnect.types.primitives import ID
from mtconnect.types.enums import CompositionTypeEnum

if TYPE_CHECKING:
    from mtconnect.models.components import Component, Description
    from mtconnect.models.configurations import Configuration


__all__ = [
    'Composition',
]

@dataclass
class Composition:
    """functional part of a piece of equipment contained within a Component."""

    # unique identifier for the Composition element.
    id: ID
    is_composition_of: Component
    # type of Composition.
    type: CompositionTypeEnum
    configuration: Optional[Configuration] = None
    description: Optional[Description] = None
    # name of the Composition element.
    name: Optional[str] = None
    # universally unique identifier for the Composition.
    uuid: Optional[UUID] = None
