"""
MTConnect Primitive Datatypes

This module provides Python classes and type aliases for MTConnect primitive datatypes
as defined in the MTConnect standard. These types enforce validation and bounds checking
to ensure data conforms to the MTConnect specification.

Classes are organized hierarchically where specialized types extend base types
(e.g., ID extends string, UUID extends ID).
"""

from dataclasses import dataclass, field
from typing import Union, List, NewType, Any
from datetime import datetime as dt
import re
import uuid as uuid_lib


# ============================================================================
# Basic Type Aliases
# ============================================================================

# Fundamental types that map directly to Python types
MTCBoolean = bool
MTCString = str
MTCInteger = int
MTCFloat = float
MTCDouble = float  # Python's float is double precision
MTCBinary = bytes


# ============================================================================
# Bounded Integer Types
# ============================================================================

@dataclass
class Int32:
    """
    32-bit signed integer type.
    Valid range: -2,147,483,648 to 2,147,483,647
    """
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(f"Int32 requires int, got {type(self.value).__name__}")
        if not (-2147483648 <= self.value <= 2147483647):
            raise ValueError(f"Int32 value {self.value} out of range [-2147483648, 2147483647]")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def __repr__(self) -> str:
        return f"Int32({self.value})"


@dataclass
class Int64:
    """
    64-bit signed integer type.
    Valid range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
    """
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(f"Int64 requires int, got {type(self.value).__name__}")
        if not (-9223372036854775808 <= self.value <= 9223372036854775807):
            raise ValueError(f"Int64 value {self.value} out of range")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def __repr__(self) -> str:
        return f"Int64({self.value})"


@dataclass
class UInt32:
    """
    32-bit unsigned integer type.
    Valid range: 0 to 4,294,967,295
    """
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(f"UInt32 requires int, got {type(self.value).__name__}")
        if not (0 <= self.value <= 4294967295):
            raise ValueError(f"UInt32 value {self.value} out of range [0, 4294967295]")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def __repr__(self) -> str:
        return f"UInt32({self.value})"


@dataclass
class UInt64:
    """
    64-bit unsigned integer type.
    Valid range: 0 to 18,446,744,073,709,551,615
    """
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(f"UInt64 requires int, got {type(self.value).__name__}")
        if not (0 <= self.value <= 18446744073709551615):
            raise ValueError(f"UInt64 value {self.value} out of range")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def __repr__(self) -> str:
        return f"UInt64({self.value})"


# ============================================================================
# String-based Types (Hierarchical)
# ============================================================================

