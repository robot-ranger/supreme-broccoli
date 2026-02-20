"""
Tests for MTConnect primitive types.
"""

import pytest
from mtconnect.types.primitives import (
    ID,
    UUID,
    Int32,
    MTCDateTime,
    Version,
)


def test_id_creation():
    """Test ID type creation and validation"""
    id_val = ID("my_data_item")
    assert str(id_val) == "my_data_item"


def test_id_invalid():
    """Test ID validation fails for invalid identifiers"""
    with pytest.raises(ValueError):
        ID("")  # Empty ID not allowed


def test_uuid_extends_id():
    """Test that UUID extends ID"""
    uuid = UUID("M8010W4194N")
    assert isinstance(uuid, ID)
    assert isinstance(uuid, UUID)


def test_int32_range():
    """Test Int32 validates range constraints"""
    # Valid values
    Int32(0)
    Int32(2147483647)
    Int32(-2147483648)
    
    # Out of range
    with pytest.raises(ValueError):
        Int32(2147483648)
    with pytest.raises(ValueError):
        Int32(-2147483649)


def test_mtc_datetime_parsing():
    """Test MTCDateTime parses ISO 8601 format"""
    dt = MTCDateTime("2026-02-19T10:30:45.123Z")
    assert str(dt).endswith("Z")


def test_version_comparison():
    """Test Version comparison operators"""
    v1 = Version("2.6.0")
    v2 = Version("2.5.0")
    v3 = Version("2.6.1")
    
    assert v1 > v2
    assert v1 < v3
    assert v1 == Version("2.6.0")
