"""
Tests for MTConnect Component models.
"""

import pytest
from mtconnect.models.components import (
    Device,
    Controller,
    Linear,
    Rotary,
    Spindle,
    Description,
)
from mtconnect.types.primitives import ID, UUID


def test_device_creation():
    """Test Device creation with required fields"""
    device = Device(
        id=ID("mill"),
        name="Mill-01",
        uuid=UUID("M8010W4194N")
    )
    
    assert device.id == ID("mill")
    assert device.name == "Mill-01"
    assert device.uuid == UUID("M8010W4194N")


def test_device_with_description():
    """Test Device with Description metadata"""
    desc = Description(
        manufacturer="ACME Corp",
        model="CNC-5000",
        serial_number="SN12345"
    )
    
    device = Device(
        id=ID("mill"),
        name="Mill-01",
        description=desc
    )
    
    assert device.description.manufacturer == "ACME Corp"
    assert device.description.serial_number == "SN12345"


def test_device_add_component():
    """Test adding components to a device"""
    device = Device(id=ID("mill"), name="Mill-01")
    controller = Controller(id=ID("cnc"), name="Controller")
    
    device.add_component(controller)
    
    assert len(device.components) == 1
    assert device.components[0] == controller


def test_linear_component():
    """Test Linear component creation"""
    x_axis = Linear(
        id=ID("x"),
        name="X",
        native_name="X-Axis"
    )
    
    assert x_axis.id == ID("x")
    assert x_axis.name == "X"
    assert x_axis.native_name == "X-Axis"


def test_spindle_component():
    """Test Spindle component creation"""
    spindle = Spindle(
        id=ID("sp1"),
        name="Spindle"
    )
    
    assert spindle.id == ID("sp1")
