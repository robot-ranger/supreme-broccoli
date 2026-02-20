"""
MTConnect Reference Models

Reference models for establishing connections between components, data items,
and assets in the MTConnect information model.

References (ComponentRef, DataItemRef, AssetRef) allow one entity to reference
another by ID. This is distinct from Relationships (ConfigurationRelationship)
which describe associations between equipment and only exist in Configuration.

Reference: MTConnect Standard v2.6 - References Package
"""

from dataclasses import dataclass
from typing import Optional

from mtconnect.types.primitives import ID, UUID
from mtconnect.types.enums import DataItemRelationshipTypeEnum


@dataclass
class ComponentRef:
    """
    Reference to a Component by ID or ID path.
    
    Provides a way to reference another Component in the device hierarchy,
    used for associations, compositions, and relationships.
    """
    id_ref: ID
    name: Optional[str] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.id_ref, str):
            self.id_ref = ID(self.id_ref)


@dataclass
class DataItemRef:
    """
    Reference to a DataItem by ID.
    
    Establishes relationships between DataItems, such as pairing a measured value
    with its specification limits, control limits, or alarm thresholds.
    
    Reference: MTConnect Standard v2.6 - DataItemRef (lines 51538-51564 in model_2.6.xml)
    """
    id_ref: ID
    name: Optional[str] = None
    relationship_type: Optional[DataItemRelationshipTypeEnum] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.id_ref, str):
            self.id_ref = ID(self.id_ref)


@dataclass
class AssetRef:
    """
    Reference to an Asset by asset ID.
    
    Associates a Component or DataItem with an Asset, such as linking a Spindle
    component to the currently loaded CuttingTool asset.
    
    Note: While not explicitly defined as a Reference subclass in the normative
    model, AssetRef provides practical utility for referencing assets by ID
    similar to ComponentRef and DataItemRef patterns.
    """
    asset_id: ID
    asset_type: Optional[str] = None
    device_uuid: Optional[UUID] = None
    
    def __post_init__(self):
        """Validate reference"""
        if isinstance(self.asset_id, str):
            self.asset_id = ID(self.asset_id)
        
        if self.device_uuid and isinstance(self.device_uuid, str):
            self.device_uuid = UUID(self.device_uuid)
