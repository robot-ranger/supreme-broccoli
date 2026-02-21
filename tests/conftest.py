"""
Pytest configuration and fixtures for MTConnect tests.
"""

import uuid

import pytest
from datetime import datetime

from mtconnect.types.primitives import ID, UUID, MTCDateTime, Version
from mtconnect.types.sample import SampleType
from mtconnect.types.event import EventType
from mtconnect.protocol.header import Header


@pytest.fixture
def sample_header():
    """Create a sample MTConnect header for testing"""
    return Header(
        creation_time=MTCDateTime("2026-02-19T10:30:00Z"),
        sender="test-agent",
        instance_id=1234567890,
        version=Version("2.6.0"),
        buffer_size=10000,
        first_sequence=1000,
        last_sequence=5000,
        next_sequence=5001
    )


@pytest.fixture
def sample_device_uuid():
    """Create a sample device UUID for testing"""
    return UUID("550e8400-e29b-41d4-a716-446655440000")


@pytest.fixture
def sample_data_item_id():
    """Create a sample DataItem ID for testing"""
    return ID("x_pos_actual")


@pytest.fixture
def sample_timestamp():
    """Create a sample ISO 8601 timestamp for testing"""
    return MTCDateTime("2026-02-19T10:30:45.123Z")
