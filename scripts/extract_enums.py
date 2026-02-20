#!/usr/bin/env python3
"""
Extract all enumeration types from the MTConnect normative model XML
and generate separate Python enum modules.

Generated files:
  - mtconnect/types/event.py          EventEnum -> EventType
  - mtconnect/types/sample.py         SampleEnum -> SampleType
  - mtconnect/types/condition.py      ConditionEnum -> ConditionType (+ ConditionLevel, ConditionQualifier)
  - mtconnect/types/subtype.py        DataItemSubTypeEnum -> DataItemSubType
  - mtconnect/types/interface_types.py InterfaceEventEnum, InterfaceStateEnum, concrete classes
  - mtconnect/types/enums.py          All remaining enums (states, modes, units, etc.)

Usage:
  python scripts/extract_enums.py
  python scripts/extract_enums.py --model-path .github/agents/data/model_2.6.xml
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import argparse
from pathlib import Path
import sys
import re


# =============================================================================
# Helpers
# =============================================================================

def sanitize_identifier(name):
    """
    Transform MTConnect names into valid Python identifiers.

    Rules (KISS approach):
    1. Prepend underscore if starts with digit
    2. Replace all special characters with underscore
    3. Prepend underscore if Python keyword
    """
    if not name:
        return name

    PYTHON_KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield'
    }

    if name[0].isdigit():
        name = '_' + name
    name = re.sub(r'[^A-Za-z0-9_]', '_', name)
    if name.lower() in PYTHON_KEYWORDS:
        name = '_' + name
    return name


def clean_doc(doc):
    """Clean MTConnect model documentation strings."""
    if not doc:
        return doc
    doc = doc.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    doc = doc.replace('{{term(', '').replace('{{termplural(', '')
    doc = doc.replace('{{property(', '').replace('{{block(', '')
    doc = doc.replace('{{package(', '').replace('{{url(', '')
    doc = doc.replace(')}}', '').replace('}}', '')
    doc = doc.replace('&#10;', ' ').replace('&#13;', ' ')
    return ' '.join(doc.split())


def format_inline_comment(doc, max_len=80):
    """Truncate a cleaned doc string for an inline comment."""
    if not doc:
        return ''
    if len(doc) > max_len:
        doc = doc[:max_len - 3] + '...'
    return doc


def extract_elem_doc(elem):
    """Extract the ownedComment body from an XML element."""
    for comment in elem.findall('ownedComment'):
        body = comment.get('body')
        if body:
            return body
    return None


def generate_enum_members(literals, indent='    '):
    """Generate enum member lines with inline comments. No blank lines between members."""
    lines = []
    used_names = {}
    for literal in literals:
        raw_name = literal['name']
        san_name = sanitize_identifier(raw_name)

        # Deduplicate after sanitization
        if san_name in used_names:
            counter = 2
            base = san_name
            while san_name in used_names:
                san_name = f"{base}_{counter}"
                counter += 1
        used_names[san_name] = raw_name

        doc = clean_doc(literal.get('doc') or '')
        doc = format_inline_comment(doc)

        if doc:
            if san_name != raw_name:
                lines.append(f"{indent}{san_name} = auto()  # {raw_name}: {doc}")
            else:
                lines.append(f"{indent}{san_name} = auto()  # {doc}")
        else:
            if san_name != raw_name:
                lines.append(f"{indent}{san_name} = auto()  # {raw_name}")
            else:
                lines.append(f"{indent}{san_name} = auto()")
    return lines


def write_module(filepath, content):
    """Write content to file and report."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  Generated {filepath}")


def module_header(title, description, reference):
    return (
        f'"""\n'
        f'{title}\n'
        f'\n'
        f'{description}\n'
        f'\n'
        f'Reference: MTConnect Standard v2.6 Normative Model - {reference}\n'
        f'Auto-generated from: model_2.6.xml\n'
        f'"""\n'
        f'\n'
        f'from enum import Enum, auto\n'
    )


# =============================================================================
# CLI
# =============================================================================

parser = argparse.ArgumentParser(
    description='Extract MTConnect enumerations from model XML into separate modules'
)
parser.add_argument('--model-path', type=str,
                    default='.github/agents/data/model_2.6.xml',
                    help='Path to MTConnect model XML file')
parser.add_argument('--output-dir', type=str,
                    default='mtconnect/types',
                    help='Output directory for generated Python modules')
