"""
Tests for MTConnect model generation validation.

This test module validates that the generated models follow the correct patterns:
1. Required field validation (e.g., Door requires door_state)
2. [0..0] cardinality exclusion (leaf components don't have composition/component fields)
3. Optional vs required field handling
4. TYPE_CHECKING imports work correctly
5. Dataclass field ordering (required fields before optional)
"""

import pytest
from mtconnect.types.primitives import ID


class TestRequiredFieldValidation:
    """Test that required relationships are properly validated."""
    
    def test_door_requires_door_state(self):
        """Door component must have door_state [1..1] relationship."""
        from mtconnect.models.components import Door
        
        # Should raise ValueError when door_state is missing
        with pytest.raises(ValueError, match="observesDoorState"):
            Door(
                id=ID("door1"),
                name="MainDoor"
            )
    
    def test_interface_requires_interface_state(self):
        """Interface component must have interface_state [1..1] relationship."""
        from mtconnect.models.components import Interface
        
        # Should raise ValueError when interface_state is missing
        with pytest.raises(ValueError, match="observesInterfaceState"):
            Interface(
                id=ID("interface1"),
                name="RobotInterface"
            )
    
    def test_part_occurrence_requires_part_id(self):
        """PartOccurrence component must have part_id [1..1] relationship."""
        from mtconnect.models.components import PartOccurrence
        
        # Should raise ValueError when part_id is missing
        with pytest.raises(ValueError, match="observesPartId"):
            PartOccurrence(
                id=ID("part1"),
                name="Bracket"
            )
    
    def test_door_succeeds_with_required_field(self):
        """Door can be created when door_state is provided."""
        from mtconnect.models.components import Door
        from mtconnect.models.data_items import EventDataItem
        from mtconnect.types.event import EventType
        
        door_state = EventDataItem(
            id=ID("ds1"),
            type=EventType.DOOR_STATE,
            category="EVENT"
        )
        
        door = Door(
            id=ID("door1"),
            name="MainDoor",
            door_state=door_state
        )
        
        assert door.id == ID("door1")
        assert door.door_state is door_state


class TestCardinalityExclusion:
    """Test that [0..0] cardinality properly excludes fields from leaf components."""
    
    def test_workpiece_no_compositions(self):
        """Workpiece (leaf) should not have composition field."""
        from mtconnect.models.components import Workpiece
        
        workpiece = Workpiece(
            id=ID("wp1"),
            name="Part123"
        )
        
        # Should not have composition or components fields
        assert not hasattr(workpiece, 'composition')
        assert not hasattr(workpiece, 'components')
    
    def test_amplifier_no_compositions(self):
        """Amplifier (leaf) should not have composition field."""
        from mtconnect.models.components import Amplifier
        
        amp = Amplifier(
            id=ID("amp1"),
            name="PowerAmp"
        )
        
        assert not hasattr(amp, 'composition')
        assert not hasattr(amp, 'components')
    
    def test_fan_no_compositions(self):
        """Fan (leaf) should not have composition field."""
        from mtconnect.models.components import Fan
        
        fan = Fan(
            id=ID("fan1"),
            name="CoolingFan"
        )
        
        assert not hasattr(fan, 'composition')
        assert not hasattr(fan, 'components')
    
    def test_ballscrew_no_compositions(self):
        """Ballscrew (leaf) should not have composition field."""
        from mtconnect.models.components import Ballscrew
        
        ballscrew = Ballscrew(
            id=ID("bs1"),
            name="BallScrew"
        )
        
        assert not hasattr(ballscrew, 'composition')
        assert not hasattr(ballscrew, 'components')
    
    def test_encoder_no_compositions(self):
        """Encoder (leaf) should not have composition field."""
        from mtconnect.models.components import Encoder
        
        encoder = Encoder(
            id=ID("enc1"),
            name="PositionEncoder"
        )
        
        assert not hasattr(encoder, 'composition')
        assert not hasattr(encoder, 'components')
    
    def test_drain_no_compositions(self):
        """Drain (leaf) should not have composition field."""
        from mtconnect.models.components import Drain
        
        drain = Drain(
            id=ID("drain1"),
            name="CoolantDrain"
        )
        
        assert not hasattr(drain, 'composition')
        assert not hasattr(drain, 'components')


class TestOptionalVsRequiredFields:
    """Test that optional and required fields are handled correctly."""
    
    def test_component_optional_relationships(self):
        """Components with optional relationships can be created without them."""
        from mtconnect.models.components import Auxiliary
        
        # Auxiliary has optional is_auxiliary_of relationship
        aux = Auxiliary(
            id=ID("aux1"),
            name="CuttingTool"
        )
        
        assert aux.id == ID("aux1")
        assert aux.is_auxiliary_of is None
    
    def test_component_can_have_optional_configs(self):
        """Components can be created without optional configuration."""
        from mtconnect.models.components import Linear
        
        linear = Linear(
            id=ID("x"),
            name="X-Axis"
        )
        
        assert linear.id == ID("x")
        assert linear.configuration is None
    
    def test_part_occurrence_optional_fields_work(self):
        """PartOccurrence can be created with only required part_id."""
        from mtconnect.models.components import PartOccurrence
        from mtconnect.models.data_items import EventDataItem
        from mtconnect.types.event import EventType
        
        part_id = EventDataItem(
            id=ID("pid1"),
            type=EventType.PART_ID,
            category="EVENT"
        )
        
        part_occ = PartOccurrence(
            id=ID("part1"),
            name="Bracket-001",
            part_id=part_id
        )
        
        assert part_occ.id == ID("part1")
        assert part_occ.part_id is part_id
        # Optional fields should be None
        assert part_occ.part_unique_id is None
        assert part_occ.part_group_id is None
        assert part_occ.part_count is None


