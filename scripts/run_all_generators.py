#!/usr/bin/env python3
"""
Master script to run all MTConnect model generators in correct order.

This script orchestrates the generation of all model and type files:
1. types/ (event.py, sample.py, condition.py, subtype.py, interface_types.py, enums.py)
2. configurations.py (no dependencies)
3. data_items.py (no dependencies)
4. components.py (depends on data_items for TYPE_CHECKING)
5. compositions.py (depends on components, configurations)
6. references.py (depends on components, data_items)

Usage:
  python scripts/run_all_generators.py
  python scripts/run_all_generators.py --model-path path/to/model.xml
  python scripts/run_all_generators.py --test
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Dict


def run_enums_generator(model_path: Path, project_root: Path) -> Tuple[bool, Dict[str, Dict[str, int]]]:
    """
    Run the generate_enums.py script which produces 6 files in mtconnect/types/.
    
    Args:
        model_path: Path to the model XML file
        project_root: Project root directory
        
    Returns:
        Tuple of (success, dict of {filename: stats_dict})
    """
    script_path = project_root / 'scripts' / 'generate_enums.py'
    types_dir = project_root / 'mtconnect' / 'types'
    
    expected_files = [
        'event.py', 'sample.py', 'condition.py', 
        'subtype.py', 'interface_types.py', 'enums.py'
    ]
    
    print(f"Running generate_enums.py...", end=' ', flush=True)
    
    # Run the generator script
    result = subprocess.run(
        [sys.executable, str(script_path), '--model-path', str(model_path)],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    if result.returncode != 0:
        print("❌ FAILED")
        print(f"Error output:\n{result.stderr}")
        return False, {}
    
    # Validate all expected output files
    all_stats = {}
    total_lines = 0
    total_enums = 0
    
    for filename in expected_files:
        output_path = types_dir / filename
        
        if not output_path.exists():
            print(f"❌ FAILED ({filename} not created)")
            return False, {}
        
        file_size = output_path.stat().st_size
        if file_size == 0:
            print(f"❌ FAILED ({filename} is empty)")
            return False, {}
        
        content = output_path.read_text()
        line_count = len(content.splitlines())
        enum_count = content.count('class ') - content.count('@dataclass')
        
        all_stats[filename] = {
            'lines': line_count,
            'classes': enum_count,
            'size_kb': file_size // 1024
        }
        
        total_lines += line_count
        total_enums += enum_count
    
    print(f"✓ (6 files, {total_lines} lines, {total_enums} enums)")
    
    return True, all_stats


def run_generator(script_name: str, model_path: Path, project_root: Path) -> Tuple[bool, str, Dict[str, int]]:
    """
    Run a single generator script.
    
    Args:
        script_name: Name of the generator script (e.g., 'generate_configurations.py')
        model_path: Path to the model XML file
        project_root: Project root directory
        
    Returns:
        Tuple of (success, output_file_name, stats_dict)
    """
    script_path = project_root / 'scripts' / script_name
    
    # Determine output file name from script name
    output_name = script_name.replace('generate_', '').replace('.py', '.py')
    output_path = project_root / 'mtconnect' / 'models' / output_name
    
    print(f"Running {script_name}...", end=' ', flush=True)
    
    # Run the generator script
    result = subprocess.run(
        [sys.executable, str(script_path), '--model-path', str(model_path)],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    if result.returncode != 0:
        print("❌ FAILED")
        print(f"Error output:\n{result.stderr}")
        return False, output_name, {}
    
    # Validate output file exists and has content
    if not output_path.exists():
        print("❌ FAILED (output file not created)")
        return False, output_name, {}
    
    file_size = output_path.stat().st_size
    if file_size == 0:
        print("❌ FAILED (empty output file)")
        return False, output_name, {}
    
    # Count lines and classes
    content = output_path.read_text()
    line_count = len(content.splitlines())
    class_count = content.count('@dataclass\nclass ') + content.count('@dataclass\n\nclass ')
    
    print(f"✓ ({line_count} lines, {class_count} classes)")
    
    stats = {
        'lines': line_count,
        'classes': class_count,
        'size_kb': file_size // 1024
    }
    
    return True, output_name, stats


def validate_imports(project_root: Path) -> bool:
    """
    Test that all generated files can be imported without errors.
    
    Args:
        project_root: Project root directory
        
    Returns:
        True if all imports succeed, False otherwise
    """
    print("\nValidating imports...", end=' ', flush=True)
    
    test_script = """