@dataclass
class ID:
    """
    ID type - extends string type.
    Used for unique identifiers in MTConnect documents.
    Must be a valid XML ID (starts with letter or underscore, 
    followed by letters, digits, hyphens, underscores, or periods).
    """
    value: str
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"ID requires str, got {type(self.value).__name__}")
        if not self.value:
            raise ValueError("ID cannot be empty")
        # XML ID validation: must start with letter or underscore
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-\.]*$', self.value):
            raise ValueError(f"Invalid ID format: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"ID('{self.value}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ID):
            return self.value == other.value
        return self.value == other
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class UUID(ID):
    """
    UUID type - extends ID type.
    Universally Unique Identifier conforming to RFC 4122.
    Format: 8-4-4-4-12 hexadecimal digits (e.g., 550e8400-e29b-41d4-a716-446655440000)
    """
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"UUID requires str, got {type(self.value).__name__}")
        try:
            # Validate UUID format
            uuid_obj = uuid_lib.UUID(self.value)
            # Normalize to lowercase with hyphens
            self.value = str(uuid_obj)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid UUID format: {self.value}") from e
    
    def __repr__(self) -> str:
        return f"UUID('{self.value}')"
    
    @classmethod
    def generate(cls) -> 'UUID':
        """Generate a new random UUID (version 4)."""
        return cls(str(uuid_lib.uuid4()))


# ============================================================================
# DateTime Type
# ============================================================================

@dataclass
class MTCDateTime:
    """
    DateTime type for MTConnect.
    Represents a timestamp in ISO 8601 format.
    Can be initialized from string, datetime object, or timestamp float.
    """
    value: dt
    
    def __init__(self, value: Union[str, dt, float]):
        if isinstance(value, str):
            # Parse ISO 8601 string
            self.value = self._parse_iso8601(value)
        elif isinstance(value, dt):
            self.value = value
        elif isinstance(value, (int, float)):
            # Unix timestamp
            self.value = dt.fromtimestamp(value)
        else:
            raise TypeError(f"MTCDateTime requires str, datetime, or numeric timestamp, got {type(value).__name__}")
    
    @staticmethod
    def _parse_iso8601(date_string: str) -> dt:
        """Parse ISO 8601 datetime string with various formats."""
        # Try common formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return dt.strptime(date_string, fmt)
            except ValueError:
                continue
        
        # Fallback to fromisoformat (Python 3.7+)
        try:
            # Handle Z suffix
            if date_string.endswith('Z'):
                date_string = date_string[:-1] + '+00:00'
            return dt.fromisoformat(date_string)
        except ValueError as e:
            raise ValueError(f"Invalid ISO 8601 datetime format: {date_string}") from e
    
    def __str__(self) -> str:
        """Return ISO 8601 formatted string."""
        return self.value.isoformat() + 'Z'
    
    def __repr__(self) -> str:
        return f"MTCDateTime('{self.value.isoformat()}')"
    
    @classmethod
    def now(cls) -> 'MTCDateTime':
        """Create a DateTime with the current time."""
        return cls(dt.now())
    
    def timestamp(self) -> float:
        """Return Unix timestamp."""
        return self.value.timestamp()


# ============================================================================
# Version Type
# ============================================================================

@dataclass
class Version:
    """
    Version type for MTConnect.
    Represents semantic version in format: MAJOR.MINOR.PATCH
    Supports comparison operations.
    """
    major: int
    minor: int
    patch: int = 0
    
    def __init__(self, value: Union[str, tuple]):
        if isinstance(value, str):
            parts = value.split('.')
            if len(parts) < 2 or len(parts) > 3:
                raise ValueError(f"Invalid version format: {value}. Expected MAJOR.MINOR[.PATCH]")
            try:
                self.major = int(parts[0])
                self.minor = int(parts[1])
                self.patch = int(parts[2]) if len(parts) == 3 else 0
            except ValueError as e:
                raise ValueError(f"Invalid version format: {value}. Parts must be integers") from e
        elif isinstance(value, (tuple, list)):
            if len(value) < 2 or len(value) > 3:
                raise ValueError(f"Version tuple must have 2 or 3 elements, got {len(value)}")
            self.major = int(value[0])
            self.minor = int(value[1])
            self.patch = int(value[2]) if len(value) == 3 else 0
        else:
            raise TypeError(f"Version requires str or tuple, got {type(value).__name__}")
        
        # Validate non-negative
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ValueError("Version numbers must be non-negative")
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __repr__(self) -> str:
        return f"Version('{self.major}.{self.minor}.{self.patch}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Version):
            return False
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)
    
    def __ge__(self, other) -> bool:
        return self == other or self > other
    
    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))


# ============================================================================
# XML/XLink Types
# ============================================================================

@dataclass
class XLinkType:
    """
    XLink type attribute value.
    Valid values per XLink specification (typically 'simple', 'extended', 'locator', 'arc', 'resource', 'title', 'none').
    """
    value: str
    
    VALID_TYPES = {'simple', 'extended', 'locator', 'arc', 'resource', 'title', 'none'}
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"XLinkType requires str, got {type(self.value).__name__}")
        if self.value not in self.VALID_TYPES:
            raise ValueError(f"Invalid XLink type: {self.value}. Must be one of {self.VALID_TYPES}")
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"XLinkType('{self.value}')"


@dataclass
class XLinkHref:
    """
    XLink href attribute - URI reference.
    Used to specify the remote resource in XLink.
    """
    value: str
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"XLinkHref requires str, got {type(self.value).__name__}")
        if not self.value:
            raise ValueError("XLinkHref cannot be empty")
        # Basic URI validation - must not contain spaces
        if ' ' in self.value:
            raise ValueError(f"Invalid URI: {self.value}. URIs cannot contain spaces")
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"XLinkHref('{self.value}')"


