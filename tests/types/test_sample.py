"""
Tests for SampleType enum.
"""

from mtconnect.types.sample import SampleType


def test_sample_type_enum_exists():
    """Test that SampleType enum is importable and has expected values"""
    assert hasattr(SampleType, "POSITION")
    assert hasattr(SampleType, "TEMPERATURE")
    assert hasattr(SampleType, "VELOCITY")
    assert hasattr(SampleType, "LOAD")


def test_sample_type_value():
    """Test that SampleType uses auto() for values"""
    # auto() generates integer values
    assert isinstance(SampleType.POSITION.value, int)
    assert isinstance(SampleType.TEMPERATURE.value, int)


def test_sample_type_count():
    """Test expected number of SAMPLE types"""
    # Should have 94 SAMPLE types from model_2.6.xml
    assert len(list(SampleType)) == 94
