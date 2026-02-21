#!/usr/bin/env python3
"""
Generate MTConnect DataItem type classes from XMI model.

Extracts DataItem classes from the DataItems package and generates
Python dataclasses categorized by SAMPLE, EVENT, and CONDITION.
"""

import sys
from pathlib import Path
from typing import List, Dict, Set
import xml.etree.ElementTree as ET

# Import shared generator utilities
sys.path.insert(0, str(Path(__file__).parent))

from generator_utils import (
    parse_xmi, build_type_map, get_cardinality, resolve_type_name,
    extract_docstring, attribute_to_field_name, format_python_type,
    format_field_default, get_parent_class, sanitize_class_name, NS
)

# DataItems package XMI ID
DATAITEMS_PACKAGE_ID = 'EAPK_0FAC31E7_7957_49d2_AD4C_BCFBEF9878FD'


def extract_dataitem_classes(root: ET.Element) -> Dict[str, List[ET.Element]]:
    """
    Extract all DataItem class elements from the MTConnect model.
    
    DataItem types are not in the DataItems package - they are classes throughout
    the model that inherit from Sample, Event, or Condition via generalization.
    
    NOTE: There are multiple Sample/Event/Condition classes in the model. We need
    to use the correct ones from the SysML model (package 'MTConnectSysMlModel'),
    not the ones in the DataItems package.
    
    Args:
        root: Root element from parse_xmi()
        
    Returns:
        Dict with keys 'SAMPLE', 'EVENT', 'CONDITION' mapping to lists of class elements
    """
    # Find ALL Sample, Event, Condition classes - collect all IDS
    base_class_ids = {'Sample': [], 'Event': [], 'Condition': []}
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Class':
            name = elem.get('name')
            if name in ['Sample', 'Event', 'Condition']:
                xmi_id = elem.get('{http://www.omg.org/spec/XMI/20131001}id')
                base_class_ids[name].append(xmi_id)
    
    print(f"Found base classes:")
    print(f"  Sample: {len(base_class_ids['Sample'])} instances")
    print(f"  Event: {len(base_class_ids['Event'])} instances")
    print(f"  Condition: {len(base_class_ids['Condition'])} instances")
    
    # Find all classes that inherit from ANY Sample, Event, or Condition
    categorized = {'SAMPLE': [], 'EVENT': [], 'CONDITION': []}
    seen_classes = set()  # Track by name to avoid duplicates
    
    for elem in root.iter():
        if elem.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Class':
            class_name = elem.get('name')
            if not class_name or class_name in seen_classes:
                continue
            
            # Check generalization
            for gen in elem.findall('generalization'):
                general = gen.get('general')
                if general in base_class_ids['Sample']:
                    categorized['SAMPLE'].append(elem)
                    seen_classes.add(class_name)
                    break
                elif general in base_class_ids['Event']:
                    categorized['EVENT'].append(elem)
                    seen_classes.add(class_name)
                    break
                elif general in base_class_ids['Condition']:
                    categorized['CONDITION'].append(elem)
                    seen_classes.add(class_name)
                    break
    
    return categorized


def categorize_dataitem(cls_elem: ET.Element, root: ET.Element, type_map: Dict[str, str]) -> str:
    """
    Determine if a DataItem class is SAMPLE, EVENT, or CONDITION.
    
    THIS FUNCTION IS DEPRECATED - categorization now happens in extract_dataitem_classes
    via generalization relationships.
    
    Args:
        cls_elem: Class element
        root: Root element
        type_map: Type mapping
        
    Returns:
        'SAMPLE', 'EVENT', 'CONDITION', or 'UNKNOWN'
    """
    # Check parent class
    parent = get_parent_class(cls_elem, root, type_map)
    
    if parent in ['Sample', 'SampleDataItem']:
        return 'SAMPLE'
    elif parent in ['Event', 'EventDataItem']:
        return 'EVENT'
    elif parent in ['Condition', 'ConditionDataItem']:
        return 'CONDITION'
    
    # Default: UNKNOWN (will be placed in base module)
    return 'UNKNOWN'



