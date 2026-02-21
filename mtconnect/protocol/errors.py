"""
MTConnect Protocol Errors

Error classes and error codes for MTConnect protocol communication.

Reference: MTConnect Standard v2.6 - Protocol Error Handling
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from mtconnect.protocol.header import Header


class ErrorCode(Enum):
    """
    Standard MTConnect error codes.
    
    These codes indicate specific error conditions that can occur during
    MTConnect protocol communication.
    """
    # Request errors (4xx equivalent)
    INVALID_REQUEST = auto()  # Malformed request parameters
    INVALID_XPATH = auto()  # Invalid XPath in path parameter
    OUT_OF_RANGE = auto()  # Sequence number not in buffer
    TOO_MANY = auto()  # Requested count exceeds maximum
    
    # Server errors (5xx equivalent)
    UNSUPPORTED = auto()  # Feature not supported by agent
    INTERNAL_ERROR = auto()  # Internal agent error
    ASSET_NOT_FOUND = auto()  # Requested asset doesn't exist
    QUERY_ERROR = auto()  # Error executing query
    UNAUTHORIZED = auto()  # Authentication required
    NO_DEVICE = auto()  # No device configured


@dataclass
class Error:
    """
    Single error message in an MTConnect error response.
    
    Provides error code and descriptive message explaining what went wrong.
    """
    error_code: ErrorCode
    message: str
    
    def __post_init__(self):
        """Validate error"""
        if isinstance(self.error_code, str):
            try:
                self.error_code = ErrorCode(self.error_code)
            except ValueError:
                # Allow custom error codes
                pass
    
    def __str__(self) -> str:
        """String representation of error"""
        return f"[{self.error_code.value}] {self.message}"


@dataclass
class MTConnectError:
    """
    MTConnect error response document.
    
    Returned when a request cannot be fulfilled, providing error code(s) and
    descriptive messages to help diagnose the issue.
    
    Example:
        >>> error = MTConnectError(
        ...     header=Header(...),
        ...     errors=[
        ...         Error(
        ...             error_code=ErrorCode.OUT_OF_RANGE,
        ...             message="Sequence 1000 is out of range, buffer starts at 5000"
        ...         )
        ...     ]
        ... )
    
    Reference: MTConnect Standard v2.6 - MTConnectError response
    """
    header: Header
    errors: list[Error]
    
    def __post_init__(self):
        """Validate error response"""
        if not self.errors:
            raise ValueError("MTConnectError must contain at least one error")
    
    def primary_error(self) -> Error:
        """Get the first (primary) error"""
        return self.errors[0]
    
    def has_error_code(self, code: ErrorCode) -> bool:
        """Check if response contains a specific error code"""
        return any(err.error_code == code for err in self.errors)
    
    def error_messages(self) -> list[str]:
        """Get list of all error messages"""
        return [err.message for err in self.errors]
    
    def __str__(self) -> str:
        """String representation of error response"""
        if len(self.errors) == 1:
            return str(self.errors[0])
        else:
            messages = "\n".join(f"  - {err}" for err in self.errors)
            return f"Multiple errors:\n{messages}"


class MTConnectProtocolException(Exception):
    """
    Base exception for MTConnect protocol errors.
    
    Raised when protocol-level errors occur during communication with an
    MTConnect agent.
    """
    
    def __init__(self, message: str, error_code: Optional[ErrorCode] = None):
        super().__init__(message)
        self.error_code = error_code


class InvalidRequestException(MTConnectProtocolException):
    """Exception for invalid request parameters"""
    
    def __init__(self, message: str):
        super().__init__(message, ErrorCode.INVALID_REQUEST)


class OutOfRangeException(MTConnectProtocolException):
    """Exception for sequence numbers out of buffer range"""
    
    def __init__(self, message: str, requested: int, first: int, last: int):
        super().__init__(message, ErrorCode.OUT_OF_RANGE)
        self.requested_sequence = requested
        self.first_sequence = first
        self.last_sequence = last


class AssetNotFoundException(MTConnectProtocolException):
    """Exception for asset not found"""
    
    def __init__(self, asset_id: str):
        super().__init__(f"Asset not found: {asset_id}", ErrorCode.ASSET_NOT_FOUND)
        self.asset_id = asset_id


class UnsupportedFeatureException(MTConnectProtocolException):
    """Exception for unsupported features"""
    
    def __init__(self, feature: str):
        super().__init__(f"Feature not supported: {feature}", ErrorCode.UNSUPPORTED)
        self.feature = feature


def raise_from_error_response(error_response: MTConnectError) -> None:
    """
    Convert an MTConnectError response to an appropriate exception and raise it.
    
    Args:
        error_response: The error response document
    
    Raises:
        Appropriate MTConnectProtocolException subclass
    """
    primary = error_response.primary_error()
    
    if primary.error_code == ErrorCode.INVALID_REQUEST:
        raise InvalidRequestException(primary.message)
    elif primary.error_code == ErrorCode.OUT_OF_RANGE:
        raise OutOfRangeException(
            primary.message,
            requested=0,  # Would need to parse from message
            first=0,
            last=0
        )
    elif primary.error_code == ErrorCode.ASSET_NOT_FOUND:
        raise AssetNotFoundException(primary.message)
    elif primary.error_code == ErrorCode.UNSUPPORTED:
        raise UnsupportedFeatureException(primary.message)
    else:
        raise MTConnectProtocolException(primary.message, primary.error_code)
