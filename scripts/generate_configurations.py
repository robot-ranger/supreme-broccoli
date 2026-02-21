#!/usr/bin/env python3
"""
Generate mtconnect/models/configurations.py from MTConnect XMI model.

Extracts configuration classes from the Configuration package and generates
Python dataclasses with correct cardinality and nested objects.
"""

import sys
from pathlib import Path
from typing import List, Dict
import xml.etree.ElementTree as ET

# Import shared generator utilities
sys.path.insert(0, str(Path(__file__).parent))

from generator_utils import (
    parse_xmi, build_type_map, get_cardinality, resolve_type_name,
    extract_docstring, attribute_to_field_name, format_python_type,
    format_field_default, get_parent_class, is_required_list, NS
)

# Configuration package XMI ID
CONFIGURATION_PACKAGE_ID = '_19_0_3_91b028d_1579526876433_244855_7626'


def extract_configuration_classes(root: ET.Element) -> List[ET.Element]:
    """
    Extract all configuration class elements from Configuration package.
    
    Args:
        root: Root element from parse_xmi()
        
    Returns:
        List of class elements
    """
    # Find Configuration package
    config_pkg = None
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}id') == CONFIGURATION_PACKAGE_ID:
            config_pkg = elem
            break
    
    if config_pkg is None:
        raise ValueError(f"Configuration package not found: {CONFIGURATION_PACKAGE_ID}")
    
    # Extract all classes in this package
    classes = []
    for child in config_pkg.iter():
        xmi_type = child.get('{http://www.omg.org/spec/XMI/20131001}type')
        if xmi_type == 'uml:Class':
            classes.append(child)
    
    return classes


def generate_configuration_class(
    cls_elem: ET.Element,
    root: ET.Element,
    type_map: Dict[str, str]
) -> str:
    """
    Generate Python dataclass code for a configuration class.
    
    Args:
        cls_elem: Class element from XMI
        root: Root element
        type_map: Type resolution mapping
        
    Returns:
        Generated Python class code
    """
    class_name = cls_elem.get('name')
    if not class_name:
        return ""
    
    # Extract documentation
    doc_elem = cls_elem.find('ownedComment')
    doc_text = extract_docstring(doc_elem) if doc_elem else f"{class_name} configuration."
    
    # Find parent class
    parent = get_parent_class(cls_elem, root, type_map)
    
    # Skip self-references (Configuration inheriting from Configuration)
    if parent == class_name:
        parent = None
    
    parent_str = f"({parent})" if parent else ""
    
    # Extract attributes
    attributes = []
    required_fields = []  # Track [1..1] and [1..*] fields for validation
    seen_fields = set()  # Track field names to avoid duplicates
    
    for attr in cls_elem.findall('ownedAttribute'):
        attr_name = attr.get('name')
        if not attr_name:
            continue
        
        # Get type
        type_id = attr.get('type')
        if not type_id:
            continue
        
        type_name = resolve_type_name(root, type_id, type_map)
        
        # Get cardinality
        lower, upper = get_cardinality(attr)
        
        # Check if this is a relationship (has*)
        is_relationship = attr_name.startswith('has')
        
        # Generate field name (strip 'has' prefix for nested objects)
        if is_relationship:
            field_name = attribute_to_field_name(attr_name)
        else:
            field_name = attribute_to_field_name(attr_name)
        
        # Skip duplicate fields (keep first occurrence)
        if field_name in seen_fields:
            continue
        seen_fields.add(field_name)
        
        # Format type annotation
        python_type = format_python_type(type_name, lower, upper, use_forward_ref=False)
        
        # Format default value
        default = format_field_default(lower, upper)
        
        # Extract field documentation
        field_doc_elem = attr.find('ownedComment')
        field_doc = extract_docstring(field_doc_elem) if field_doc_elem else ""
        
        # Track required fields [1..1] and [1..*]
        if lower >= 1:
            if upper == '1':
                required_fields.append((field_name, attr_name, 'single'))
            else:
                required_fields.append((field_name, attr_name, 'list'))
        
        attributes.append({
            'field_name': field_name,
            'python_type': python_type,
            'default': default,
            'doc': field_doc,
            'lower': lower,
            'upper': upper
        })
    
    # Build class code
    lines = []
    lines.append("")
    lines.append("")
    lines.append("@dataclass")
    lines.append(f"class {class_name}{parent_str}:")
    
    # Docstring
    if doc_text:
        lines.append(f'    """{doc_text}"""')
    else:
        lines.append(f'    """{class_name} configuration."""')
    
    # Attributes - for subclasses, all fields need defaults to avoid dataclass ordering issues
    # Even for base classes, we need to sort: required fields first, then optional
    if attributes:
        # Separate required and optional
        required_attrs = []
        optional_attrs = []
        
        for attr in attributes:
            # If this is a subclass and field is required, force a default and validate in __post_init__
            if parent and not attr['default'] and attr['lower'] >= 1:
                # Add default for dataclass compatibility
                if attr['upper'] == '*':
                    attr['default'] = ' = field(default_factory=list)'
                else:
                    attr['default'] = ' = None'
            
            # Sort into required (no default) or optional (has default)
            if attr['default']:
                optional_attrs.append(attr)
            else:
                required_attrs.append(attr)
        
        # Generate required fields first
        for attr in required_attrs:
            field_line = f"    {attr['field_name']}: {attr['python_type']}{attr['default']}"
            if attr['doc']:
                field_line += f"  # {attr['doc']}"
            lines.append(field_line)
        
        # Then optional fields
        for attr in optional_attrs:
            field_line = f"    {attr['field_name']}: {attr['python_type']}{attr['default']}"
            if attr['doc']:
                field_line += f"  # {attr['doc']}"
            lines.append(field_line)
    else:
        lines.append("    pass")
    
    # Add __post_init__ for type coercion if needed
    if required_fields or any('ID' in a['python_type'] for a in attributes):
        lines.append("")
        lines.append("    def __post_init__(self):")
        
        # Type coercion for ID fields
        for attr in attributes:
            if 'ID' in attr['python_type'] and 'Optional' not in attr['python_type']:
                lines.append(f"        if isinstance(self.{attr['field_name']}, str):")
                lines.append(f"            self.{attr['field_name']} = ID(self.{attr['field_name']})")
        
        # Validation for required fields
        for field_name, xml_name, field_type in required_fields:
            if field_type == 'single':
                lines.append(f"        if self.{field_name} is None:")
                lines.append(f"            raise ValueError('{xml_name} is required [1..1]')")
            else:  # list
                lines.append(f"        if not self.{field_name}:")
                lines.append(f"            raise ValueError('{xml_name} is required and cannot be empty [1..*]')")
    
    return "\n".join(lines)