def generate_dataitem_class(
    cls_elem: ET.Element,
    root: ET.Element,
    type_map: Dict[str, str],
    category: str
) -> str:
    """
    Generate Python dataclass code for a DataItem type.
    
    Args:
        cls_elem: Class element from XMI
        root: Root element
        type_map: Type resolution mapping
        category: SAMPLE, EVENT, or CONDITION
        
    Returns:
        Generated Python class code
    """
    class_name = cls_elem.get('name')
    if not class_name:
        return ""
    
    # Sanitize class name for Python
    class_name = sanitize_class_name(class_name)
    
    # Extract documentation
    doc_elem = cls_elem.find('ownedComment')
    doc_text = extract_docstring(doc_elem) if doc_elem else f"{class_name} DataItem."
    
    # Find parent class
    parent = get_parent_class(cls_elem, root, type_map)
    
    # Use category-specific base class
    # DataItem types inherit from Sample/Event/Condition in XMI, but we want
    # them to inherit from SampleDataItem/EventDataItem/ConditionDataItem in Python
    if parent in ['Sample', 'SampleDataItem'] or category == 'SAMPLE':
        parent = 'SampleDataItem'
    elif parent in ['Event', 'EventDataItem'] or category == 'EVENT':
        parent = 'EventDataItem'
    elif parent in ['Condition', 'ConditionDataItem'] or category == 'CONDITION':
        parent = 'ConditionDataItem'
    else:
        parent = 'DataItem'
    
    # Extract attributes
    attributes = []
    seen_fields = set()
    
    # Types to skip - these are complex types not yet defined in the codebase
    skip_types = {
        'AlarmLimitResult', 'ControlLimitResult', 'FeatureMeasurementResult',
        'LocationAddressResult', 'LocationSpatialGeographicResult',
        'MaintenanceListResult', 'SensorAttachmentResult', 'SpecificationLimitResult',
        'UnknownType'
    }
    
    for attr in cls_elem.findall('ownedAttribute'):
        attr_name = attr.get('name')
        if not attr_name or attr_name in ['category', 'type']:
            continue  # Skip base class fields
        
        type_id = attr.get('type')
        if not type_id:
            continue
        
        type_name = resolve_type_name(root, type_id, type_map)
        
        # Skip undefined complex types
        if type_name in skip_types or type_name.endswith('Result') and type_name not in ['GuardResult']:
            continue
        
        lower, upper = get_cardinality(attr)
        
        field_name = attribute_to_field_name(attr_name)
        
        if field_name in seen_fields:
            continue
        seen_fields.add(field_name)
        
        python_type = format_python_type(type_name, lower, upper, use_forward_ref=False)
        default = format_field_default(lower, upper)
        
        # For subclasses, force defaults
        if not default:
            if upper == '*':
                default = ' = field(default_factory=list)'
            else:
                default = ' = None'
        
        field_doc_elem = attr.find('ownedComment')
        field_doc = extract_docstring(field_doc_elem) if field_doc_elem else ""
        
        attributes.append({
            'field_name': field_name,
            'python_type': python_type,
            'default': default,
            'doc': field_doc
        })
    
    # Build class code
    lines = []
    lines.append("")
    lines.append("")
    lines.append("@dataclass")
    lines.append(f"class {class_name}({parent}):")
    
    # Docstring
    if doc_text:
        lines.append(f'    """{doc_text}"""')
    else:
        lines.append(f'    """{class_name} DataItem."""')
    
    # Attributes
    if attributes:
        for attr in attributes:
            field_line = f"    {attr['field_name']}: {attr['python_type']}{attr['default']}"
            if attr['doc']:
                field_line += f"  # {attr['doc']}"
            lines.append(field_line)
    else:
        lines.append("    pass")
    
    return "\n".join(lines)