args = parser.parse_args()

repo_root = Path(__file__).parent.parent
xml_file = repo_root / args.model_path
output_dir = repo_root / args.output_dir

if not xml_file.exists():
    print(f"Error: Model file not found at {xml_file}")
    sys.exit(1)

print(f"Parsing {xml_file}...")
tree = ET.parse(xml_file)
root = tree.getroot()

namespaces = {
    'xmi': 'http://www.omg.org/spec/XMI/20131001',
    'uml': 'http://www.omg.org/spec/UML/20131001'
}


# =============================================================================
# Phase 1 - Extract all enumerations from model
# =============================================================================

all_enums = {}  # name -> {name, doc, literals}

for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Enumeration':
        enum_name = elem.get('name')
        if not enum_name:
            continue

        enum_doc = extract_elem_doc(elem)

        literals = []
        for literal in elem.findall('ownedLiteral'):
            literal_name = literal.get('name')
            if not literal_name:
                continue
            literal_doc = extract_elem_doc(literal)
            literals.append({'name': literal_name, 'doc': literal_doc})

        if literals:
            all_enums[enum_name] = {
                'name': enum_name,
                'doc': enum_doc,
                'literals': literals,
            }

print(f"Found {len(all_enums)} enumerations with values")


# =============================================================================
# Phase 2 - Extract concrete Interface classes
# =============================================================================

concrete_interfaces = {}
for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Class':
        class_name = elem.get('name')
        if class_name in ('BarFeederInterface', 'MaterialHandlerInterface',
                          'DoorInterface', 'ChuckInterface'):
            concrete_interfaces[class_name] = clean_doc(extract_elem_doc(elem) or '')


# =============================================================================
# Phase 3 - Generate dedicated modules
# =============================================================================

# Enums routed to their own file (excluded from enums.py)
DEDICATED_ENUMS = set()


# -- event.py -----------------------------------------------------------------

def generate_event_py():
    enum_data = all_enums.get('EventEnum')
    if not enum_data:
        print("  WARNING: EventEnum not found in model")
        return
    DEDICATED_ENUMS.add('EventEnum')

    lines = [module_header(
        'MTConnect EVENT Category Types',
        'All EVENT type DataItems from MTConnect v2.6 normative model.\n'
        'Events represent discrete pieces of information from equipment.',
        'EventEnum',
    )]
    lines.append('')
    lines.append('')
    lines.append('class EventType(Enum):')
    lines.append('    """EVENT types from MTConnect EventEnum"""')
    lines.extend(generate_enum_members(enum_data['literals']))
    lines.append('')

    write_module(output_dir / 'event.py', '\n'.join(lines))


# -- sample.py ----------------------------------------------------------------

def generate_sample_py():
    enum_data = all_enums.get('SampleEnum')
    if not enum_data:
        print("  WARNING: SampleEnum not found in model")
        return
    DEDICATED_ENUMS.add('SampleEnum')

    lines = [module_header(
        'MTConnect SAMPLE Category Types',
        'All SAMPLE type DataItems from MTConnect v2.6 normative model.\n'
        'Samples represent continuously variable or analog data values.',
        'SampleEnum',
    )]
    lines.append('')
    lines.append('')
    lines.append('class SampleType(Enum):')
    lines.append('    """SAMPLE types from MTConnect SampleEnum"""')
    lines.extend(generate_enum_members(enum_data['literals']))
    lines.append('')

    write_module(output_dir / 'sample.py', '\n'.join(lines))


# -- condition.py -------------------------------------------------------------

