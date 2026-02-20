#!/usr/bin/env python3
"""
Extract all enumeration types from the MTConnect normative model XML
and generate a comprehensive Python enum module.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict

# Parse the XML file
xml_file = '/home/pi/machine-interface/.github/agents/data/model_2.6.xml'
print(f"Parsing {xml_file}...")
tree = ET.parse(xml_file)
root = tree.getroot()

# Define XML namespaces
namespaces = {
    'xmi': 'http://www.omg.org/spec/XMI/20131001',
    'uml': 'http://www.omg.org/spec/UML/20131001'
}

# Find all enumerations
enumerations = []

for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Enumeration':
        enum_name = elem.get('name')
        if not enum_name:
            continue
            
        # Extract ownedComment for the enumeration itself
        enum_doc = None
        for comment in elem.findall('uml:ownedComment', namespaces):
            body = comment.get('body')
            if body:
                enum_doc = body
                break
        
        # Extract all literals
        literals = []
        for literal in elem.findall('uml:ownedLiteral', namespaces):
            literal_name = literal.get('name')
            if not literal_name:
                continue
                
            # Extract documentation for this literal
            literal_doc = None
            for comment in literal.findall('uml:ownedComment', namespaces):
                body = comment.get('body')
                if body:
                    literal_doc = body
                    break
            
            literals.append({
                'name': literal_name,
                'doc': literal_doc
            })
        
        if literals:  # Only add enumerations that have literals
            enumerations.append({
                'name': enum_name,
                'doc': enum_doc,
                'literals': literals
            })

print(f"Found {len(enumerations)} enumerations with values")

# Generate Python code
output_lines = [
    '"""',
    'MTConnect Enumeration Types',
    '=' * 80,
    '',
    'This module contains all enumeration types extracted from the MTConnect',
    'normative model version 2.6. These enums represent the standardized values',
    'used throughout the MTConnect protocol.',
    '',
    'Auto-generated from: model_2.6.xml',
    '"""',
    '',
    'from enum import Enum',
    '',
    ''
]

# Group related enums (simple heuristic based on name patterns)
groups = defaultdict(list)
for enum_data in enumerations:
    name = enum_data['name']
    if 'State' in name:
        groups['State Enumerations'].append(enum_data)
    elif 'Type' in name:
        groups['Type Enumerations'].append(enum_data)
    elif 'Mode' in name:
        groups['Mode Enumerations'].append(enum_data)
    elif name in ['CategoryEnum', 'RepresentationEnum', 'DataItemTypeEnum']:
        groups['Core Enumerations'].append(enum_data)
    elif name.endswith('Enum') and ('Sample' in name or 'Event' in name or 'Condition' in name):
        groups['Observation Value Enumerations'].append(enum_data)
    else:
        groups['Other Enumerations'].append(enum_data)

# Sort groups for consistent output
group_order = [
    'Core Enumerations',
    'Observation Value Enumerations',
    'State Enumerations',
    'Mode Enumerations',
    'Type Enumerations',
    'Other Enumerations'
]

for group_name in group_order:
    if group_name not in groups:
        continue
        
    output_lines.append('')
    output_lines.append('#' * 80)
    output_lines.append(f'# {group_name}')
    output_lines.append('#' * 80)
    output_lines.append('')
    
    for enum_data in sorted(groups[group_name], key=lambda x: x['name']):
        # Class definition
        output_lines.append(f"class {enum_data['name']}(Enum):")
        
        # Class docstring
        if enum_data['doc']:
            # Clean up the documentation
            doc = enum_data['doc'].replace('&#10;', '\n    ')
            doc = doc.replace('{{term(', '').replace('{{termplural(', '')
            doc = doc.replace('{{property(', '').replace('{{block(', '')
            doc = doc.replace('{{package(', '').replace('{{url(', '')
            doc = doc.replace(')}}', '').replace('}}', '')
            output_lines.append('    """')
            output_lines.append(f'    {doc}')
            output_lines.append('    """')
        else:
            output_lines.append(f'    """{enum_data["name"]} values from MTConnect model."""')
        
        output_lines.append('')
        
        # Enum values
        for i, literal in enumerate(enum_data['literals'], 1):
            literal_name = literal['name']
            output_lines.append(f"    {literal_name} = '{literal_name}'")
            
            # Add literal documentation as a comment
            if literal['doc']:
                doc = literal['doc'].split('\n')[0]  # Just first line
                doc = doc.replace('{{term(', '').replace('{{termplural(', '')
                doc = doc.replace('{{property(', '').replace('{{block(', '')
                doc = doc.replace('{{package(', '').replace('{{url(', '')
                doc = doc.replace(')}}', '').replace('}}', '')
                if len(doc) > 200:
                    doc = doc[:197] + '...'
                output_lines.append(f"    # {doc}")
        
        output_lines.append('')
        output_lines.append('')

# Write to file
output_file = '/home/pi/machine-interface/src/common/mtconnect_enums.py'
with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

print(f"\nGenerated {output_file}")
print(f"\nTotal enumerations extracted: {len(enumerations)}")
print("\nFirst 10 enum names:")
for i, enum_data in enumerate(enumerations[:10], 1):
    print(f"  {i}. {enum_data['name']}")