def generate_dataitems_module(model_path: str, output_path: str):
    """
    Generate complete data_items.py module.
    
    Args:
        model_path: Path to model_2.6.xml
        output_path: Path to output data_items.py
    """
    root = parse_xmi(model_path)
    type_map = build_type_map(root)
    
    # Extract DataItem classes - now returns dict with 'SAMPLE', 'EVENT', 'CONDITION' keys
    categorized_classes = extract_dataitem_classes(root)
    
    sample_classes = categorized_classes['SAMPLE']
    event_classes = categorized_classes['EVENT']
    condition_classes = categorized_classes['CONDITION']
    
    # Sort each category by name
    sample_classes.sort(key=lambda e: e.get('name', ''))
    event_classes.sort(key=lambda e: e.get('name', ''))
    condition_classes.sort(key=lambda e: e.get('name', ''))
    
    # Generate code for each class
    sample_codes = []
    event_codes = []
    condition_codes = []
    
    for cls_elem in sample_classes:
        code = generate_dataitem_class(cls_elem, root, type_map, 'SAMPLE')
        if code:
            sample_codes.append(code)
    
    for cls_elem in event_classes:
        code = generate_dataitem_class(cls_elem, root, type_map, 'EVENT')
        if code:
            event_codes.append(code)
    
    for cls_elem in condition_classes:
        code = generate_dataitem_class(cls_elem, root, type_map, 'CONDITION')
        if code:
            condition_codes.append(code)
    
    # Build module
    module_lines = [
        '"""',
        'MTConnect DataItem Models',
        '',
        'DataItem definitions representing observation points for data collection from',
        'manufacturing equipment. DataItems are categorized as SAMPLE, EVENT, or CONDITION',
        'and define the type, units, constraints, and metadata for equipment observations.',
        '',
        'Reference: MTConnect Standard v2.6 - DataItems Package',
        'Auto-generated from: model_2.6.xml',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass, field',
        'from datetime import datetime',
        'from typing import Optional, List, Union, TYPE_CHECKING',
        'from enum import Enum',
        '',
        'from mtconnect.types.enums import (',
        '    UnitEnum,',
        '    ActuatorStateEnum, AlarmCodeEnum, AlarmSeverityEnum, AlarmStateEnum,',
        '    AvailabilityEnum, AxisCouplingEnum, AxisInterlockEnum, AxisStateEnum,',
        '    BatteryStateEnum, CharacteristicStatusEnum, ChuckInterlockEnum, ChuckStateEnum,',
        '    ConnectionStatusEnum, ControllerModeEnum, ControllerModeOverrideEnum,',
        '    DirectionEnum, DoorStateEnum, EmergencyStopEnum, EndOfBarEnum,',
        '    EquipmentModeEnum, ExecutionEnum, FunctionalModeEnum, InterfaceStateEnum,',
        '    LeakDetectEnum, LockStateEnum, OperatingModeEnum, PartCountTypeEnum,',
        '    PartDetectEnum, PartProcessingStateEnum, PartStatusEnum, PathModeEnum,',
        '    PowerStateEnum, PowerStatusEnum, ProcessStateEnum, ProgramEditEnum,',
        '    ProgramLocationTypeEnum, RotaryModeEnum, SpindleInterlockEnum,',
        '    UncertaintyTypeEnum, ValveStateEnum, WaitStateEnum',
        ')',
        'from mtconnect.types.primitives import ID, MTCFloat, MTCInteger',
        'from mtconnect.types.sample import SampleType',
        'from mtconnect.types.event import EventType',
        'from mtconnect.types.condition import ConditionType',
        'from mtconnect.types.subtype import DataItemSubType',
        '',
        '',
        'class DataItemCategory(Enum):',
        '    """MTConnect DataItem categories"""',
        '    SAMPLE = "SAMPLE"',
        '    EVENT = "EVENT"',
        '    CONDITION = "CONDITION"',
        '',
        '',
        '@dataclass',
        'class Constraints:',
        '    """',
        '    Constraints defining valid value ranges or sets for a DataItem.',
        '    """',
        '    minimum: Optional[float] = None',
        '    maximum: Optional[float] = None',
        '    nominal: Optional[float] = None',
        '    values: Optional[List[str]] = None',
        '',
        '',
        '@dataclass',
        'class DataItem:',
        '    """',
        '    Base class for all MTConnect DataItems.',
        '    ',
        '    A DataItem represents a measurement or observation point on a Component.',
        '    """',
        '    id: ID',
        '    type: Union[SampleType, EventType, ConditionType, str]',
        '    category: DataItemCategory',
        '    name: Optional[str] = None',
        '    sub_type: Optional[DataItemSubType] = None',
        '    units: Optional[UnitEnum] = None',
        '    native_units: Optional[UnitEnum] = None',
        '    native_scale: Optional[MTCFloat] = None',
        '    significant_digits: Optional[MTCInteger] = None',
        '    coordinate_system: Optional[ID] = None',
        '    composition_id: Optional[str] = None',
        '    constraints: Optional[Constraints] = None',
        '    discrete: bool = False',
        '',
        '    def __post_init__(self):',
        '        """Validate DataItem after initialization"""',
        '        if isinstance(self.id, str):',
        '            self.id = ID(self.id)',
        '',
        '',
        '@dataclass',
        'class SampleDataItem(DataItem):',
        '    """',
        '    DataItem representing continuously variable numeric measurements.',
        '    ',
        '    SAMPLE DataItems report numeric values that vary continuously over time.',
        '    """',
        '    category: DataItemCategory = DataItemCategory.SAMPLE',
        '',
        '',
        '@dataclass',
        'class EventDataItem(DataItem):',
        '    """',
        '    DataItem representing discrete, non-numeric state or status information.',
        '    ',
        '    EVENT DataItems report discrete values that change in response to specific',
        '    occurrences or state transitions.',
        '    """',
        '    category: DataItemCategory = DataItemCategory.EVENT',
        '',
        '',
        '@dataclass',
        'class ConditionDataItem(DataItem):',
        '    """',
        '    DataItem representing the health status of a Component.',
        '    ',
        '    CONDITION DataItems report the operational health and status of equipment.',
        '    """',
        '    category: DataItemCategory = DataItemCategory.CONDITION',
    ]
    
    # Add categorized classes
    if sample_codes:
        module_lines.append('')
        module_lines.append('')
        module_lines.append('# ' + '=' * 76)
        module_lines.append('# SAMPLE DataItems')
        module_lines.append('# ' + '=' * 76)
        module_lines.extend(sample_codes)
    
    if event_codes:
        module_lines.append('')
        module_lines.append('')
        module_lines.append('# ' + '=' * 76)
        module_lines.append('# EVENT DataItems')
        module_lines.append('# ' + '=' * 76)
        module_lines.extend(event_codes)
    
    if condition_codes:
        module_lines.append('')
        module_lines.append('')
        module_lines.append('# ' + '=' * 76)
        module_lines.append('# CONDITION DataItems')
        module_lines.append('# ' + '=' * 76)
        module_lines.extend(condition_codes)
    
    module_lines.append("")  # Final newline
    
    # Write to file
    output_file = Path(output_path)
    output_file.write_text("\n".join(module_lines))
    
    print(f"Generated: {output_path}")
    print(f"  - {len(sample_classes)} SAMPLE DataItem classes")
    print(f"  - {len(event_classes)} EVENT DataItem classes")
    print(f"  - {len(condition_classes)} CONDITION DataItem classes")
    print(f"  - Total: {len(sample_classes) + len(event_classes) + len(condition_classes)} DataItem types")


if __name__ == '__main__':
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    model_path = project_root / '.github' / 'agents' / 'data' / 'model_2.6.xml'
    output_path = project_root / 'mtconnect' / 'models' / 'data_items.py'
    
    if not model_path.exists():
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)
    
    generate_dataitems_module(str(model_path), str(output_path))
