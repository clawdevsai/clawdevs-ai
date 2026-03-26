#!/usr/bin/env python3
"""
Script to fix test file issues.
"""

import os
import sys

def fix_test_file(filepath):
    """Fix a test file."""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove reset_mock import from test_config.py
    if 'reset_mock' in content:
        content = content.replace(
            'from unittest.mock import patch, MagicMock, reset_mock',
            'from unittest.mock import patch, MagicMock'
        )
        content = content.replace(
            'from unittest.mock import reset_mock',
            ''
        )
    
    # Fix @pytest.mark.mark.asyncio to @pytest.mark.asyncio
    content = content.replace('@pytest.mark.mark.asyncio', '@pytest.mark.asyncio')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Fix all test files."""
    test_dir = sys.argv[1] if len(sys.argv) > 1 else 'tests'
    
    print(f"🔍 Fixing test files in {test_dir}...")
    
    fixed_count = 0
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_test_file(filepath):
                    print(f"✅ Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")
    return 0

if __name__ == '__main__':
    sys.exit(main())