@dataclass
class XSLang:
    """
    XML language code (xml:lang attribute).
    Specifies the language used in the content.
    Format: ISO 639 language code, optionally followed by ISO 3166 country code.
    Examples: 'en', 'en-US', 'fr-FR'
    """
    value: str
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"XSLang requires str, got {type(self.value).__name__}")
        if not self.value:
            raise ValueError("XSLang cannot be empty")
        # Basic validation: language code format
        if not re.match(r'^[a-z]{2,3}(-[A-Z]{2})?$', self.value):
            raise ValueError(f"Invalid language code format: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"XSLang('{self.value}')"


@dataclass
class X509:
    """
    X.509 certificate or certificate-related data.
    Base64-encoded certificate data.
    """
    value: str
    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"X509 requires str, got {type(self.value).__name__}")
        if not self.value:
            raise ValueError("X509 data cannot be empty")
        # Basic validation: check if it looks like base64
        if not re.match(r'^[A-Za-z0-9+/=\s]+$', self.value):
            raise ValueError("Invalid X509 format: must be base64-encoded")
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"X509('{self.value[:20]}...')"


# ============================================================================
# Array Types
# ============================================================================

@dataclass
class MTCArray:
    """
    Generic array type for MTConnect.
    Represents a space-separated list of values.
    """
    values: List[Union[float, int, str]]
    
    def __post_init__(self):
        if not isinstance(self.values, list):
            raise TypeError(f"MTCArray requires list, got {type(self.values).__name__}")
    
    def __str__(self) -> str:
        return ' '.join(str(v) for v in self.values)
    
    def __repr__(self) -> str:
        return f"MTCArray({self.values})"
    
    def __len__(self) -> int:
        return len(self.values)
    
    def __getitem__(self, index):
        return self.values[index]
    
    @classmethod
    def from_string(cls, value: str) -> 'MTCArray':
        """Parse a space-separated string into an MTCArray."""
        parts = value.split()
        # Try to convert to numbers if possible
        values = []
        for part in parts:
            try:
                if '.' in part or 'e' in part.lower():
                    values.append(float(part))
                else:
                    values.append(int(part))
            except ValueError:
                values.append(part)
        return cls(values)


@dataclass
class Float3D:
    """
    3D float array type.
    Represents a 3-dimensional vector with exactly 3 float values.
    Common for position, rotation, and orientation data.
    """
    x: float
    y: float
    z: float
    
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                # Parse from space-separated string
                parts = args[0].split()
                if len(parts) != 3:
                    raise ValueError(f"Float3D requires exactly 3 values, got {len(parts)}")
                self.x = float(parts[0])
                self.y = float(parts[1])
                self.z = float(parts[2])
            elif isinstance(args[0], (list, tuple)):
                if len(args[0]) != 3:
                    raise ValueError(f"Float3D requires exactly 3 values, got {len(args[0])}")
                self.x = float(args[0][0])
                self.y = float(args[0][1])
                self.z = float(args[0][2])
            else:
                raise TypeError(f"Float3D requires str, list, or tuple, got {type(args[0]).__name__}")
        elif len(args) == 3:
            self.x = float(args[0])
            self.y = float(args[1])
            self.z = float(args[2])
        else:
            raise ValueError(f"Float3D requires exactly 3 values, got {len(args)}")
    
    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z}"
    
    def __repr__(self) -> str:
        return f"Float3D({self.x}, {self.y}, {self.z})"
    
    def __iter__(self):
        return iter([self.x, self.y, self.z])
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError(f"Float3D index out of range: {index}")
    
    def to_list(self) -> List[float]:
        """Convert to list."""
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> tuple:
        """Convert to tuple."""
        return (self.x, self.y, self.z)


# ============================================================================
# Unit Types
# ============================================================================

