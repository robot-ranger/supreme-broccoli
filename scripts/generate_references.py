#!/usr/bin/env python3
"""
Generate mtconnect/models/references.py from MTConnect XMI model.

Extracts reference classes from the References package and generates
Python dataclasses with correct inheritance and typing.
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
    format_field_default, get_parent_class, NS
)

# References package XMI ID
REFERENCES_PACKAGE_ID = 'EAPK_F54CCA63_E73C_468b_B64E_F97DEE70FFC6'


def extract_reference_classes(root: ET.Element) -> List[ET.Element]:
    """
    Extract all reference class elements from References package.
    
    Args:
        root: Root element from parse_xmi()
        
    Returns:
        List of class elements
    """
    # Find References package
    ref_pkg = None
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}id') == REFERENCES_PACKAGE_ID:
            ref_pkg = elem
            break
    
    if ref_pkg is None:
        raise ValueError(f"References package not found: {REFERENCES_PACKAGE_ID}")
    
    # Extract all classes in this package
    classes = []
    for child in ref_pkg.iter():
        xmi_type = child.get('{http://www.omg.org/spec/XMI/20131001}type')
        if xmi_type == 'uml:Class':
            classes.append(child)
    
    return classes


def generate_reference_class(
    cls_elem: ET.Element,
    root: ET.Element,
    type_map: Dict[str, str]
) -> str:
    """
    Generate Python dataclass code for a reference class.
    
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
    doc_text = extract_docstring(doc_elem) if doc_elem else f"{class_name} reference."
    
    # Find parent class
    parent = get_parent_class(cls_elem, root, type_map)
    
    # Skip self-references
    if parent == class_name:
        parent = None
    
    parent_str = f"({parent})" if parent else ""
    
    # Check if abstract
    is_abstract = cls_elem.get('isAbstract') == 'true'
    
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
        
        # Get cardinality
        lower, upper = get_cardinality(attr)
        
        # Skip [0..0] cardinality (excluded attributes)
        if lower == 0 and upper == '0':
            continue
        
        # Resolve type name
        type_name = resolve_type_name(root, type_id, type_map)
        
        # Convert attribute name to field name
        field_name = attribute_to_field_name(attr_name)
        
        # Avoid duplicates (in case of association ends)
        if field_name in seen_fields:
            continue
        seen_fields.add(field_name)
        
        # Extract documentation for this attribute
        attr_doc_elem = attr.find('ownedComment')
        attr_doc = extract_docstring(attr_doc_elem) if attr_doc_elem else ""
        
        # Format type and default
        python_type = format_python_type(type_name, lower, upper)
        field_default = format_field_default(lower, upper)
        
        # Track required fields for validation
        if lower >= 1:
            required_fields.append(field_name)
        
        attributes.append({
            'name': field_name,
            'type': python_type,
            'default': field_default,
            'doc': attr_doc,
            'required': lower >= 1
        })
    
    # Sort attributes: required fields first (no default), then optional fields (with defaults)
    # This is required by Python dataclasses
    attributes.sort(key=lambda a: (not a['required'], a['name']))
    
    # Generate class code
    lines = []
    lines.append("")
    lines.append(f"@dataclass")
    lines.append(f"class {class_name}{parent_str}:")
    
    # Docstring
    if doc_text:
        lines.append(f'    """{doc_text}"""')
        lines.append("")
    
    # If no attributes and not abstract, add pass
    if not attributes and not required_fields:
        lines.append("    pass")
        return '\n'.join(lines)
    
    # Generate fields
    for attr in attributes:
        if attr['doc']:
            lines.append(f"    # {attr['doc']}")
        lines.append(f"    {attr['name']}: {attr['type']}{attr['default']}")
    
    # Generate __post_init__ for validation if there are required fields
    if required_fields and not is_abstract:
        lines.append("")
        lines.append("    def __post_init__(self):")
        lines.append('        """Validate required fields."""')
        for field in required_fields:
            lines.append(f"        if self.{field} is None:")
            lines.append(f"            raise ValueError(f'{class_name}.{field} is required')")
    
    return '\n'.join(lines)


def generate_references_module(xmi_path: str, output_path: str) -> None:
    """
    Generate references.py module from XMI model.
    
    Args:
        xmi_path: Path to model_2.6.xml
        output_path: Path to output references.py
    """
    print(f"Parsing XMI from: {xmi_path}")
    root = parse_xmi(xmi_path)
    
    print("Building type map...")
    type_map = build_type_map(root)
    
    print("Extracting reference classes...")
    classes = extract_reference_classes(root)
    print(f"Found {len(classes)} reference classes")
    
    # Sort classes: parent first (Reference), then children
    # Reference is abstract, ComponentRef and DataItemRef inherit from it
    sorted_classes = []
    abstract_classes = []
    concrete_classes = []
    
    for cls_elem in classes:
        is_abstract = cls_elem.get('isAbstract') == 'true'
        if is_abstract:
            abstract_classes.append(cls_elem)
        else:
            concrete_classes.append(cls_elem)
    
    sorted_classes = abstract_classes + concrete_classes
    
    # Generate header
    lines = []
    lines.append('"""')
    lines.append('MTConnect References Model.')
    lines.append('')
    lines.append('Auto-generated from model_2.6.xml - DO NOT EDIT.')
    lines.append('"""')
    lines.append('')
    lines.append('from __future__ import annotations')
    lines.append('')
    lines.append('from dataclasses import dataclass')
    lines.append('from typing import TYPE_CHECKING, Optional')
    lines.append('')
    lines.append('from mtconnect.types.primitives import ID')
    lines.append('')
    lines.append('if TYPE_CHECKING:')
    lines.append('    from mtconnect.models.components import Component')
    lines.append('    from mtconnect.models.data_items import DataItem')
    lines.append('')
    lines.append('')
    lines.append('__all__ = [')
    
    # Collect class names for __all__
    class_names = []
    for cls_elem in sorted_classes:
        name = cls_elem.get('name')
        if name:
            class_names.append(name)
    
    for name in sorted(class_names):
        lines.append(f"    '{name}',")
    lines.append(']')
    
    # Generate classes
    for cls_elem in sorted_classes:
        class_code = generate_reference_class(cls_elem, root, type_map)
        if class_code:
            lines.append(class_code)
    
    # Write output
    output = '\n'.join(lines) + '\n'
    Path(output_path).write_text(output)
    print(f"Generated {output_path}")
    print(f"  Total classes: {len(class_names)}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate MTConnect references model')
    parser.add_argument(
        '--model-path',
        default='.github/agents/data/model_2.6.xml',
        help='Path to model_2.6.xml'
    )
    parser.add_argument(
        '--output-path',
        default='mtconnect/models/references.py',
        help='Path to output file'
    )
    
    args = parser.parse_args()
    
    generate_references_module(args.model_path, args.output_path)
    print("✓ Reference model generation complete")


if __name__ == '__main__':
    main()
