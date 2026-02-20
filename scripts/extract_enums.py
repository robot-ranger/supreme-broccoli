#!/usr/bin/env python3
"""
Extract all enumeration types from the MTConnect normative model XML
and generate a comprehensive Python enum module.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import argparse
from pathlib import Path
import sys

# Set up argument parser
parser = argparse.ArgumentParser(description='Extract MTConnect enumerations from model XML')
parser.add_argument('--model-path', type=str, 
                    default='.github/agents/data/model_2.6.xml',
                    help='Path to MTConnect model XML file')
parser.add_argument('--output-dir', type=str,
                    default='mtconnect/types',
                    help='Output directory for generated Python modules')
parser.add_argument('--enum-names', type=str, nargs='*',
                    help='Optional: specific enum names to extract (extracts all if not specified)')
parser.add_argument('--output-file', type=str,
                    help='Optional: single output file name (default: enums.py)')

args = parser.parse_args()

# Resolve paths relative to repository root
repo_root = Path(__file__).parent.parent
xml_file = repo_root / args.model_path

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

# Find all enumerations
enumerations = []

for elem in root.iter():
    if elem.get('{' + namespaces['xmi'] + '}type') == 'uml:Enumeration':
        enum_name = elem.get('name')
        if not enum_name:
            continue
            
        # Extract ownedComment for the enumeration itself
        enum_doc = None
        for comment in elem.findall('ownedComment'):
            body = comment.get('body')
            if body:
                enum_doc = body
                break
        
        # Extract all literals
        literals = []
        for literal in elem.findall('ownedLiteral'):  
            literal_name = literal.get('name')
            if not literal_name:
                continue
                
            # Extract documentation for this literal
            literal_doc = None
            for comment in literal.findall('ownedComment'):
                body = comment.get('body')
                if body:
                    literal_doc = body
                    break
            
            literals.append({
                'name': literal_name,
                'doc': literal_doc
            })
        
        if literals:  # Only add enumerations that have literals
            # Filter by specific enum names if provided
            if args.enum_names and enum_name not in args.enum_names:
                continue
                
            enumerations.append({
                'name': enum_name,
                'doc': enum_doc,
                'literals': literals
            })

if args.enum_names and not enumerations:
    print(f"Warning: No enumerations found matching: {', '.join(args.enum_names)}")
    sys.exit(1)

print(f"Found {len(enumerations)} enumerations with values")

# Generate Python code
output_lines = [
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
        
        # Enum values with inline comments (no blank lines between members)
        for i, literal in enumerate(enum_data['literals']):
            literal_name = literal['name']
            
            # Add literal documentation as inline comment
            if literal['doc']:
                doc = literal['doc'].split('\n')[0]  # Just first line
                doc = doc.replace('{{term(', '').replace('{{termplural(', '')
                doc = doc.replace('{{property(', '').replace('{{block(', '')
                doc = doc.replace('{{package(', '').replace('{{url(', '')
                doc = doc.replace(')}}', '').replace('}}', '')
                doc = doc.replace('&#10;', ' ')
                if len(doc) > 80:
                    doc = doc[:77] + '...'
                output_lines.append(f"    {literal_name} = auto()  # {doc}")
            else:
                output_lines.append(f"    {literal_name} = auto()")
        
        output_lines.append('')
        output_lines.append('')

# Determine output path
output_dir = repo_root / args.output_dir
output_dir.mkdir(parents=True, exist_ok=True)

if args.output_file:
    output_file = output_dir / args.output_file
else:
    output_file = output_dir / 'enums.py'

# Write to file
with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

print(f"\nGenerated {output_file}")
print(f"Total enumerations extracted: {len(enumerations)}")

if len(enumerations) <= 20:
    print("\nExtracted enum names:")
    for i, enum_data in enumerate(enumerations, 1):
        print(f"  {i}. {enum_data['name']}")
else:
    print(f"\nFirst 20 of {len(enumerations)} enum names:")
    for i, enum_data in enumerate(enumerations[:20], 1):
        print(f"  {i}. {enum_data['name']}")