class TestTypeCheckingImports:
    """Test that TYPE_CHECKING imports work without circular import errors."""
    
    def test_all_model_modules_import(self):
        """All model modules can be imported without circular import errors."""
        # This should not raise ImportError
        from mtconnect.models import (
            Component,
            Device,
            DataItem,
            Configuration,
            Composition,
            ComponentRef,
            DataItemRef,
        )
        
        # Verify classes are importable
        assert Component is not None
        assert Device is not None
        assert DataItem is not None
        assert Configuration is not None
        assert Composition is not None
        assert ComponentRef is not None
        assert DataItemRef is not None
    
    def test_component_dataitem_forward_references(self):
        """Components can use forward references to DataItems."""
        from mtconnect.models.components import Door
        from mtconnect.models.data_items import EventDataItem
        from mtconnect.types.event import EventType
        
        # Create a DataItem
        door_state = EventDataItem(
            id=ID("ds1"),
            type=EventType.DOOR_STATE,
            category="EVENT"
        )
        
        # Use it in a Component (forward reference should work)
        door = Door(
            id=ID("door1"),
            name="MainDoor",
            door_state=door_state
        )
        
        assert door.door_state is door_state
    
    def test_components_module_imports_without_circular_error(self):
        """Components module can import data_items types via TYPE_CHECKING."""
        # This was previously a circular import issue
        # Should not raise ImportError
        from mtconnect.models import components
        
        assert hasattr(components, 'Component')
        assert hasattr(components, 'Door')
        assert hasattr(components, 'Interface')


class TestDataclassFieldOrdering:
    """Test that dataclasses handle mixed required/optional fields correctly."""
    
    def test_door_field_ordering_works(self):
        """Door has correct field ordering (required before optional)."""
        from mtconnect.models.components import Door
        from mtconnect.models.data_items import EventDataItem
        from mtconnect.types.event import EventType
        
        # This should work without "non-default argument follows default argument"
        door_state = EventDataItem(
            id=ID("ds1"),
            type=EventType.DOOR_STATE,
            category="EVENT"
        )
        
        door = Door(
            id=ID("door1"),
            name="MainDoor",
            door_state=door_state
        )
        
        # Verify the instance is created correctly
        assert isinstance(door, Door)
    
    def test_part_occurrence_field_ordering_works(self):
        """PartOccurrence has correct field ordering with many optional fields."""
        from mtconnect.models.components import PartOccurrence
        from mtconnect.models.data_items import EventDataItem
        from mtconnect.types.event import EventType
        
        part_id = EventDataItem(
            id=ID("pid1"),
            type=EventType.PART_ID,
            category="EVENT"
        )
        
        # Should work with required part_id and many optional fields
        part = PartOccurrence(
            id=ID("part1"),
            name="Bracket",
            part_id=part_id
        )
        
        assert isinstance(part, PartOccurrence)
    
    def test_component_inheritance_field_ordering(self):
        """Inherited fields maintain correct ordering."""
        from mtconnect.models.components import Device
        
        # Device inherits from Component - should work correctly
        device = Device(
            id=ID("mill"),
            name="Mill-01"
        )
        
        assert isinstance(device, Device)
        assert device.id == ID("mill")
        assert device.name == "Mill-01"


class TestGeneratedClassCounts:
    """Test that all expected classes were generated."""
    
    def test_components_generated(self):
        """Verify expected number of component classes."""
        from mtconnect.models import components
        
        # Count dataclass definitions
        import inspect
        from dataclasses import is_dataclass
        
        classes = [
            obj for name, obj in inspect.getmembers(components)
            if inspect.isclass(obj) and is_dataclass(obj)
        ]
        
        # Should have ~126 component classes
        assert len(classes) >= 120, f"Expected >=120 component classes, found {len(classes)}"
    
    def test_data_items_generated(self):
        """Verify expected number of DataItem classes."""
        from mtconnect.models import data_items
        
        import inspect
        from dataclasses import is_dataclass
        
        classes = [
            obj for name, obj in inspect.getmembers(data_items)
            if inspect.isclass(obj) and is_dataclass(obj)
        ]
        
        # Should have ~258 DataItem classes
        assert len(classes) >= 250, f"Expected >=250 DataItem classes, found {len(classes)}"
    
    def test_configurations_generated(self):
        """Verify expected number of Configuration classes."""
        from mtconnect.models import configurations
        
        import inspect
        from dataclasses import is_dataclass
        
        classes = [
            obj for name, obj in inspect.getmembers(configurations)
            if inspect.isclass(obj) and is_dataclass(obj)
        ]
        
        # Should have ~31 configuration classes
        assert len(classes) >= 30, f"Expected >=30 configuration classes, found {len(classes)}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
