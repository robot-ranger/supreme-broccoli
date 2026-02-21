"""
MTConnect Protocol

REST API response document structures, headers, streams, and error handling
for MTConnect protocol communication.

Reference: MTConnect Standard v2.6 - Protocol Specification
"""

# Header
from mtconnect.protocol.header import Header

# Response documents
from mtconnect.protocol.responses import (
    MTConnectDevices,
    MTConnectStreams,
    MTConnectAssets,
)

# Stream structures
from mtconnect.protocol.streams import (
    ComponentStream,
    DeviceStream,
)

# Error handling
from mtconnect.protocol.errors import (
    Error,
    ErrorCode,
    MTConnectError,
    MTConnectProtocolException,
    InvalidRequestException,
    OutOfRangeException,
    AssetNotFoundException,
    UnsupportedFeatureException,
    raise_from_error_response,
)

__all__ = [
    # Header
    "Header",
    # Responses
    "MTConnectDevices",
    "MTConnectStreams",
    "MTConnectAssets",
   # Streams
    "ComponentStream",
    "DeviceStream",
    # Errors
    "Error",
    "ErrorCode",
    "MTConnectError",
    "MTConnectProtocolException",
    "InvalidRequestException",
    "OutOfRangeException",
    "AssetNotFoundException",
    "UnsupportedFeatureException",
    "raise_from_error_response",
]
