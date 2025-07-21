# 🚀 Quick Release Guide

## The Easiest Way to Create a Release (30 seconds!)

### Step 1: Update Repository Settings (One-time setup)
1. Go to: https://github.com/Hakhyun-Kim/MSU_API_Test/settings/actions
2. Under "Workflow permissions", select **"Read and write permissions"**
3. Click **Save**

### Step 2: Create Your Release
1. Go to: https://github.com/Hakhyun-Kim/MSU_API_Test/actions/workflows/push-button-release.yml
2. Click the **"Run workflow"** button (on the right)
3. Fill in:
   - Version: `1.0.0` (or any version like `1.0.1`, `2.0.0`)
   - Release notes: `Initial release with mock data support`
4. Click the green **"Run workflow"** button

### Step 3: Wait for Magic! ✨
- The workflow will create the release
- Then automatically build executables for:
  - 🪟 Windows (.exe)
  - 🍎 macOS
  - 🐧 Linux

### Step 4: Download Your App
After 5-10 minutes:
1. Go to: https://github.com/Hakhyun-Kim/MSU_API_Test/releases
2. Download the version for your OS
3. Run and enjoy!

## That's it! 🎉

No command line needed, no complex setup. Just click and release!

---

## Alternative: Command Line Release

If you prefer using the terminal:
```bash
# First time only - update your local copy
git pull

# Create release
py create_release.py
```

Follow the prompts and it will handle everything! 