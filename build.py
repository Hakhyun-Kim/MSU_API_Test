#!/usr/bin/env python3
"""
Build script for MSU API Test application
"""

import os
import sys
import subprocess
import shutil
import platform

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}")
    
    # Clean .spec file if it exists
    if os.path.exists('MSU_API_Test.spec'):
        os.remove('MSU_API_Test.spec')
        print("Cleaned MSU_API_Test.spec")

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)

def build_executable():
    """Build the executable using PyInstaller"""
    print(f"Building executable for {platform.system()}...")
    
    # Create PyInstaller command
    cmd = [
        'pyinstaller',
        '--windowed',
        '--onefile',
        '--name', 'MSU_API_Test',
        '--clean',
        'main.py'
    ]
    
    # Run PyInstaller
    subprocess.run(cmd, check=True)
    
    print("Build complete!")
    print(f"Executable located at: dist/MSU_API_Test{'.exe' if platform.system() == 'Windows' else ''}")

def main():
    """Main build process"""
    print("MSU API Test Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("Error: main.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    response = input("Clean previous builds? (y/n): ").lower()
    if response == 'y':
        clean_build()
    
    # Install requirements
    response = input("Install/update requirements? (y/n): ").lower()
    if response == 'y':
        install_requirements()
    
    # Build executable
    build_executable()

if __name__ == "__main__":
    main() 