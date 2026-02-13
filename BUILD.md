# Building TouchPy to an Executable

## Quick Build (Windows)

Run the build script:

```powershell
.\build.ps1
```

This will:

1. Install PyInstaller if needed
2. Build the executable
3. Create `dist\TouchPy\TouchPy.exe`

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
   dist\TouchPy\TouchPy.exe
   ```

## Distribution

To distribute your app:

1. Copy the entire `dist\TouchPy` folder
2. Share it with others
3. Users can run `TouchPy.exe` directly (no Python installation needed!)

## Customization

### Add an Icon

1. Create or download a `.ico` file
2. Edit `TouchPy.spec` and change:
   ```python
   icon=None,  # Change to icon='your_icon.ico'
   ```

### Create a Single-File Executable

Edit `TouchPy.spec` and change the `EXE` section:

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,      # Add this
    a.datas,         # Add this
    [],
    name='TouchPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Then remove the `COLLECT` section at the bottom.

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
- Exercise files are bundled into the executable
- Users can still add custom exercises by placing `.txt` files in an `exercises` folder next to the `.exe`