def generate_condition_py():
    cond_enum = all_enums.get('ConditionEnum')
    state_enum = all_enums.get('ConditionStateEnum')
    qual_enum = all_enums.get('QualifierEnum')

    if not cond_enum:
        print("  WARNING: ConditionEnum not found in model")
        return

    DEDICATED_ENUMS.add('ConditionEnum')
    if state_enum:
        DEDICATED_ENUMS.add('ConditionStateEnum')
    if qual_enum:
        DEDICATED_ENUMS.add('QualifierEnum')

    lines = [module_header(
        'MTConnect CONDITION Category Types',
        'All CONDITION type DataItems and related enumerations from MTConnect v2.6\n'
        'normative model. Conditions represent fault or alarm states with\n'
        'hierarchical severity levels.',
        'ConditionEnum',
    )]
    lines.append('')
    lines.append('')

    # ConditionType
    lines.append('class ConditionType(Enum):')
    lines.append('    """CONDITION types from MTConnect ConditionEnum"""')
    lines.extend(generate_enum_members(cond_enum['literals']))
    lines.append('')
    lines.append('')

    # ConditionLevel (from ConditionStateEnum, renamed for clarity)
    if state_enum:
        lines.append('class ConditionLevel(Enum):')
        lines.append('    """MTConnect condition severity levels in hierarchical order"""')
        lines.extend(generate_enum_members(state_enum['literals']))
        # UNAVAILABLE is part of the protocol but not in XML model
        lines.append('    UNAVAILABLE = auto()  # Condition status cannot be determined')
        lines.append('')
        lines.append('')

    # ConditionQualifier (from QualifierEnum)
    if qual_enum:
        lines.append('class ConditionQualifier(Enum):')
        lines.append('    """MTConnect condition qualifiers for additional context"""')
        lines.extend(generate_enum_members(qual_enum['literals']))
        lines.append('')

    write_module(output_dir / 'condition.py', '\n'.join(lines))


# -- subtype.py ---------------------------------------------------------------

def generate_subtype_py():
    enum_data = all_enums.get('DataItemSubTypeEnum')
    if not enum_data:
        print("  WARNING: DataItemSubTypeEnum not found in model")
        return
    DEDICATED_ENUMS.add('DataItemSubTypeEnum')

    lines = [module_header(
        'MTConnect DataItem SubTypes',
        'All DataItem subType values from MTConnect v2.6 normative model.\n'
        'SubTypes qualify the specific aspect of a DataItem type being measured.',
        'DataItemSubTypeEnum',
    )]
    lines.append('')
    lines.append('')
    lines.append('class DataItemSubType(Enum):')
    lines.append('    """DataItem subType values from MTConnect DataItemSubTypeEnum"""')
    lines.extend(generate_enum_members(enum_data['literals']))
    lines.append('')

    write_module(output_dir / 'subtype.py', '\n'.join(lines))


# -- interface_types.py -------------------------------------------------------

def generate_interface_types_py():
    event_enum = all_enums.get('InterfaceEventEnum')
    state_enum = all_enums.get('InterfaceStateEnum')

    if event_enum:
        DEDICATED_ENUMS.add('InterfaceEventEnum')
    if state_enum:
        DEDICATED_ENUMS.add('InterfaceStateEnum')

    lines = [module_header(
        'MTConnect Interface Interaction Model Types',
        'Interface types for device-to-device coordination (MTConnect Part 5.0).\n'
        'Interfaces use a request/response pattern for coordinating actions\n'
        'between equipment.',
        'Interface Interaction Model',
    )]
    lines.append('')
    lines.append('')

    # InterfaceType from concrete classes
    interface_type_map = {
        'BarFeederInterface': ('BAR_FEEDER', 'Coordinates bar feeder operations pushing stock into equipment'),
        'ChuckInterface': ('CHUCK', 'Coordinates chuck operations for workpiece holding'),
        'DoorInterface': ('DOOR', 'Coordinates door operations between equipment'),
        'MaterialHandlerInterface': ('MATERIAL_HANDLER', 'Coordinates material/tooling loading, unloading, inspection'),
    }
    lines.append('class InterfaceType(Enum):')
    lines.append('    """Concrete Interface types for device-to-device coordination"""')
    for class_name in sorted(interface_type_map):
        enum_name, doc = interface_type_map[class_name]
        lines.append(f"    {enum_name} = auto()  # {doc}")
    lines.append('')
    lines.append('')

    # InterfaceEvent
    if event_enum:
        lines.append('class InterfaceEvent(Enum):')
        lines.append('    """Interface event types from InterfaceEventEnum"""')
        lines.extend(generate_enum_members(
            sorted(event_enum['literals'], key=lambda x: x['name'])
        ))
        lines.append('')
        lines.append('')

    # InterfaceState
    if state_enum:
        lines.append('class InterfaceState(Enum):')
        lines.append('    """Interface operational state values"""')
        lines.extend(generate_enum_members(
            sorted(state_enum['literals'], key=lambda x: x['name'])
        ))
        lines.append('')
        lines.append('')

    # InterfaceRequestResponseState (state machine - not a single enum in XML)
    lines.append('class InterfaceRequestResponseState(Enum):')
    lines.append('    """')
    lines.append('    State machine values for Interface request/response pattern.')
    lines.append('    Flow: NOT_READY -> READY -> ACTIVE -> COMPLETE (or FAIL)')
    lines.append('    """')
    lines.append('    NOT_READY = auto()  # Not prepared to perform service')
    lines.append('    READY = auto()  # Ready to request or perform service')
    lines.append('    ACTIVE = auto()  # Currently performing action')
    lines.append('    COMPLETE = auto()  # Action finished successfully')
    lines.append('    FAIL = auto()  # Failure occurred during action')
    lines.append('')

    write_module(output_dir / 'interface_types.py', '\n'.join(lines))


