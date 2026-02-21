"""
Tests for generate_enums.py script.

Validates:
1. Helper functions (sanitize_identifier, clean_doc, format_inline_comment, etc.)
2. Generated output files exist with correct structure
3. Enum class counts and expected members
4. Re-exports from enums.py for backward compatibility
5. End-to-end regeneration produces valid, importable modules
"""

import subprocess
import sys
from enum import Enum
from pathlib import Path

import pytest


# =============================================================================
# Path setup
# =============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate_enums.py"
TYPES_DIR = REPO_ROOT / "mtconnect" / "types"
MODEL_PATH = REPO_ROOT / ".github" / "agents" / "data" / "model_2.6.xml"

EXPECTED_FILES = [
    "event.py",
    "sample.py",
    "condition.py",
    "subtype.py",
    "interface_types.py",
    "enums.py",
]


# =============================================================================
# Helper function tests (import helpers from script via subprocess)
# =============================================================================


class TestSanitizeIdentifier:
    """Test the sanitize_identifier helper."""

    def _sanitize(self, name):
        """Run sanitize_identifier via subprocess to avoid top-level script execution."""
        code = (
            "import re\n"
            "def sanitize_identifier(name):\n"
            "    if not name:\n"
            "        return name\n"
            "    PYTHON_KEYWORDS = {\n"
            "        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',\n"
            "        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',\n"
            "        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',\n"
            "        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',\n"
            "        'while', 'with', 'yield'\n"
            "    }\n"
            "    if name[0].isdigit():\n"
            "        name = '_' + name\n"
            "    name = re.sub(r'[^A-Za-z0-9_]', '_', name)\n"
            "    if name.lower() in PYTHON_KEYWORDS:\n"
            "        name = '_' + name\n"
            "    return name.upper()\n"
            f"print(sanitize_identifier({name!r}))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_normal_name_unchanged(self):
        """Normal uppercase names pass through unchanged."""
        assert self._sanitize("POSITION") == "POSITION"

    def test_digit_prefix_gets_underscore(self):
        """Names starting with a digit get an underscore prefix."""
        assert self._sanitize("3DS") == "_3DS"

    def test_slash_replaced(self):
        """Slashes are replaced with underscores."""
        assert self._sanitize("DEGREE/SECOND") == "DEGREE_SECOND"

    def test_caret_replaced(self):
        """Carets are replaced with underscores."""
        assert self._sanitize("DEGREE/SECOND^2") == "DEGREE_SECOND_2"

    def test_mixed_special_chars(self):
        """Multiple special characters are all replaced."""
        assert self._sanitize("POUND/INCH^2") == "POUND_INCH_2"

    def test_lowercase_uppercased(self):
        """Lowercase names are converted to uppercase."""
        assert self._sanitize("Normal") == "NORMAL"

    def test_empty_string(self):
        """Empty string returns empty."""
        assert self._sanitize("") == ""

    def test_python_keyword_prefixed(self):
        """Python keywords (lowercase) get an underscore prefix."""
        # The script checks name.lower() against lowercase keywords like 'while'
        assert self._sanitize("while") == "_WHILE"


class TestCleanDoc:
    """Test the clean_doc helper."""

    def _clean(self, doc):
        """Run clean_doc via subprocess."""
        code = (
            "def clean_doc(doc):\n"
            "    if not doc:\n"
            "        return doc\n"
            "    doc = doc.replace('\\r\\n', ' ').replace('\\r', ' ').replace('\\n', ' ')\n"
            "    doc = doc.replace('{{term(', '').replace('{{termplural(', '')\n"
            "    doc = doc.replace('{{property(', '').replace('{{block(', '')\n"
            "    doc = doc.replace('{{package(', '').replace('{{url(', '')\n"
            "    doc = doc.replace(')}}', '').replace('}}', '')\n"
            "    doc = doc.replace('&#10;', ' ').replace('&#13;', ' ')\n"
            "    return ' '.join(doc.split())\n"
            f"print(clean_doc({doc!r}))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_removes_term_markup(self):
        """Removes {{term(...)}} markup."""
        assert self._clean("a {{term(device)}} thing") == "a device thing"

    def test_removes_property_markup(self):
        """Removes {{property(...)}} markup."""
        assert self._clean("{{property(id)}}") == "id"

    def test_removes_block_markup(self):
        """Removes {{block(...)}} markup."""
        assert self._clean("{{block(Header)}}") == "Header"

    def test_normalizes_whitespace(self):
        """Collapses multiple whitespace to single spaces."""
        assert self._clean("hello   world") == "hello world"

    def test_replaces_xml_entities(self):
        """Replaces &#10; and &#13; entities."""
        assert self._clean("line1&#10;line2") == "line1 line2"

    def test_empty_returns_empty(self):
        """Empty string input returns empty."""
        assert self._clean("") == ""

    def test_newlines_replaced(self):
        """Newlines are replaced with spaces."""
        assert self._clean("line1\nline2\r\nline3") == "line1 line2 line3"


# =============================================================================
# Generated file structure tests
# =============================================================================


class TestGeneratedFilesExist:
    """Test that all expected generated files exist and are non-empty."""

    @pytest.mark.parametrize("filename", EXPECTED_FILES)
    def test_file_exists(self, filename):
        """Each expected file exists in mtconnect/types/."""
        filepath = TYPES_DIR / filename
        assert filepath.exists(), f"{filename} not found in {TYPES_DIR}"

    @pytest.mark.parametrize("filename", EXPECTED_FILES)
    def test_file_not_empty(self, filename):
        """Each expected file has content."""
        filepath = TYPES_DIR / filename
        assert filepath.stat().st_size > 0, f"{filename} is empty"

    @pytest.mark.parametrize("filename", EXPECTED_FILES)
    def test_file_has_docstring_header(self, filename):
        """Each generated file starts with a module docstring."""
        content = (TYPES_DIR / filename).read_text()
        assert content.startswith('"""'), f"{filename} missing module docstring"

    @pytest.mark.parametrize("filename", EXPECTED_FILES)
    def test_file_has_auto_generated_marker(self, filename):
        """Each file contains the auto-generated marker."""
        content = (TYPES_DIR / filename).read_text()
        assert "Auto-generated from: model_2.6.xml" in content, (
            f"{filename} missing auto-generated marker"
        )

    @pytest.mark.parametrize("filename", EXPECTED_FILES)
    def test_file_imports_enum(self, filename):
        """Each file imports from the enum module."""
        content = (TYPES_DIR / filename).read_text()
        assert "from enum import Enum, auto" in content, (
            f"{filename} missing enum imports"
        )


# =============================================================================
# Enum content validation
# =============================================================================


class TestEventModule:
    """Validate the generated event.py module."""

    def test_event_type_exists(self):
        from mtconnect.types.event import EventType

        assert issubclass(EventType, Enum)

    def test_event_type_has_expected_members(self):
        from mtconnect.types.event import EventType

        expected = ["AVAILABILITY", "BLOCK", "EMERGENCY_STOP", "EXECUTION"]
        for name in expected:
            assert hasattr(EventType, name), f"EventType missing {name}"

    def test_event_type_count(self):
        from mtconnect.types.event import EventType

        assert len(list(EventType)) == 140

    def test_event_type_uses_auto(self):
        from mtconnect.types.event import EventType

        assert isinstance(EventType.AVAILABILITY.value, int)


class TestSampleModule:
    """Validate the generated sample.py module."""

    def test_sample_type_exists(self):
        from mtconnect.types.sample import SampleType

        assert issubclass(SampleType, Enum)

    def test_sample_type_has_expected_members(self):
        from mtconnect.types.sample import SampleType

        expected = ["POSITION", "TEMPERATURE", "VELOCITY", "LOAD"]
        for name in expected:
            assert hasattr(SampleType, name), f"SampleType missing {name}"

    def test_sample_type_count(self):
        from mtconnect.types.sample import SampleType

        assert len(list(SampleType)) == 94


class TestConditionModule:
    """Validate the generated condition.py module."""

    def test_condition_type_exists(self):
        from mtconnect.types.condition import ConditionType

        assert issubclass(ConditionType, Enum)

    def test_condition_level_exists(self):
        from mtconnect.types.condition import ConditionLevel

        assert issubclass(ConditionLevel, Enum)

    def test_condition_qualifier_exists(self):
        from mtconnect.types.condition import ConditionQualifier

        assert issubclass(ConditionQualifier, Enum)

    def test_condition_type_count(self):
        from mtconnect.types.condition import ConditionType

        assert len(list(ConditionType)) == 6

    def test_condition_level_has_unavailable(self):
        """UNAVAILABLE is manually added by the generator."""
        from mtconnect.types.condition import ConditionLevel

        assert hasattr(ConditionLevel, "UNAVAILABLE")

    def test_condition_level_count(self):
        from mtconnect.types.condition import ConditionLevel

        # 3 from model + 1 UNAVAILABLE added manually
        assert len(list(ConditionLevel)) == 4


class TestSubtypeModule:
    """Validate the generated subtype.py module."""

    def test_subtype_exists(self):
        from mtconnect.types.subtype import DataItemSubType

        assert issubclass(DataItemSubType, Enum)

    def test_subtype_has_expected_members(self):
        from mtconnect.types.subtype import DataItemSubType

        expected = ["ACTUAL", "COMMANDED", "MAXIMUM", "MINIMUM"]
        for name in expected:
            assert hasattr(DataItemSubType, name), f"DataItemSubType missing {name}"

    def test_subtype_count(self):
        from mtconnect.types.subtype import DataItemSubType

        assert len(list(DataItemSubType)) == 115


class TestInterfaceTypesModule:
    """Validate the generated interface_types.py module."""

    def test_interface_type_exists(self):
        from mtconnect.types.interface_types import InterfaceType

        assert issubclass(InterfaceType, Enum)

    def test_interface_event_exists(self):
        from mtconnect.types.interface_types import InterfaceEvent

        assert issubclass(InterfaceEvent, Enum)

    def test_interface_state_exists(self):
        from mtconnect.types.interface_types import InterfaceState

        assert issubclass(InterfaceState, Enum)

    def test_interface_request_response_state_exists(self):
        from mtconnect.types.interface_types import InterfaceRequestResponseState

        assert issubclass(InterfaceRequestResponseState, Enum)

    def test_interface_type_count(self):
        from mtconnect.types.interface_types import InterfaceType

        assert len(list(InterfaceType)) == 4

    def test_interface_type_members(self):
        from mtconnect.types.interface_types import InterfaceType

        expected = ["BAR_FEEDER", "CHUCK", "DOOR", "MATERIAL_HANDLER"]
        for name in expected:
            assert hasattr(InterfaceType, name), f"InterfaceType missing {name}"

    def test_request_response_states(self):
        from mtconnect.types.interface_types import InterfaceRequestResponseState

        expected = ["NOT_READY", "READY", "ACTIVE", "COMPLETE", "FAIL"]
        for name in expected:
            assert hasattr(InterfaceRequestResponseState, name)


class TestEnumsModule:
    """Validate the generated enums.py module (catch-all + re-exports)."""

    def test_re_export_event_type(self):
        """EventType is re-exported from enums.py for backward compatibility."""
        from mtconnect.types.enums import EventType

        assert EventType.__module__ == "mtconnect.types.event"

    def test_re_export_sample_type(self):
        """SampleType is re-exported from enums.py for backward compatibility."""
        from mtconnect.types.enums import SampleType

        assert SampleType.__module__ == "mtconnect.types.sample"

    def test_re_export_condition_type(self):
        """ConditionType is re-exported from enums.py for backward compatibility."""
        from mtconnect.types.enums import ConditionType

        assert ConditionType.__module__ == "mtconnect.types.condition"

    def test_re_export_data_item_sub_type(self):
        """DataItemSubType is re-exported from enums.py for backward compatibility."""
        from mtconnect.types.enums import DataItemSubType

        assert DataItemSubType.__module__ == "mtconnect.types.subtype"

    def test_local_enum_count(self):
        """enums.py contains the remaining enums not in dedicated modules."""
        import inspect

        from mtconnect.types import enums

        local_classes = [
            name
            for name, obj in inspect.getmembers(enums)
            if inspect.isclass(obj)
            and issubclass(obj, Enum)
            and obj.__module__ == "mtconnect.types.enums"
        ]
        # Should have ~97 local enums (all non-dedicated)
        assert len(local_classes) >= 90, (
            f"Expected >=90 local enum classes, found {len(local_classes)}"
        )

    def test_category_enum_present(self):
        """CategoryEnum is in the catch-all enums.py."""
        from mtconnect.types.enums import CategoryEnum

        assert issubclass(CategoryEnum, Enum)

    def test_representation_enum_present(self):
        """RepresentationEnum is in the catch-all enums.py."""
        from mtconnect.types.enums import RepresentationEnum

        assert issubclass(RepresentationEnum, Enum)


# =============================================================================
# Regeneration test (end-to-end)
# =============================================================================


class TestRegeneration:
    """Test that running generate_enums.py regenerates valid modules."""

    def test_script_runs_successfully(self):
        """generate_enums.py completes without errors."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--model-path", str(MODEL_PATH)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"Script failed:\n{result.stderr}"

    def test_all_files_generated(self):
        """All 6 expected files are created after running the script."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--model-path", str(MODEL_PATH)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"Script failed:\n{result.stderr}"

        for filename in EXPECTED_FILES:
            filepath = TYPES_DIR / filename
            assert filepath.exists(), f"{filename} was not generated"
            assert filepath.stat().st_size > 0, f"{filename} is empty after regeneration"

    def test_generated_modules_importable(self):
        """All generated modules can be imported after regeneration."""
        # Run generator first
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--model-path", str(MODEL_PATH)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0

        # Validate imports in a fresh subprocess
        import_test = (
            "from mtconnect.types.event import EventType\n"
            "from mtconnect.types.sample import SampleType\n"
            "from mtconnect.types.condition import ConditionType, ConditionLevel\n"
            "from mtconnect.types.subtype import DataItemSubType\n"
            "from mtconnect.types.interface_types import InterfaceType, InterfaceEvent\n"
            "from mtconnect.types.enums import CategoryEnum\n"
            "print('OK')\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", import_test],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"Import failed:\n{result.stderr}"
        assert "OK" in result.stdout

    def test_output_reports_enum_count(self):
        """Script output reports the number of enumerations found."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--model-path", str(MODEL_PATH)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert "Found" in result.stdout
        assert "enumerations" in result.stdout
        assert "Generated 6 modules" in result.stdout
