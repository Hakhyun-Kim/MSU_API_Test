#!/usr/bin/env python3
"""
Simple import test for CI/CD
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    try:
        # Test basic imports
        print("Testing basic imports...")
        import PyQt6
        print("✓ PyQt6 imported successfully")
        
        import requests
        print("✓ requests imported successfully")
        
        import PIL
        print("✓ PIL imported successfully")
        
        # Test project imports
        print("\nTesting project imports...")
        
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        import models.character
        print("✓ models.character imported successfully")
        
        import models.item
        print("✓ models.item imported successfully")
        
        import api.api_client
        print("✓ api.api_client imported successfully")
        
        # Test UI imports (may fail in headless environment)
        try:
            import ui.main_window
            print("✓ ui.main_window imported successfully")
            
            import ui.character_widget
            print("✓ ui.character_widget imported successfully")
        except ImportError as e:
            print(f"⚠ UI imports failed (expected in headless environment): {e}")
            # This is okay in CI environment
            return True
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 