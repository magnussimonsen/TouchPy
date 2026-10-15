# Building TouchPy to an Executable

## Quick Build (Windows)

Run the build script:

```powershell
.\build.ps1
```

This will:

1. Install PyInstaller if needed
2. Build the executable
3. Create `dist\TouchPy.exe`

## Manual Build

If you prefer to build manually:

1. **Install PyInstaller:**

   ```bash
   pip install -r requirements-build.txt
   ```

2. **Build the executable:**

   ```bash
   pyinstaller --clean --noconfirm TouchPy.spec
   ```

3. **Find your executable:**
   ```
   dist\TouchPy.exe
   ```

## Distribution

To distribute your app:

1. Copy `dist\TouchPy.exe`
2. Share it with others
3. Users can run `TouchPy.exe` directly (no Python installation needed!)

### Adding Custom Exercises After Build

Users can add their own exercises **without rebuilding**:

1. Create an `exercises` folder next to `TouchPy.exe`:

   ```
   dist\
   ├── TouchPy.exe
   └── exercises\          ← Create this folder
       └── 018_custom.txt
   ```

2. Add `.txt` files with format:
   - Line 1: Exercise title
   - Rest: Exercise text

See [EXERCISES_README.md](EXERCISES_README.md) for detailed instructions.

## Customization

### Add an Icon

1. Create or download a `.ico` file
2. Edit `TouchPy.spec` and change:
   ```python
   icon=None,  # Change to icon='your_icon.ico'
   ```

### Single-File Executable

The current `TouchPy.spec` already builds a single-file executable at
`dist\TouchPy.exe`. No additional configuration is needed.

## Troubleshooting

### Build fails with import errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try deleting `build` and `dist` folders, then rebuild

### Executable is too large

- This is normal for Python apps (~50-100MB)
- PyInstaller bundles Python and all dependencies
- Use UPX compression (enabled by default with `upx=True`)

### Antivirus flags the exe

- This is a false positive (common with PyInstaller)
- Add an exception in your antivirus
- Or sign the executable with a code signing certificate

## File Size Expectations

- The `.exe` will be approximately 50-100 MB
- This includes Python interpreter, Textual, Rich, and all dependencies
- The exercises folder will be bundled inside

## Notes

- The built executable includes everything needed to run
- No Python installation required on target machines
- Built-in exercise files are bundled into the executable
- Users can still add custom exercises by placing `.txt` files in an `exercises` folder next to the `.exe`
