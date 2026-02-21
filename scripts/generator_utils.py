#!/usr/bin/env python3
"""
Shared utilities for MTConnect model generators.

Provides common functions for parsing XMI, resolving types, extracting
cardinality, and formatting Python code.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple, Dict

# XMI/UML Namespaces
NS = {
    'xmi': 'http://www.omg.org/spec/XMI/20131001',
    'uml': 'http://www.omg.org/spec/UML/20131001'
}

# Primitive type XMI ID to Python type mapping
PRIMITIVE_TYPE_MAP = {
    '_19_0_3_91b028d_1579272245466_691733_672': 'ID',  # ID DataType
    '_19_0_3_91b028d_1579272360416_763325_681': 'str',  # string
    '_19_0_3_91b028d_1579272233011_597138_670': 'datetime',  # datetime
    '_19_0_3_91b028d_1579272506322_914606_702': 'float',  # float
    '_19_0_3_91b028d_1579278876899_683310_3821': 'bool',  # boolean
    '_19_0_3_91b028d_1579272271512_537408_674': 'int',  # integer
    '_19_0_3_91b028d_1579272245467_819074_673': 'UUID',  # UUID
}


def parse_xmi(file_path: str) -> ET.Element:
    """
    Parse XMI file and return root element.
    
    Args:
        file_path: Path to model_2.6.xml
        
    Returns:
        Root element of parsed XML tree
    """
    tree = ET.parse(file_path)
    return tree.getroot()


def find_package_by_id(root: ET.Element, package_id: str) -> Optional[ET.Element]:
    """
    Find package element by XMI ID.
    
    Args:
        root: Root element from parse_xmi()
        package_id: XMI ID of package to find
        
    Returns:
        Package element or None if not found
    """
    # Try with namespace
    elem = root.find(f".//*[@{{http://www.omg.org/spec/XMI/20131001}}id='{package_id}']")
    if elem is not None:
        return elem
    
    # Try without namespace (fallback)
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}id') == package_id:
            return elem
    
    return None


def find_element_by_id(root: ET.Element, xmi_id: str) -> Optional[ET.Element]:
    """
    Find any element by XMI ID.
    
    Args:
        root: Root element
        xmi_id: XMI ID to search for
        
    Returns:
        Element or None
    """
    # Try with namespace
    elem = root.find(f".//*[@{{http://www.omg.org/spec/XMI/20131001}}id='{xmi_id}']")
    if elem is not None:
        return elem
    
    # Try without namespace (fallback)
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}id') == xmi_id:
            return elem
    
    return None


def get_cardinality(attr: ET.Element) -> Tuple[int, str]:
    """
    Extract lowerValue and upperValue from attribute.
    
    Handles both direct children and xmi:Extension-wrapped values (MagicDraw format).
    
    Args:
        attr: ownedAttribute element
        
    Returns:
        Tuple of (lowerValue: int, upperValue: str)
        Default is (1, '1') if not specified
    """
    # Try direct children first
    lower_elem = attr.find('.//lowerValue')
    upper_elem = attr.find('.//upperValue')
    
    # Try with any namespace
    if lower_elem is None:
        for elem in attr.iter():
            if elem.tag.endswith('lowerValue'):
                lower_elem = elem
                break
    
    if upper_elem is None:
        for elem in attr.iter():
            if elem.tag.endswith('upperValue'):
                upper_elem = elem
                break
    
    # Parse values
    lower = 1  # Default
    upper = '1'  # Default
    
    if lower_elem is not None:
        lower_val = lower_elem.get('value')
        if lower_val is not None:
            lower = int(lower_val)
        else:
            # Missing value attribute means 0 in UML
            lower = 0
    
    if upper_elem is not None:
        upper_val = upper_elem.get('value')
        if upper_val is not None:
            upper = upper_val
        else:
            # Missing value attribute means 0 in UML
            upper = '0'
    
    return lower, upper


def build_type_map(root: ET.Element) -> Dict[str, str]:
    """
    Build XMI ID to type name mapping.
    
    Pre-builds a lookup dictionary for fast type resolution.
    
    Args:
        root: Root element
        
    Returns:
        Dictionary mapping XMI ID to type name
    """
    type_map = PRIMITIVE_TYPE_MAP.copy()
    
    # Find all named elements (classes, enums, datatypes)
    for elem in root.iter():
        xmi_id = elem.get('{http://www.omg.org/spec/XMI/20131001}id')
        name = elem.get('name')
        xmi_type = elem.get('{http://www.omg.org/spec/XMI/20131001}type')
        
        if xmi_id and name and xmi_type in [
            'uml:Class', 'uml:Enumeration', 'uml:DataType', 'uml:PrimitiveType'
        ]:
            type_map[xmi_id] = name
    
    return type_map


def resolve_type_name(root: ET.Element, type_id: str, type_map: Optional[Dict[str, str]] = None) -> str:
    """
    Resolve XMI ID to type name.
    
    Args:
        root: Root element
        type_id: XMI ID of type to resolve
        type_map: Pre-built type map (optional, will build if not provided)
        
    Returns:
        Type name (e.g., 'Controller', 'DoorState', 'str')
    """
    # Check pre-built map first
    if type_map and type_id in type_map:
        name = type_map[type_id]
    elif type_id in PRIMITIVE_TYPE_MAP:
        # Check primitive map
        name = PRIMITIVE_TYPE_MAP[type_id]
    else:
        # Find element in XML
        elem = find_element_by_id(root, type_id)
        if elem is None:
            return 'UnknownType'
        name = elem.get('name', 'UnknownType')
    
    # Map common XMI type names to Python types
    type_name_map = {
        'integer': 'int',
        'string': 'str',
        'double': 'float',
        'boolean': 'bool',
        'float3d': 'List[float]',  # 3D vector
        'xslang': 'str',  # XML schema language type
        'NativeUnitEnum': 'UnitEnum',  # Use UnitEnum for native units
        'DataItemSubTypeEnum': 'DataItemSubType',  # Correct import name
    }
    
    return type_name_map.get(name, name)


def extract_docstring(comment_elem: Optional[ET.Element]) -> str:
    """
    Extract and clean ownedComment body for docstring.
    
    Removes MTConnect template syntax like {{block()}}, {{term()}}, etc.
    
    Args:
        comment_elem: ownedComment element or None
        
    Returns:
        Cleaned docstring text
    """
    if comment_elem is None:
        return ""
    
    body = comment_elem.get('body', '')
    
    # Clean MTConnect template syntax
    body = re.sub(r'\{\{block\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{term\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{termplural\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{property\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{sect\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{cite\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{def\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{package\((.*?)\)\}\}', r'\1', body)
    body = re.sub(r'\{\{lst\((.*?)\)\}\}', r'\1', body)
    
    # Clean up whitespace
    body = ' '.join(body.split())
    
    return body.strip()


def strip_relationship_prefix(name: str) -> str:
    """
    Strip relationship prefixes from attribute names.
    
    MTConnect UML uses prefixes like 'has*' and 'observes*' for relationships.
    Strip these for Python field names.
    
    Args:
        name: Attribute name from XMI (e.g., 'hasPath', 'observesDoorState')
        
    Returns:
        Name without prefix (e.g., 'Path', 'DoorState')
    """
    # Strip common relationship prefixes
    for prefix in ['observes', 'has']:
        if name.startswith(prefix):
            remainder = name[len(prefix):]
            if remainder and remainder[0].isupper():
                return remainder
    
    return name


def to_snake_case(name: str) -> str:
    """
    Convert PascalCase/camelCase to snake_case.
    
    Args:
        name: CamelCase or PascalCase string
        
    Returns:
        snake_case string
    """
    # Replace spaces and special characters with underscores first
    name = name.replace(' ', '_')
    name = name.replace(':', '_')
    name = name.replace('-', '_')
    
    # Insert underscore before capital letters (except first)
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def attribute_to_field_name(attr_name: str) -> str:
    """
    Convert XMI attribute name to Python field name.
    
    Strips relationship prefixes and converts to snake_case.
    
    Args:
        attr_name: XMI attribute name (e.g., 'hasPath', 'observesDoorState')
        
    Returns:
        Python field name (e.g., 'path', 'door_state')
    """
    stripped = strip_relationship_prefix(attr_name)
    return to_snake_case(stripped)


def sanitize_class_name(class_name: str) -> str:
    """
    Sanitize XMI class name to valid Python class name.
    
    Removes spaces, special characters, and ensures PascalCase.
    
    Args:
        class_name: XMI class name (e.g., 'Observed Measurement', 'MTConnect Event', 'DoorState')
        
    Returns:
        Valid Python class name (e.g., 'ObservedMeasurement', 'MTConnectEvent', 'DoorState')
    """
    # If the name has no spaces and only valid identifiers, keep it as-is
    if ' ' not in class_name and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', class_name):
        return class_name
    
    # Remove spaces and capitalize each word
    class_name = ''.join(word.capitalize() for word in class_name.split())
    # Remove any remaining invalid characters
    class_name = re.sub(r'[^A-Za-z0-9_]', '', class_name)
    return class_name


def is_optional_single(lower: int, upper: str) -> bool:
    """Check if cardinality is [0..1] (optional single)."""
    return lower == 0 and upper == '1'


def is_required_single(lower: int, upper: str) -> bool:
    """Check if cardinality is [1..1] (required single)."""
    return lower == 1 and upper == '1'


def is_optional_list(lower: int, upper: str) -> bool:
    """Check if cardinality is [0..*] (optional list)."""
    return lower == 0 and upper == '*'


def is_required_list(lower: int, upper: str) -> bool:
    """Check if cardinality is [1..*] (required list)."""
    return lower == 1 and upper == '*'


def format_python_type(type_name: str, lower: int, upper: str, use_forward_ref: bool = False) -> str:
    """
    Format Python type annotation based on cardinality.
    
    Args:
        type_name: Base type name (e.g., 'Controller', 'str')
        lower: Lower bound of cardinality
        upper: Upper bound of cardinality ('1' or '*')
        use_forward_ref: Whether to wrap type in quotes for forward reference
        
    Returns:
        Formatted type annotation (e.g., "Optional[Controller]", "List[str]")
    """
    # Handle forward references
    if use_forward_ref and type_name not in ['str', 'int', 'float', 'bool', 'datetime']:
        type_ref = f"'{type_name}'"
    else:
        type_ref = type_name
    
    # Format based on cardinality
    if is_required_single(lower, upper):
        return type_ref
    elif is_optional_single(lower, upper):
        return f"Optional[{type_ref}]"
    elif is_required_list(lower, upper):
        return f"List[{type_ref}]"
    elif is_optional_list(lower, upper):
        return f"List[{type_ref}]"
    else:
        # Default to optional
        return f"Optional[{type_ref}]"


def format_field_default(lower: int, upper: str) -> str:
    """
    Format field default value based on cardinality.
    
    Args:
        lower: Lower bound
        upper: Upper bound
        
    Returns:
        Default value string (empty for required, "= None", or "= field(default_factory=list)")
    """
    if is_required_single(lower, upper):
        return ""  # Required, no default
    elif is_optional_single(lower, upper):
        return " = None"
    elif upper == '*':
        return " = field(default_factory=list)"
    else:
        return " = None"


def get_parent_class(cls_elem: ET.Element, root: ET.Element, type_map: Dict[str, str]) -> Optional[str]:
    """
    Get parent class name from generalization element.
    
    Args:
        cls_elem: Class element
        root: Root element
        type_map: Type mapping dictionary
        
    Returns:
        Parent class name or None
    """
    gen_elem = cls_elem.find('generalization', NS)
    if gen_elem is None:
        gen_elem = cls_elem.find('.//generalization')
    
    if gen_elem is not None:
        parent_id = gen_elem.get('general')
        if parent_id:
            return resolve_type_name(root, parent_id, type_map)
    
    return None


def is_abstract(cls_elem: ET.Element) -> bool:
    """Check if class is abstract."""
    return cls_elem.get('isAbstract') == 'true'


def is_leaf(cls_elem: ET.Element) -> bool:
    """Check if class is a leaf (cannot be subclassed)."""
    return cls_elem.get('isLeaf') == 'true'


def format_docstring(text: str, indent: int = 4) -> str:
    """
    Format text as Python docstring with proper indentation.
    
    Args:
        text: Docstring text
        indent: Number of spaces for indentation
        
    Returns:
        Formatted docstring including triple quotes
    """
    if not text:
        return ""
    
    indent_str = ' ' * indent
    
    # Simple single-line docstring
    if len(text) < 70 and '\n' not in text:
        return f'{indent_str}"""{text}"""'
    
    # Multi-line docstring
    lines = []
    lines.append(f'{indent_str}"""')
    
    # Wrap long lines at 88 characters (Black default)
    max_width = 88 - indent - 4  # Account for indent and continuation
    words = text.split()
    current_line = []
    current_length = 0
    
    for word in words:
        word_len = len(word) + 1  # +1 for space
        if current_length + word_len > max_width and current_line:
            lines.append(f'{indent_str}{" ".join(current_line)}')
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += word_len
    
    if current_line:
        lines.append(f'{indent_str}{" ".join(current_line)}')
    
    lines.append(f'{indent_str}"""')
    
    return '\n'.join(lines)