def generate_configurations_module(model_path: str, output_path: str):
    """
    Generate complete configurations.py module.
    
    Args:
        model_path: Path to model_2.6.xml
        output_path: Path to output configurations.py
    """
    root = parse_xmi(model_path)
    type_map = build_type_map(root)
    
    # Extract configuration classes
    classes = extract_configuration_classes(root)
    
    # Sort classes by dependency (parents first)
    sorted_classes = []
    added_names = set()
    processing = set()  # Track currently processing to detect cycles
    
    def add_class_and_parents(cls_elem):
        """Recursively add class and its parents."""
        name = cls_elem.get('name')
        if not name:
            return
        
        if name in added_names:
            return
        
        if name in processing:
            # Circular dependency detected, just add it
            sorted_classes.append(cls_elem)
            added_names.add(name)
            return
        
        processing.add(name)
        
        # Add parent first
        parent_name = get_parent_class(cls_elem, root, type_map)
        if parent_name and parent_name not in added_names:
            # Find parent class element
            for c in classes:
                if c.get('name') == parent_name:
                    add_class_and_parents(c)
                    break
        
        processing.remove(name)
        sorted_classes.append(cls_elem)
        added_names.add(name)
    
    # Add all classes
    for cls_elem in classes:
        add_class_and_parents(cls_elem)
    
    # Generate code for each class
    class_codes = []
    for cls_elem in sorted_classes:
        code = generate_configuration_class(cls_elem, root, type_map)
        if code:
            class_codes.append(code)
    
    # Build module
    module_lines = [
        '"""',
        'MTConnect Configuration Models',
        '',
        'Configuration information for components including coordinate systems,',
        'specifications, sensor configuration, motion parameters, and solid models.',
        '',
        'Reference: MTConnect Standard v2.6 - Configuration Package',
        'Auto-generated from: model_2.6.xml',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass, field',
        'from typing import Optional, List, Union, TYPE_CHECKING',
        '',
        'from mtconnect.types.primitives import ID, MTCFloat',
        'from mtconnect.types.enums import (',
        '    CoordinateSystemTypeEnum, MotionActuationTypeEnum, MotionTypeEnum,',
        '    OriginatorEnum, UnitEnum, RelationshipTypeEnum, MediaTypeEnum',
        ')',
        'from mtconnect.types.subtype import DataItemSubType',
        'from mtconnect.types.sample import SampleType',
        'from mtconnect.types.event import EventType',
        'from mtconnect.types.condition import ConditionType',
        '',
        'if TYPE_CHECKING:',
        '    from mtconnect.models.components import Description',
        '',
    ]
    
    module_lines.extend(class_codes)
    module_lines.append("")  # Final newline
    
    # Write to file
    output_file = Path(output_path)
    output_file.write_text("\n".join(module_lines))
    print(f"Generated: {output_path}")
    print(f"  - {len(sorted_classes)} configuration classes")


if __name__ == '__main__':
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    model_path = project_root / '.github' / 'agents' / 'data' / 'model_2.6.xml'
    output_path = project_root / 'mtconnect' / 'models' / 'configurations.py'
    
    if not model_path.exists():
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)
    
    generate_configurations_module(str(model_path), str(output_path))
