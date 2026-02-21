#!/usr/bin/env python3
"""
Master script to run all MTConnect model generators in correct order.

This script orchestrates the generation of all model files:
1. configurations.py (no dependencies)
2. data_items.py (no dependencies)
3. components.py (depends on data_items for TYPE_CHECKING)
4. compositions.py (depends on components, configurations)
5. references.py (depends on components, data_items)

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
    print(f"Output dir: {project_root / 'mtconnect' / 'models'}")
    print()
    
    # Define generators in correct dependency order
    generators = [
        ('generate_configurations.py', 'No dependencies'),
        ('generate_data_items.py', 'No dependencies'),
        ('generate_components.py', 'Depends on: data_items (TYPE_CHECKING)'),
        ('generate_compositions.py', 'Depends on: components, configurations'),
        ('generate_references.py', 'Depends on: components, data_items'),
    ]
    
    all_stats = {}
    
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
        print(f"  {filename:20s} {stats['lines']:5d} lines, {stats['classes']:3d} classes, {stats['size_kb']:4d} KB")
        total_lines += stats['lines']
        total_classes += stats['classes']
    
    print(f"\n  {'TOTAL':20s} {total_lines:5d} lines, {total_classes:3d} classes")
    print("\n✓ All generators completed successfully")
    print("✓ All imports validated")
    
    # Run tests if requested
    if args.test:
        if not run_tests(project_root):
            sys.exit(1)
    

if __name__ == '__main__':
    main()