import sys
sys.path.insert(0, '.')
try:
    from mtconnect.models import (
        Component, Device, DataItem,
        Configuration, Composition, ComponentRef
    )
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
"""
    
    result = subprocess.run(
        [sys.executable, '-c', test_script],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    if result.returncode != 0 or 'FAILED' in result.stdout:
        print("❌ FAILED")
        print(f"Import error:\n{result.stdout}\n{result.stderr}")
        return False
    
    print("✓")
    return True


def run_tests(project_root: Path) -> bool:
    """
    Run the test suite using pytest.
    
    Args:
        project_root: Project root directory
        
    Returns:
        True if all tests pass, False otherwise
    """
    print("\n" + "=" * 70)
    print("Running Test Suite")
    print("=" * 70)
    
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-v', '-o', 'addopts='],
        cwd=str(project_root)
    )
    
    if result.returncode != 0:
        print("\n❌ Tests failed")
        return False
    
    print("\n✓ All tests passed")
    return True


def main():
    """Run all generators in correct dependency order."""
    parser = argparse.ArgumentParser(
        description='Run all MTConnect model generators'
    )
    parser.add_argument(
        '--model-path',
        type=Path,
        default=None,
        help='Path to model XML file (default: .github/agents/data/model_2.6.xml)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test suite after successful generation'
    )
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    if args.model_path:
        model_path = args.model_path
    else:
        model_path = project_root / '.github' / 'agents' / 'data' / 'model_2.6.xml'
    
    # Validate model file exists
    if not model_path.exists():
        print(f"❌ Error: Model file not found: {model_path}")
        sys.exit(1)
    
    print("=" * 70)
    print("MTConnect Model Generation")
    print("=" * 70)
    print(f"Model file: {model_path}")
    print(f"Output dirs: {project_root / 'mtconnect' / 'types'}")
    print(f"             {project_root / 'mtconnect' / 'models'}")
    print()
    
    all_stats = {}
    
    # Step 1: Generate type enums (required by all other generators)
    print("[generate_enums.py]")
    print("  Generates all type enums (EVENT, SAMPLE, CONDITION, SubType, Interface, etc.)")
    print("  ", end='')
    
    success, enums_stats = run_enums_generator(model_path, project_root)
    
    if not success:
        print(f"\n❌ Generation failed at generate_enums.py")
        print("Stopping execution.")
        sys.exit(1)
    
    # Add enums stats to all_stats with a special marker
    all_stats['types/'] = enums_stats
    
    # Step 2: Generate model classes in correct dependency order
    generators = [
        ('generate_configurations.py', 'No dependencies'),
        ('generate_data_items.py', 'No dependencies'),
        ('generate_components.py', 'Depends on: data_items (TYPE_CHECKING)'),
        ('generate_compositions.py', 'Depends on: components, configurations'),
        ('generate_references.py', 'Depends on: components, data_items'),
    ]
    
    # Run each generator
    for script_name, dependency_note in generators:
        print(f"\n[{script_name}]")
        print(f"  {dependency_note}")
        print(f"  ", end='')
        
        success, output_name, stats = run_generator(script_name, model_path, project_root)
        
        if not success:
            print(f"\n❌ Generation failed at {script_name}")
            print("Stopping execution.")
            sys.exit(1)
        
        all_stats[output_name] = stats
    
    # Validate imports
    if not validate_imports(project_root):
        print("\n❌ Import validation failed")
        sys.exit(1)
    
    # Print summary
    print("\n" + "=" * 70)
    print("Generation Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    
    total_lines = 0
    total_classes = 0
    
    for filename, stats in all_stats.items():
        if filename == 'types/':
            # Special case: generate_enums.py creates multiple files
            print(f"\n  types/ (6 enum modules):")
            for type_file, type_stats in stats.items():
                print(f"    {type_file:18s} {type_stats['lines']:5d} lines, {type_stats['classes']:3d} enums, {type_stats['size_kb']:4d} KB")
                total_lines += type_stats['lines']
                total_classes += type_stats['classes']
        else:
            # Regular model file
            print(f"  models/{filename:14s} {stats['lines']:5d} lines, {stats['classes']:3d} classes, {stats['size_kb']:4d} KB")
            total_lines += stats['lines']
            total_classes += stats['classes']
    
    print(f"\n  {'TOTAL':20s} {total_lines:5d} lines, {total_classes:3d} types")
    print("\n✓ All generators completed successfully")
    print("✓ All imports validated")
    
    # Run tests if requested
    if args.test:
        if not run_tests(project_root):
            sys.exit(1)
    

if __name__ == '__main__':
    main()
