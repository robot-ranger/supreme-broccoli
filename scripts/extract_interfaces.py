#!/usr/bin/env python3
"""
Extract Interface Interaction Model types from MTConnect normative model XML.
Generates interface_types.py with all Interface-related enumerations.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# Resolve paths relative to repository root
repo_root = Path(__file__).parent.parent
xml_file = repo_root / '.github/agents/data/model_2.6.xml'

if not xml_file.exists():
    print(f"Error: Model file not found at {xml_file}")
    sys.exit(1)

print(f"Parsing {xml_file}...")
tree = ET.parse(xml_file)
root = tree.getroot()

# Define XML namespaces
namespaces = {
    'xmi': 'http://www.omg.org/spec/XMI/20131001',
    'uml': 'http://www.omg.org/spec/UML/20131001'
}

def clean_doc(doc: str) -> str:
    """Clean MTConnect model documentation strings"""
    if not doc:
        return doc
    
    # Remove MTConnect markup
    doc = doc.replace('{{term(', '').replace('{{termplural(', '')
    doc = doc.replace('{{property(', '').replace('{{block(', '')
    doc = doc.replace('{{package(', '').replace('{{url(', '')
    doc = doc.replace(')}}', '').replace('}}', '')
    
    # Normalize line breaks
    doc = doc.replace('&#10;', ' ')
    
    return doc.strip()

# Extract InterfaceEventEnum
interface_events = []
interface_states = []
concrete_interfaces = {}

print("Extracting Interface enumerations...")

for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Enumeration':
        enum_name = elem.get('name')
        
        # Extract InterfaceEventEnum (11 event types)
        if enum_name == 'InterfaceEventEnum':
            print(f"  Found {enum_name}")
            for literal in elem.findall('ownedLiteral'):
                literal_name = literal.get('name')
                if literal_name:
                    literal_doc = None
                    for comment in literal.findall('ownedComment'):
                        body = comment.get('body')
                        if body:
                            literal_doc = clean_doc(body).split('\n')[0]
                            break
                    interface_events.append({
                        'name': literal_name,
                        'doc': literal_doc
                    })
        
        # Extract InterfaceStateEnum (ENABLED/DISABLED)
        elif enum_name == 'InterfaceStateEnum':
            print(f"  Found {enum_name}")
            for literal in elem.findall('ownedLiteral'):
                literal_name = literal.get('name')
                if literal_name:
                    literal_doc = None
                    for comment in literal.findall('ownedComment'):
                        body = comment.get('body')
                        if body:
                            literal_doc = clean_doc(body).split('\n')[0]
                            break
                    interface_states.append({
                        'name': literal_name,
                        'doc': literal_doc
                    })
    
    # Extract concrete Interface types
    elif elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Class':
        class_name = elem.get('name')
        if class_name in ['BarFeederInterface', 'MaterialHandlerInterface', 
                          'DoorInterface', 'ChuckInterface']:
            print(f"  Found {class_name}")
            class_doc = None
            for comment in elem.findall('ownedComment'):
                body = comment.get('body')
                if body:
                    class_doc = clean_doc(body)
                    break
            concrete_interfaces[class_name] = class_doc

# Generate interface_types.py
output_lines = [
    '"""',
    'MTConnect Interface Interaction Model Types',
    '',
    'Interface types for device-to-device coordination (MTConnect Part 5.0).',
    'Interfaces use a request/response pattern for coordinating actions between equipment.',
    '',
    'Reference: MTConnect Standard v2.6 Normative Model - Interface Interaction Model',
    'Package: Interface Interaction Model (line ~42336)',
    '"""',
    '',
    'from enum import Enum, auto',
    '',
    ''
]

# InterfaceType enum
output_lines.append('class InterfaceType(Enum):')
output_lines.append('    """Concrete Interface types for device-to-device coordination"""')
interface_type_map = {
    'BarFeederInterface': ('BAR_FEEDER', 'Coordinates bar feeder operations pushing stock into equipment'),
    'MaterialHandlerInterface': ('MATERIAL_HANDLER', 'Coordinates material/tooling loading, unloading, inspection'),
    'ChuckInterface': ('CHUCK', 'Coordinates chuck operations for workpiece holding'),
    'DoorInterface': ('DOOR', 'Coordinates door operations between equipment')
}
for class_name in ['BarFeederInterface', 'ChuckInterface', 'DoorInterface', 'MaterialHandlerInterface']:
    if class_name in interface_type_map:
        enum_name, doc = interface_type_map[class_name]
        output_lines.append(f"    {enum_name} = auto()  # {doc}")
output_lines.append('')
output_lines.append('')

# InterfaceEvent enum
output_lines.append('class InterfaceEvent(Enum):')
output_lines.append('    """Interface event types from InterfaceEventEnum"""')
for event in sorted(interface_events, key=lambda x: x['name']):
    if event['doc']:
        doc = event['doc']
        if len(doc) > 80:
            doc = doc[:77] + '...'
        output_lines.append(f"    {event['name']} = auto()  # {doc}")
    else:
        output_lines.append(f"    {event['name']} = auto()")
output_lines.append('')
output_lines.append('')

# InterfaceState enum
output_lines.append('class InterfaceState(Enum):')
output_lines.append('    """Interface operational state values"""')
for state in sorted(interface_states, key=lambda x: x['name']):
    if state['doc']:
        doc = state['doc']
        if len(doc) > 80:
            doc = doc[:77] + '...'
        output_lines.append(f"    {state['name']} = auto()  # {doc}")
    else:
        output_lines.append(f"    {state['name']} = auto()")
output_lines.append('')
output_lines.append('')

# InterfaceRequestResponseState enum (state machine values)
output_lines.append('class InterfaceRequestResponseState(Enum):')
output_lines.append('    """')
output_lines.append('    State machine values for Interface request/response pattern.')
output_lines.append('    Flow: NOT_READY → READY → ACTIVE → COMPLETE (or FAIL)')
output_lines.append('    """')
output_lines.append('    NOT_READY = auto()  # Not prepared to perform service')
output_lines.append('    READY = auto()  # Ready to request or perform service')
output_lines.append('    ACTIVE = auto()  # Currently performing action')
output_lines.append('    COMPLETE = auto()  # Action finished successfully')
output_lines.append('    FAIL = auto()  # Failure occurred during action')
output_lines.append('')

# Write to file
output_dir = repo_root / 'mtconnect/types'
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'interface_types.py'

with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

print(f"\nGenerated {output_file}")
print(f"  InterfaceType: {len(interface_type_map)} types")
print(f"  InterfaceEvent: {len(interface_events)} events")
print(f"  InterfaceState: {len(interface_states)} states")
print(f"  InterfaceRequestResponseState: 5 states")
