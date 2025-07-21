# Setting Up Automatic Releases

## Quick Fix for Permission Error

If you're getting a "Permission denied" error when creating releases, follow these steps:

### 1. Update Repository Settings

1. Go to your repository: https://github.com/Hakhyun-Kim/MSU_API_Test
2. Click on **Settings** (top menu)
3. Click on **Actions** → **General** (left sidebar)
4. Scroll down to **Workflow permissions**
5. Select **"Read and write permissions"**
6. Check **"Allow GitHub Actions to create and approve pull requests"**
7. Click **Save**

### 2. Create Your First Release

Now you can create releases using any of these methods:

#### Option A: Push Button Release (Easiest)
1. Go to [Actions](https://github.com/Hakhyun-Kim/MSU_API_Test/actions)
2. Click on **"Push Button Release"**
3. Click **"Run workflow"**
4. Enter version: `1.0.0`
5. Enter release notes: `Initial release`
6. Click green **"Run workflow"** button

#### Option B: Command Line
```bash
py create_release.py
```

#### Option C: Auto Release
Just push a commit with a proper message:
```bash
git commit -m "feat: initial release"
git push
```

### 3. Monitor the Release

1. Check [Actions tab](https://github.com/Hakhyun-Kim/MSU_API_Test/actions) to see the progress
2. Once complete, check [Releases page](https://github.com/Hakhyun-Kim/MSU_API_Test/releases)
3. Download links will appear automatically!

## Troubleshooting

### Still getting permission errors?

Try these alternatives:

1. **Use a Personal Access Token (PAT)**:
   - Go to Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` scope
   - Add it as a repository secret named `RELEASE_TOKEN`
   - Update workflows to use `${{ secrets.RELEASE_TOKEN }}` instead of `${{ secrets.GITHUB_TOKEN }}`

2. **Manual Release**:
   - Create tag locally: `git tag -a v1.0.0 -m "Release v1.0.0"`
   - Push tag: `git push origin v1.0.0`
   - GitHub Actions will build the executables

## Success! 🎉

Once set up correctly, every push to main will automatically:
- Determine the version
- Create a release
- Build executables for all platforms
- Upload them to GitHub Releases 