# =============================================================================
# Phase 4 - Generate enums.py with everything else + re-exports
# =============================================================================

def generate_enums_py():
    # Collect remaining enums (not in dedicated modules)
    remaining = {
        name: data for name, data in all_enums.items()
        if name not in DEDICATED_ENUMS
    }

    print(f"  Remaining enums for enums.py: {len(remaining)}")

    # Group by heuristic
    groups = defaultdict(list)
    for enum_data in remaining.values():
        name = enum_data['name']
        if name in ('CategoryEnum', 'RepresentationEnum', 'DataItemTypeEnum'):
            groups['Core Enumerations'].append(enum_data)
        elif 'State' in name:
            groups['State Enumerations'].append(enum_data)
        elif 'Mode' in name:
            groups['Mode Enumerations'].append(enum_data)
        elif 'Type' in name:
            groups['Type Enumerations'].append(enum_data)
        else:
            groups['Other Enumerations'].append(enum_data)

    lines = [
        '"""',
        'MTConnect Enumeration Types',
        '',
        'Additional enumeration types extracted from the MTConnect normative model',
        'version 2.6. These enums represent standardized values for units, states,',
        'representations, and other categorical values used in MTConnect.',
        '',
        'Reference: MTConnect Standard v2.6 Normative Model',
        'Auto-generated from: model_2.6.xml',
        '"""',
        '',
        'from enum import Enum, auto',
        '',
        '# =============================================================================',
        '# Re-exports from canonical modules (backward compatibility)',
        '# =============================================================================',
        '# These types have dedicated modules. Re-exported here so existing imports',
        "# like 'from mtconnect.types.enums import EventType' continue to work.",
        'from mtconnect.types.event import EventType  # noqa: F401',
        'from mtconnect.types.sample import SampleType  # noqa: F401',
        'from mtconnect.types.condition import ConditionType  # noqa: F401',
        'from mtconnect.types.subtype import DataItemSubType  # noqa: F401',
        'from mtconnect.types.interface_types import (  # noqa: F401',
        '    InterfaceEvent as InterfaceEventEnum,',
        '    InterfaceState as InterfaceStateEnum,',
        ')',
        '',
    ]

    group_order = [
        'Core Enumerations',
        'State Enumerations',
        'Mode Enumerations',
        'Type Enumerations',
        'Other Enumerations',
    ]

    for group_name in group_order:
        if group_name not in groups:
            continue

        lines.append('')
        lines.append('#' * 80)
        lines.append(f'# {group_name}')
        lines.append('#' * 80)
        lines.append('')

        for enum_data in sorted(groups[group_name], key=lambda x: x['name']):
            class_name = enum_data['name']

            lines.append(f"class {class_name}(Enum):")

            if enum_data['doc']:
                doc = clean_doc(enum_data['doc'])
                lines.append('    """')
                lines.append(f'    {doc}')
                lines.append('    """')
            else:
                lines.append(f'    """{class_name} values from MTConnect model"""')

            lines.append('')
            lines.extend(generate_enum_members(enum_data['literals']))
            lines.append('')
            lines.append('')

    write_module(output_dir / 'enums.py', '\n'.join(lines))


# =============================================================================
# Main - generate all files
# =============================================================================

print(f"\nGenerating modules in {output_dir}/\n")

generate_event_py()
generate_sample_py()
generate_condition_py()
generate_subtype_py()
generate_interface_types_py()
generate_enums_py()

print(f"\nDone. Generated 6 modules from {len(all_enums)} enumerations.")
print(f"  Dedicated modules: {len(DEDICATED_ENUMS)} enums")
print(f"  enums.py: {len(all_enums) - len(DEDICATED_ENUMS)} enums")
