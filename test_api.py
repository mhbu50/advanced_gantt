#!/usr/bin/env python3
"""
Test script for Advanced Gantt API endpoints
This script tests the API functionality without requiring a full Frappe installation
"""

import json
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'advanced_gantt'))

def test_data_transformation():
    """Test the data transformation functions"""
    print("Testing data transformation functions...")
    
    # Mock data similar to what ERPNext would return
    mock_projects = [
        {
            'name': 'PROJECT-001',
            'project_name': 'Website Redesign',
            'status': 'Open',
            'priority': 'High',
            'percent_complete': 25,
            'expected_start_date': '2024-01-01',
            'expected_end_date': '2024-03-31',
            'actual_start_date': '2024-01-05',
            'actual_end_date': None,
            'project_type': 'Internal',
            'department': 'IT',
            'company': 'Test Company',
            'estimated_costing': 50000,
            'total_costing_amount': 12500,
            'description': 'Complete website redesign project'
        }
    ]
    
    mock_tasks = [
        {
            'name': 'TASK-001',
            'subject': 'Design Homepage',
            'status': 'Working',
            'priority': 'High',
            'progress': 50,
            'project': 'PROJECT-001',
            'exp_start_date': '2024-01-01',
            'exp_end_date': '2024-01-15',
            'act_start_date': '2024-01-05',
            'act_end_date': None,
            'expected_time': 40,
            'actual_time': 20,
            'parent_task': None,
            'task_weight': 1,
            'assigned_to': 'user@example.com',
            'department': 'IT',
            'company': 'Test Company',
            'description': 'Design the new homepage layout',
            'is_milestone': False
        },
        {
            'name': 'TASK-002',
            'subject': 'Homepage Review',
            'status': 'Open',
            'priority': 'Medium',
            'progress': 0,
            'project': 'PROJECT-001',
            'exp_start_date': '2024-01-16',
            'exp_end_date': '2024-01-16',
            'act_start_date': None,
            'act_end_date': None,
            'expected_time': 2,
            'actual_time': 0,
            'parent_task': 'TASK-001',
            'task_weight': 0.5,
            'assigned_to': 'manager@example.com',
            'department': 'IT',
            'company': 'Test Company',
            'description': 'Review homepage design',
            'is_milestone': True
        }
    ]
    
    mock_dependencies = [
        {
            'parent': 'TASK-002',
            'task': 'TASK-002',
            'depends_on_task': 'TASK-001'
        }
    ]
    
    # Import the transformation functions
    try:
        from api.gantt_data import (
            transform_tasks_for_bryntum,
            transform_dependencies_for_bryntum
        )
        
        # Test task transformation
        bryntum_tasks = transform_tasks_for_bryntum(mock_projects, mock_tasks)
        print(f"✓ Transformed {len(bryntum_tasks)} tasks successfully")
        
        # Test dependency transformation
        bryntum_deps = transform_dependencies_for_bryntum(mock_dependencies)
        print(f"✓ Transformed {len(bryntum_deps)} dependencies successfully")
        
        # Print sample output
        print("\nSample Bryntum Task Data:")
        print(json.dumps(bryntum_tasks[0], indent=2, default=str))
        
        if bryntum_deps:
            print("\nSample Bryntum Dependency Data:")
            print(json.dumps(bryntum_deps[0], indent=2, default=str))
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Transformation error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'advanced_gantt/hooks.py',
        'advanced_gantt/api/__init__.py',
        'advanced_gantt/api/gantt_data.py',
        'advanced_gantt/public/js/gantt_component.js',
        'advanced_gantt/public/css/gantt_styles.css',
        'advanced_gantt/www/gantt.py',
        'advanced_gantt/www/gantt.html',
        'advanced_gantt/advanced_gantt/doctype/gantt_chart_settings/gantt_chart_settings.json',
        'advanced_gantt/advanced_gantt/doctype/gantt_chart_settings/gantt_chart_settings.py',
        'advanced_gantt/advanced_gantt/workspace/advanced_gantt/advanced_gantt.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n{len(missing_files)} files are missing!")
        return False
    else:
        print(f"\n✓ All {len(required_files)} required files exist")
        return True

def test_javascript_syntax():
    """Basic syntax check for JavaScript files"""
    print("\nTesting JavaScript syntax...")
    
    js_files = [
        'advanced_gantt/public/js/gantt_component.js'
    ]
    
    for js_file in js_files:
        full_path = os.path.join(os.path.dirname(__file__), js_file)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                content = f.read()
                
            # Basic syntax checks
            if 'class AdvancedGanttChart' in content:
                print(f"✓ {js_file} - Class definition found")
            else:
                print(f"✗ {js_file} - Class definition missing")
                
            if 'async fetchGanttData()' in content:
                print(f"✓ {js_file} - API fetch method found")
            else:
                print(f"✗ {js_file} - API fetch method missing")
                
            if 'window.AdvancedGanttChart' in content:
                print(f"✓ {js_file} - Global export found")
            else:
                print(f"✗ {js_file} - Global export missing")
        else:
            print(f"✗ {js_file} - File not found")

def main():
    """Run all tests"""
    print("Advanced Gantt App - Test Suite")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Data Transformation", test_data_transformation),
        ("JavaScript Syntax", test_javascript_syntax)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The Advanced Gantt app is ready for installation.")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please review the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)