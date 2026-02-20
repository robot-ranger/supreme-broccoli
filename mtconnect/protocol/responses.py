"""
MTConnect Protocol Responses

Response document structures for MTConnect REST API endpoints.

Reference: MTConnect Standard v2.6 - Protocol Responses
"""

from dataclasses import dataclass, field
from typing import List

from mtconnect.protocol.header import Header
from mtconnect.protocol.streams import DeviceStream
from mtconnect.models.components import Device
from mtconnect.models.assets import Asset


@dataclass
class MTConnectDevices:
    """
    MTConnectDevices response from /probe endpoint.
    
    Contains the complete device information model including component hierarchy,
    data item definitions, and device metadata. This is the discovery document
    that describes what data is available from the agent.
    
    Example:
        >>> devices_response = MTConnectDevices(
        ...     header=Header(...),
        ...     devices=[
        ...         Device(id="mill", name="Mill-01", ...)
        ...     ]
        ... )
    
    Reference: MTConnect Standard v2.6 - /probe endpoint
    """
    header: Header
    devices: List[Device] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate devices response"""
        if not self.devices:
            # Empty devices list is valid (e.g., agent starting up)
            pass
    
    def get_device_by_name(self, name: str) -> Device | None:
        """Find a device by name"""
        for device in self.devices:
            if device.name == name:
                return device
        return None
    
    def get_device_by_uuid(self, uuid: str) -> Device | None:
        """Find a device by UUID"""
        for device in self.devices:
            if device.uuid and str(device.uuid) == uuid:
                return device
        return None
    
    def device_count(self) -> int:
        """Get number of devices in response"""
        return len(self.devices)


@dataclass
class MTConnectStreams:
    """
    MTConnectStreams response from /current or /sample endpoints.
    
    Contains observation data organized by device and component streams.
    Returned from /current (snapshot) endpoint or /sample (historical/streaming)
    endpoint.
    
    Example:
        >>> streams_response = MTConnectStreams(
        ...     header=Header(...),
        ...     streams=[
        ...         DeviceStream(name="Mill-01", ...)
        ...     ]
        ... )
    
    Reference: MTConnect Standard v2.6 - /current and /sample endpoints
    """
    header: Header
    streams: List[DeviceStream] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate streams response"""
        # Empty streams list is valid (no data available)
        pass
    
    def get_device_stream(self, device_name: str) -> DeviceStream | None:
        """Find a device stream by device name"""
        for stream in self.streams:
            if stream.name == device_name:
                return stream
        return None
    
    def get_device_stream_by_uuid(self, uuid: str) -> DeviceStream | None:
        """Find a device stream by UUID"""
        for stream in self.streams:
            if str(stream.uuid) == uuid:
                return stream
        return None
    
    def total_observations(self) -> int:
        """Get total number of observations across all devices"""
        return sum(stream.observation_count() for stream in self.streams)
    
    def has_any_faults(self) -> bool:
        """Check if any device stream has faults"""
        return any(stream.has_faults() for stream in self.streams)
    
    def has_any_warnings(self) -> bool:
        """Check if any device stream has warnings"""
        return any(stream.has_warnings() for stream in self.streams)
    
    def devices_with_faults(self) -> List[DeviceStream]:
        """Get list of device streams that have faults"""
        return [stream for stream in self.streams if stream.has_faults()]
    
    def devices_with_warnings(self) -> List[DeviceStream]:
        """Get list of device streams that have warnings"""
        return [stream for stream in self.streams if stream.has_warnings()]
    
    def sequence_range(self) -> tuple[int, int] | None:
        """Get the sequence range from header"""
        return self.header.available_sequence_range()


@dataclass
class MTConnectAssets:
    """
    MTConnectAssets response from /assets endpoint.
    
    Contains asset documents such as cutting tools, parts, raw materials,
    and other lifecycle objects tracked through the manufacturing process.
    
    Example:
        >>> assets_response = MTConnectAssets(
        ...     header=Header(...),
        ...     assets=[
        ...         CuttingTool(asset_id="T12", ...),
        ...         Part(asset_id="P1001", ...)
        ...     ]
        ... )
    
    Reference: MTConnect Standard v2.6 - /assets endpoint
    """
    header: Header
    assets: List[Asset] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate assets response"""
        # Empty assets list is valid
        pass
    
    def get_asset(self, asset_id: str) -> Asset | None:
        """Find an asset by ID"""
        for asset in self.assets:
            if str(asset.asset_id) == asset_id:
                return asset
        return None
    
    def get_assets_by_type(self, asset_type: str) -> List[Asset]:
        """Get all assets of a specific type"""
        return [
            asset for asset in self.assets
            if asset.__class__.__name__ == asset_type
        ]
    
    def removed_assets(self) -> List[Asset]:
        """Get list of removed assets"""
        return [asset for asset in self.assets if asset.removed]
    
    def active_assets(self) -> List[Asset]:
        """Get list of active (not removed) assets"""
        return [asset for asset in self.assets if not asset.removed]
    
    def asset_count(self) -> int:
        """Get total number of assets in response"""
        return len(self.assets)
    
    def active_asset_count(self) -> int:
        """Get number of active assets"""
        return len(self.active_assets())
