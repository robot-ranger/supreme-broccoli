#!/usr/bin/env python3
"""
Generate MTConnect component hierarchy from model XML.

Parses model_2.6.xml and generates mtconnect/models/components.py with all
component types in the correct inheritance order, including relationship fields.

Usage:
  python scripts/generate_components.py
  python scripts/generate_components.py --model-path .github/agents/data/model_2.6.xml
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Import shared generator utilities
from generator_utils import (
    get_cardinality, resolve_type_name, attribute_to_field_name,
    format_python_type, format_field_default, extract_docstring,
    is_required_list, build_type_map
)

# =============================================================================
# Constants
# =============================================================================

XMI_NS = "http://www.omg.org/spec/XMI/20131001"
COMPONENT_XMI_ID = "_19_0_3_45f01b9_1581734537697_742151_1119"

# Types to exclude entirely
DEPRECATED_EXCLUDE = {"Power", "Thermostat", "Vibration"}
SKIP_NAMES = {
    "MTConnect Device with Operational States",
    "MTConnect Device with Power Source Config",
}

# Organizer types not present in the XML model but part of the MTConnect
# document structure.  Each organizer gets a typed List field for its children.
ORGANIZER_TYPES = {
    "Axes": {
        "parent": "Component",
        "child_type": "Axis",
        "field_name": "axes",
        "doc": "Organizer that groups Axis components.",
    },
    "Systems": {
        "parent": "Component",
        "child_type": "System",
        "field_name": "systems",
        "doc": "Organizer that groups System components.",
    },
    "Auxiliaries": {
        "parent": "Component",
        "child_type": "Auxiliary",
        "field_name": "auxiliaries",
        "doc": "Organizer that groups Auxiliary components.",
    },
    "Resources": {
        "parent": "Component",
        "child_type": "Resource",
        "field_name": "resources",
        "doc": "Organizer that groups Resource components.",
    },
    "Controllers": {
        "parent": "Component",
        "child_type": "Controller",
        "field_name": "controllers",
        "doc": "Organizer that groups Controller components.",
    },
    "Materials": {
        "parent": "Component",
        "child_type": "Material",
        "field_name": "materials",
        "doc": "Organizer that groups Material components.",
    },
    "Interfaces": {
        "parent": "Component",
        "child_type": "Interface",
        "field_name": "interfaces",
        "doc": "Organizer that groups Interface components.",
    },
    "Adapters": {
        "parent": "Component",
        "child_type": "Adapter",
        "field_name": "adapters",
        "doc": "Organizer that groups Adapter components.",
    },
    "Structures": {
        "parent": "Component",
        "child_type": "Structure",
        "field_name": "structures",
        "doc": "Organizer that groups Structure components.",
    },
    "Processes": {
        "parent": "Component",
        "child_type": "Process",
        "field_name": "processes",
        "doc": "Organizer that groups Process components.",
    },
    "Parts": {
        "parent": "Component",
        "child_type": "Part",
        "field_name": "parts",
        "doc": "Organizer that groups Part components.",
    },
}


# =============================================================================
# Helpers
# =============================================================================


def collect_dataitem_types(classes, type_map):
    """
    Collect all DataItem subclass type names used in components.
    
    Scans all component attributes to find references to DataItem types.
    Returns a sorted set of DataItem type names.
    """
    dataitem_types = set()
    
    for cls_info in classes:
        for attr in cls_info.get('attributes', []):
            type_name = attr.get('type_name', '')
            
            # Skip if empty
            if not type_name:
                continue
                
            # Extract base type name (handle dotted subtypes like "Load.Actual")
            base_type = type_name.split('.')[0]
            
            # Skip primitive types and Component types
            if base_type in ['DataItem', 'Component', 'Configuration', 
                            'ID', 'UUID', 'str', 'int', 'float', 
                            'bool', 'datetime', 'List', 'Optional']:
                continue
                
            # Check if this looks like a DataItem type (CamelCase, not a known component type)
            # Simple heuristic: if it's not in the component class names, assume it's a DataItem
            component_names = {c.get('name') for c in classes}
            if base_type not in component_names and base_type[0].isupper():
                dataitem_types.add(base_type)
    
    return sorted(dataitem_types)


def clean_doc(doc):
    """Clean MTConnect model documentation strings."""
    if not doc:
        return doc
    doc = doc.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    doc = doc.replace("{{term(", "").replace("{{termplural(", "")
    doc = doc.replace("{{property(", "").replace("{{block(", "")
    doc = doc.replace("{{package(", "").replace("{{url(", "")
    doc = doc.replace(")}}",  "").replace("}}", "")
    doc = doc.replace("&#10;", " ").replace("&#13;", " ")
    doc = doc.replace("$$", "")
    return " ".join(doc.split())


def brief_doc(doc, max_len=90):
    """Return first sentence of a cleaned doc, truncated if needed."""
    if not doc:
        return ""
    doc = clean_doc(doc)
    # Take first sentence
    for end in (".", ".\n", ".\r"):
        idx = doc.find(end)
        if idx != -1:
            doc = doc[: idx + 1]
            break
    if len(doc) > max_len:
        doc = doc[: max_len - 3] + "..."
    return doc


def extract_elem_doc(elem):
    """Extract the ownedComment body from an XML element."""
    for comment in elem.findall("ownedComment"):
        body = comment.get("body")
        if body:
            return body
    return None


# =============================================================================
# XML Model Parsing
# =============================================================================


def _build_class_info(root):
    """Extract all UML class definitions from the XML model root.
    
    Prioritizes classes from the 'Component Types' package when duplicates exist.
    """
    # Build type map for type resolution
    type_map = build_type_map(root)
    
    # Component Types package ID - contains canonical component definitions
    COMP_TYPES_PKG_ID = "EAPK_6BEE6977_1698_498c_87A6_34B5E656F773"
    
    # First pass: find Component Types package and extract its classes
    comp_types_classes = {}
    for pkg in root.iter():
        if pkg.get("{" + XMI_NS + "}type") == "uml:Package" and \
           pkg.get("{" + XMI_NS + "}id") == COMP_TYPES_PKG_ID:
            for elem in pkg.findall("packagedElement"):
                if elem.get("{" + XMI_NS + "}type") == "uml:Class":
                    name = elem.get("name")
                    xmi_id = elem.get("{" + XMI_NS + "}id")
                    if name and xmi_id:
                        comp_types_classes[name] = xmi_id
            break
    
    class_info = {}
    for elem in root.iter():
        xmi_type = elem.get("{" + XMI_NS + "}type")
        name = elem.get("name")
        xmi_id = elem.get("{" + XMI_NS + "}id")
        if xmi_type == "uml:Class" and name and xmi_id:
            # Skip if this is a duplicate and we already have the Component Types version
            if name in comp_types_classes and xmi_id != comp_types_classes[name]:
                continue
                
            parents = [
                gen.get("general")
                for gen in elem.findall("generalization")
                if gen.get("general")
            ]
            
            # Extract attributes and relationships
            attributes = []
            for attr in elem.findall("ownedAttribute"):
                attr_name = attr.get('name')
                type_id = attr.get('type')
                if not attr_name or not type_id:
                    continue
                
                # Get cardinality
                lower, upper = get_cardinality(attr)
                
                # Skip [0..0] cardinality (redefined to empty in leaf components)
                if lower == 0 and upper == '0':
                    continue
                
                # Resolve type name
                type_name = resolve_type_name(root, type_id, type_map)
                
                # Get attribute documentation
                attr_doc_elem = attr.find('ownedComment')
                attr_doc = extract_docstring(attr_doc_elem) if attr_doc_elem else ""
                
                attributes.append({
                    'xml_name': attr_name,
                    'type_name': type_name,
                    'lower': lower,
                    'upper': upper,
                    'doc': attr_doc
                })
            
            is_leaf = elem.get("isLeaf") == "true"
            
            # Manual override: Chuck is a leaf component per MTConnect standard
            # (isLeaf attribute not set in v2.6 XMI but semantically it's a leaf)
            if name == "Chuck":
                is_leaf = True
            
            class_info[xmi_id] = {
                "name": name,
                "parent_ids": parents,
                "doc": extract_elem_doc(elem) or "",
                "is_abstract": elem.get("isAbstract") == "true",
                "is_leaf": is_leaf,
                "attributes": attributes,
            }
    return class_info, type_map


def _is_component_descendant(xmi_id, class_info, visited=None):
    """Return True if *xmi_id* is a transitive child of Component."""
    if visited is None:
        visited = set()
    if xmi_id in visited:
        return False
    visited.add(xmi_id)
    if xmi_id == COMPONENT_XMI_ID:
        return True
    info = class_info.get(xmi_id)
    if not info:
        return False
    return any(
        _is_component_descendant(p, class_info, visited)
        for p in info["parent_ids"]
    )


def _should_skip(name, xmi_id, info):
    """Return True if this class should be excluded from generation."""
    if xmi_id == COMPONENT_XMI_ID:
        return True
    if name in SKIP_NAMES or name in DEPRECATED_EXCLUDE:
        return True
    if name == "Component" and info["is_abstract"]:
        return True
    # Device is handled as a static template
    return name == "Device"


def _resolve_parent(info, class_info):
    """Resolve the Component-tree parent name for a class.
    
    Leaf components (isLeaf="true") inherit directly from ComponentBase
    to avoid inheriting the components field.
    
    Non-leaf components use their natural parent from the XMI hierarchy.
    """
    is_leaf = info.get("is_leaf", False)
    
    # Leaf components always inherit directly from ComponentBase
    if is_leaf:
        return "ComponentBase"
    
    # Non-leaf components use their parent from the hierarchy
    for p_id in info["parent_ids"]:
        if p_id == COMPONENT_XMI_ID:
            return "Component"
        p_info = class_info.get(p_id)
        if p_info and _is_component_descendant(p_id, class_info):
            return p_info["name"]
    
    # Default to Component for non-leaf classes
    return "Component"


def parse_model(xml_path):
    """Parse the MTConnect model XML and extract component types.

    Returns a tuple: (list of component dicts, type_map dict, root element)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    class_info, type_map = _build_class_info(root)

    components = []
    seen_names = set()

    for xmi_id, info in class_info.items():
        name = info["name"]
        if _should_skip(name, xmi_id, info):
            continue
        if not _is_component_descendant(xmi_id, class_info):
            continue
        if name in seen_names:
            continue
        seen_names.add(name)

        parent_name = _resolve_parent(info, class_info)
        deprecated = "DEPRECATED" in info["doc"].upper() if info["doc"] else False

        components.append(
            {
                "name": name,
                "parent": parent_name,
                "doc": brief_doc(info["doc"]),
                "is_abstract": info["is_abstract"],
                "is_leaf": info["is_leaf"],
                "deprecated": deprecated,
                "attributes": info["attributes"],  # Include attributes
            }
        )

    return sorted(components, key=lambda c: c["name"]), type_map, root