@dataclass
class Second:
    """
    SECOND unit type - represents a duration in seconds.
    Used for time durations and intervals.
    """
    value: float
    
    def __post_init__(self):
        if not isinstance(self.value, (int, float)):
            raise TypeError(f"Second requires numeric value, got {type(self.value).__name__}")
        if self.value < 0:
            raise ValueError(f"Second value cannot be negative: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"Second({self.value})"
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __int__(self) -> int:
        return int(self.value)
    
    def __add__(self, other):
        if isinstance(other, Second):
            return Second(self.value + other.value)
        return Second(self.value + other)
    
    def __sub__(self, other):
        if isinstance(other, Second):
            return Second(self.value - other.value)
        return Second(self.value - other)
    
    def __mul__(self, other):
        return Second(self.value * other)
    
    def __truediv__(self, other):
        return Second(self.value / other)


# ============================================================================
# Type Union for Convenience
# ============================================================================

MTCPrimitiveType = Union[
    MTCBoolean, MTCString, MTCInteger, MTCFloat, MTCDouble, MTCBinary,
    Int32, Int64, UInt32, UInt64,
    ID, UUID, MTCDateTime, Version,
    XLinkType, XLinkHref, XSLang, X509,
    MTCArray, Float3D, Second
]


# ============================================================================
# Helper Functions
# ============================================================================

def validate_primitive(value: Any, type_name: str) -> bool:
    """
    Validate if a value conforms to a given MTConnect primitive type.
    
    Args:
        value: The value to validate
        type_name: The name of the MTConnect primitive type
        
    Returns:
        True if valid, False otherwise
    """
    type_map = {
        'boolean': MTCBoolean,
        'string': MTCString,
        'integer': MTCInteger,
        'float': MTCFloat,
        'double': MTCDouble,
        'binary': MTCBinary,
        'int32': Int32,
        'int64': Int64,
        'uint32': UInt32,
        'uint64': UInt64,
        'ID': ID,
        'UUID': UUID,
        'datetime': MTCDateTime,
        'version': Version,
        'xlinktype': XLinkType,
        'xlinkhref': XLinkHref,
        'xslang': XSLang,
        'x509': X509,
        'Array': MTCArray,
        'float3d': Float3D,
        'SECOND': Second,
    }
    
    type_class = type_map.get(type_name.lower())
    if type_class is None:
        return False
    
    # For basic types, check isinstance
    if type_class in (MTCBoolean, MTCString, MTCInteger, MTCFloat, MTCDouble, MTCBinary):
        return isinstance(value, type_class)
    
    # For complex types, try to construct and validate
    try:
        type_class(value)
        return True
    except (ValueError, TypeError):
        return False


def convert_to_primitive(value: Any, type_name: str) -> MTCPrimitiveType:
    """
    Convert a value to the specified MTConnect primitive type.
    
    Args:
        value: The value to convert
        type_name: The name of the MTConnect primitive type
        
    Returns:
        The converted value as the appropriate type
        
    Raises:
        ValueError: If conversion fails
        TypeError: If type is not recognized
    """
    type_map = {
        'boolean': lambda v: bool(v),
        'string': lambda v: str(v),
        'integer': lambda v: int(v),
        'float': lambda v: float(v),
        'double': lambda v: float(v),
        'binary': lambda v: v if isinstance(v, bytes) else v.encode('utf-8'),
        'int32': Int32,
        'int64': Int64,
        'uint32': UInt32,
        'uint64': UInt64,
        'ID': ID,
        'UUID': UUID,
        'datetime': MTCDateTime,
        'version': Version,
        'xlinktype': XLinkType,
        'xlinkhref': XLinkHref,
        'xslang': XSLang,
        'x509': X509,
        'Array': MTCArray if isinstance(value, list) else MTCArray.from_string,
        'float3d': Float3D,
        'SECOND': Second,
    }
    
    converter = type_map.get(type_name.lower())
    if converter is None:
        raise TypeError(f"Unknown MTConnect primitive type: {type_name}")
    
    try:
        return converter(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to convert {value} to {type_name}: {e}") from e


__all__ = [
    # Basic types
    'MTCBoolean', 'MTCString', 'MTCInteger', 'MTCFloat', 'MTCDouble', 'MTCBinary',
    # Bounded integer types
    'Int32', 'Int64', 'UInt32', 'UInt64',
    # String-based types
    'ID', 'UUID',
    # DateTime and Version
    'MTCDateTime', 'Version',
    # XML/XLink types
    'XLinkType', 'XLinkHref', 'XSLang', 'X509',
    # Array types
    'MTCArray', 'Float3D',
    # Unit types
    'Second',
    # Union type
    'MTCPrimitiveType',
    # Helper functions
    'validate_primitive', 'convert_to_primitive',
]
