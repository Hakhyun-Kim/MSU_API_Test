#!/usr/bin/env python3
"""
Simple import test for CI/CD
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    # Use ASCII-safe characters for all platforms in CI
    check = "[OK]"
    warn = "[WARN]"
    fail = "[FAIL]"
    
    try:
        # Test basic imports
        print("Testing basic imports...")
        import PyQt6
        print(f"{check} PyQt6 imported successfully")
        
        import requests
        print(f"{check} requests imported successfully")
        
        import PIL
        print(f"{check} PIL imported successfully")
        
        # Test project imports
        print("\nTesting project imports...")
        
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        import models.character
        print(f"{check} models.character imported successfully")
        
        import models.item
        print(f"{check} models.item imported successfully")
        
        import api.api_client
        print(f"{check} api.api_client imported successfully")
        
        # Test UI imports (may fail in headless environment)
        try:
            import ui.main_window
            print(f"{check} ui.main_window imported successfully")
            
            import ui.character_widget
            print(f"{check} ui.character_widget imported successfully")
        except ImportError as e:
            print(f"{warn} UI imports failed (expected in headless environment): {e}")
            # This is okay in CI environment
            return True
        
        print("\n[SUCCESS] All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n{fail} Import failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 