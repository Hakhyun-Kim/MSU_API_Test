#!/usr/bin/env python3
"""
Helper script to create a new release
"""

import subprocess
import sys
import re
from datetime import datetime

def get_current_version():
    """Get current version from CHANGELOG"""
    try:
        with open('CHANGELOG.md', 'r') as f:
            content = f.read()
            # Find version pattern like [1.0.0]
            match = re.search(r'\[(\d+\.\d+\.\d+)\]', content)
            if match:
                return match.group(1)
    except:
        pass
    return "1.0.0"

def increment_version(version, bump_type='patch'):
    """Increment version number"""
    major, minor, patch = map(int, version.split('.'))
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

def main():
    print("MSU API Test - Release Creator")
    print("=" * 50)
    
    # Get current version
    current_version = get_current_version()
    print(f"Current version: v{current_version}")
    
    # Ask for version bump type
    print("\nSelect version bump type:")
    print("1. Patch (bug fixes)")
    print("2. Minor (new features)")
    print("3. Major (breaking changes)")
    choice = input("Choice (1-3): ").strip()
    
    bump_type = 'patch'
    if choice == '2':
        bump_type = 'minor'
    elif choice == '3':
        bump_type = 'major'
    
    new_version = increment_version(current_version, bump_type)
    print(f"\nNew version will be: v{new_version}")
    
    # Get release notes
    print("\nEnter release notes (press Enter twice to finish):")
    release_notes = []
    while True:
        line = input()
        if line:
            release_notes.append(line)
        else:
            if release_notes:
                break
    
    release_message = '\n'.join(release_notes)
    
    # Confirm
    print("\n" + "=" * 50)
    print(f"Version: v{new_version}")
    print(f"Release notes:\n{release_message}")
    print("=" * 50)
    
    confirm = input("\nProceed with release? (y/n): ").lower()
    if confirm != 'y':
        print("Release cancelled.")
        return
    
    # Create and push tag
    try:
        print("\nCreating release...")
        
        # Commit any pending changes
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Release v{new_version}'], check=False)
        
        # Create tag
        tag_message = f"Release v{new_version}\n\n{release_message}"
        subprocess.run(['git', 'tag', '-a', f'v{new_version}', '-m', tag_message], check=True)
        
        # Push changes and tags
        subprocess.run(['git', 'push'], check=True)
        subprocess.run(['git', 'push', 'origin', f'v{new_version}'], check=True)
        
        print(f"\n✅ Release v{new_version} created successfully!")
        print("GitHub Actions will now build and publish the release.")
        print(f"Check progress at: https://github.com/Hakhyun-Kim/MSU_API_Test/actions")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error creating release: {e}")
        print("Make sure you have git configured and are in the project directory.")

if __name__ == "__main__":
    main() 