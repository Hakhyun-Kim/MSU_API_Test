#!/usr/bin/env python3
"""
Trigger build workflow for an existing release
"""

import subprocess
import webbrowser

print("MSU API Test - Build for Existing Release")
print("=" * 50)
print()
print("Since you already created a release, you need to trigger the build workflow.")
print()
print("Option 1: Automatic (via GitHub website)")
print("-" * 50)
print("1. Open this link:")
print("   https://github.com/Hakhyun-Kim/MSU_API_Test/actions/workflows/build-release.yml")
print()
print("2. Click 'Run workflow'")
print("3. Leave the branch as 'main'")
print("4. Click 'Run workflow'")
print()
input("Press Enter to open the link in your browser...")
webbrowser.open("https://github.com/Hakhyun-Kim/MSU_API_Test/actions/workflows/build-release.yml")

print()
print("Option 2: Check if builds are already running")
print("-" * 50)
print("Check here: https://github.com/Hakhyun-Kim/MSU_API_Test/actions")
print()
print("The build process takes about 10-15 minutes to complete.")
print("Once done, the executables will be automatically added to your release!")
print()
print("Your release page: https://github.com/Hakhyun-Kim/MSU_API_Test/releases") 