# =============================================================================
# Topological Sort
# =============================================================================


def topological_sort(classes):
    """Sort classes so parents appear before children.

    *classes* is a list of dicts with 'name' and 'parent' keys.
    Returns a new list in dependency order.
    """
    # Build adjacency (parent -> children)
    children_of = {}
    class_map = {c["name"]: c for c in classes}

    for c in classes:
        parent = c["parent"]
        children_of.setdefault(parent, []).append(c["name"])

    # BFS from roots (classes whose parent is not in the class_map)
    order = []
    visited = set()

    def visit(name):
        if name in visited:
            return
        visited.add(name)
        # Visit parent first
        if name in class_map:
            parent = class_map[name]["parent"]
            if parent in class_map:
                visit(parent)
        order.append(name)
        # Then visit children alphabetically
        for child in sorted(children_of.get(name, [])):
            visit(child)

    # Start from roots: classes whose parent is NOT in the class set
    # (parent == "Component" typically, since Component is a static template)
    roots = sorted(
        c["name"]
        for c in classes
        if c["parent"] not in class_map
    )
    for root in roots:
        visit(root)

    # Any remaining (shouldn't happen with valid data)
    for c in classes:
        visit(c["name"])

    return [class_map[name] for name in order if name in class_map]


# =============================================================================
# Code Generation
# =============================================================================


