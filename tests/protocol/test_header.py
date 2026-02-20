"""
Tests for MTConnect Header.
"""

import pytest
from mtconnect.protocol.header import Header
from mtconnect.types.primitives import MTCDateTime, Version


def test_header_creation(sample_header):
    """Test Header creation with all fields"""
    assert sample_header.sender == "test-agent"
    assert sample_header.instance_id == 1234567890
    assert sample_header.buffer_size == 10000


def test_header_sequence_validation():
    """Test that first_sequence must be <= last_sequence"""
    with pytest.raises(ValueError):
        Header(
            creation_time=MTCDateTime("2026-02-19T10:30:00Z"),
            sender="test-agent",
            instance_id=123,
            version=Version("2.6.0"),
            first_sequence=5000,
            last_sequence=1000  # Invalid: first > last
        )


def test_header_has_sequence_info(sample_header):
    """Test has_sequence_info() method"""
    assert sample_header.has_sequence_info() is True


def test_header_observations_in_buffer(sample_header):
    """Test observations_in_buffer() calculation"""
    # first=1000, last=5000 → 4001 observations
    assert sample_header.observations_in_buffer() == 4001


def test_header_buffer_utilization(sample_header):
    """Test buffer utilization calculation"""
    util = sample_header.buffer_utilization_percent()
    # 4001 / 10000 * 100 = 40.01%
    assert util is not None
    assert 40.0 <= util <= 40.1


def test_header_sequence_is_available(sample_header):
    """Test checking if sequence is in buffer"""
    assert sample_header.sequence_is_available(3000) is True
    assert sample_header.sequence_is_available(999) is False
    assert sample_header.sequence_is_available(5001) is False