def generate_module_header(dataitem_types):
    """Generate module header with detected DataItem type imports."""
    header_lines = [
        '"""',
        'MTConnect Component Models',
        '',
        'Component hierarchy representing the physical and logical organization of',
        'manufacturing equipment in the MTConnect device information model.',
        '',
        'Reference: MTConnect Standard v2.6 Normative Model',
        'Auto-generated from: model_2.6.xml',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass, field',
        'from typing import TYPE_CHECKING, Optional, List',
        '',
        'from mtconnect.models.configurations import Configuration',
        'from mtconnect.types.primitives import ID, UUID',
        '',
        'if TYPE_CHECKING:',
        '    from mtconnect.models.data_items import ('
    ]
    
    # Add DataItem first, then all specific types
    header_lines.append('        DataItem,')
    
    # Add imported DataItem types (max 5 per line for readability)
    if dataitem_types:
        for i in range(0, len(dataitem_types), 5):
            chunk = dataitem_types[i:i+5]
            line = '        ' + ', '.join(chunk)
            if i + 5 < len(dataitem_types):
                line += ','
            else:
                # Last line - no trailing comma
                pass
            header_lines.append(line)
    
    header_lines.append('    )')
    
    return '\n'.join(header_lines)


DESCRIPTION_TEMPLATE = '''

@dataclass
class Description:
    """
    Descriptive information about a piece of equipment.

    Provides manufacturer, model, serial number, and other identifying
    information for a Device.
    """
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    station: str | None = None
    description: str | None = None
'''

COMPONENT_BASE_TEMPLATE = '''

@dataclass
class ComponentBase:
    """
    Base class for all MTConnect components.

    Components represent functional sub-units of a Device, organized in a
    hierarchical structure that models the physical and logical organization
    of manufacturing equipment.

    Reference: https://model.mtconnect.org/#Package__EAPK_7E9F9609_E982_40e1_88EC_28890F7ECF79
    """
    id: ID
    name: str
    uuid: UUID | None = None
    native_name: str | None = None
    sample_interval: float | None = None
    sample_rate: float | None = None
    description: Description | None = None
    configuration: Configuration | None = None
    data_items: list[DataItem] = field(default_factory=list)

    def __post_init__(self):
        """Validate component after initialization"""
        if not isinstance(self.id, (ID, str)):
            msg = f"Component id must be ID or str, got {type(self.id)}"
            raise TypeError(msg)
        if isinstance(self.id, str):
            self.id = ID(self.id)

        if self.uuid and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)
'''

COMPONENT_TEMPLATE = '''

@dataclass
class Component(ComponentBase):
    """
    Component with child component support.
    
    Non-leaf components can contain other components in a hierarchical structure.
    Leaf components do not have this field.
    """
    components: list[Component] = field(default_factory=list)
'''

DEVICE_TEMPLATE = '''

@dataclass
class Device(Component):
    """
    Top-level Component representing a piece of equipment.

    A Device is a Component that organizes all information for a single piece
    of manufacturing equipment. It represents the root of the component hierarchy
    and contains Axes, Controllers, Systems, and other sub-components.

    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1623082330438_892066_4246
    """
    iso_841_class: str | None = None
    mtconnect_version: str = "2.6.0"

    def add_component(self, component: Component) -> None:
        """Add a child component to this device"""
        self.components.append(component)

    def add_data_item(self, data_item: DataItem) -> None:
        """Add a data item to this device"""
        self.data_items.append(data_item)
'''


def generate_class_code(cls_info, type_map, root):
    """Generate a @dataclass class definition for a component type."""
    name = cls_info["name"]
    parent = cls_info["parent"]
    doc = cls_info.get("doc", "")
    attributes = cls_info.get("attributes", [])

    lines = []
    lines.append("")
    lines.append("")
    lines.append("@dataclass")
    lines.append(f"class {name}({parent}):")

    # Build docstring
    if doc:
        lines.append(f'    """{doc}')
    else:
        lines.append(f'    """{name} component.')
    
    # Add relationship documentation
    relationships = []
    required_lists = []
    
    for attr in attributes:
        xml_name = attr['xml_name']
        type_name = attr['type_name']
        lower = attr['lower']
        upper = attr['upper']
        attr_doc = attr['doc']
        
        # Check if this is a relationship
        is_relationship = xml_name.startswith('has') or xml_name.startswith('observes')
        
        if is_relationship:
            # Add note for prohibited [0..0] relationships
            if lower == 0 and upper == '0':
                rel_desc = f"    - {xml_name} [{lower}..{upper}] (prohibited)"
            else:
                rel_desc = f"    - {xml_name} [{lower}..{upper}]"
            if attr_doc:
                rel_desc += f": {attr_doc}"
            relationships.append(rel_desc)
            
            # Track required lists for validation
            if is_required_list(lower, upper):
                field_name = attribute_to_field_name(xml_name)
                required_lists.append((field_name, xml_name, lower, upper))
    
    if relationships:
        lines.append("")
        lines.append("    MTConnect Relationships:")
        lines.extend(relationships)
    
    lines.append('    """')

    # Generate fields
    # IMPORTANT: Python dataclass inheritance requires that subclasses don't add required
    # fields if parent has optional fields. All generated component classes (except
    # the base Component template) get defaults on all fields to avoid ordering issues.
    fields_generated = False
    if attributes:
        for attr in attributes:
            xml_name = attr['xml_name']
            type_name = attr['type_name']
            lower = attr['lower']
            upper = attr['upper']
            attr_doc = attr['doc']
            
            # Skip [0..0] relationships (prohibited in UML)
            if lower == 0 and upper == '0':
                continue
            
            field_name = attribute_to_field_name(xml_name)
            python_type = format_python_type(type_name, lower, upper, use_forward_ref=True)
            default = format_field_default(lower, upper)
            
            # All generated fields need defaults to work with Component base class inheritance
            if not default:
                # Required field but needs default for dataclass compatibility
                if upper == '*':
                    default = " = field(default_factory=list)"
                else:
                    default = " = None"
                # Track required fields for validation
                is_relationship = xml_name.startswith('has') or xml_name.startswith('observes')
                if is_relationship and lower > 0:
                    required_lists.append((field_name, xml_name, lower, upper))
            
            field_line = f"    {field_name}: {python_type}{default}"
            if attr_doc:
                field_line += f"  # {attr_doc}"
            
            lines.append(field_line)
            fields_generated = True
    
    # If no fields were generated, add pass
    if not fields_generated:
        lines.append("    pass")
    
    # Add __post_init__ validation for required relationships
    if required_lists:
        lines.append("")
        lines.append("    def __post_init__(self):")
        for field_name, xml_name, lower, upper in required_lists:
            if upper == '*':
                lines.append(f"        if not self.{field_name}:")
                lines.append(f"            raise ValueError(\"{xml_name}: required relationship [{lower}..{upper}] cannot be empty\")")
            else:
                lines.append(f"        if self.{field_name} is None:")
                lines.append(f"            raise ValueError(\"{xml_name}: required relationship [{lower}..{upper}] cannot be None\")")
        lines.append("        super().__post_init__()")

    return "\n".join(lines)


def generate_organizer_code(name, info):
    """Generate a @dataclass class definition for an organizer type."""
    parent = info["parent"]
    child_type = info["child_type"]
    field_name = info["field_name"]
    doc = info["doc"]

    lines = []
    lines.append("")
    lines.append("")
    lines.append("@dataclass")
    lines.append(f"class {name}({parent}):")
    lines.append(f'    """{doc}"""')
    lines.append(
        f"    {field_name}: list[{child_type}] = field(default_factory=list)"
    )
    return "\n".join(lines)


def generate_components_py(xml_components, type_map, root, output_path):
    """Generate the complete components.py file."""
    # Merge XML-derived classes with organizer types
    all_classes = list(xml_components)

    for org_name, org_info in ORGANIZER_TYPES.items():
        all_classes.append(
            {
                "name": org_name,
                "parent": org_info["parent"],
                "doc": org_info["doc"],
                "is_abstract": False,
                "is_leaf": False,
                "deprecated": False,
                "organizer": org_info,
                "attributes": [],  # Organizers don't have XMI attributes
            }
        )

    # Collect DataItem types used in components
    dataitem_types = collect_dataitem_types(all_classes, type_map)
    print(f"Found {len(dataitem_types)} DataItem types referenced in components")
    
    # Generate module header with DataItem imports
    module_header = generate_module_header(dataitem_types)

    # Topological sort
    sorted_classes = topological_sort(all_classes)

    # Generate code
    parts = [module_header, DESCRIPTION_TEMPLATE, COMPONENT_BASE_TEMPLATE, COMPONENT_TEMPLATE, DEVICE_TEMPLATE]

    for cls_info in sorted_classes:
        if "organizer" in cls_info:
            parts.append(generate_organizer_code(cls_info["name"], cls_info["organizer"]))
        else:
            parts.append(generate_class_code(cls_info, type_map, root))

    # Final newline
    parts.append("")

    content = "\n".join(parts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
    print(f"Generated {output_path}")
    return content


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate MTConnect component hierarchy from model XML"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=".github/agents/data/model_2.6.xml",
        help="Path to MTConnect model XML file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="mtconnect/models/components.py",
        help="Output file path",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    xml_file = repo_root / args.model_path
    output_file = repo_root / args.output

    if not xml_file.exists():
        print(f"Error: Model file not found at {xml_file}")
        sys.exit(1)

    print(f"Parsing {xml_file}...")
    components, type_map, root = parse_model(xml_file)
    print(f"Found {len(components)} component types from XML")

    print(f"Adding {len(ORGANIZER_TYPES)} organizer types")
    total = len(components) + len(ORGANIZER_TYPES)
    print(f"Total component classes (excl. Description, Component, Device): {total}")

    generate_components_py(components, type_map, root, output_file)

    # Summary
    print(f"\nTotal classes in generated file: {total + 3}")
    print("  Static templates: Description, Component, Device")
    print(f"  Organizer types: {len(ORGANIZER_TYPES)}")
    print(f"  Component types from XML: {len(components)}")


if __name__ == "__main__":
    main()
