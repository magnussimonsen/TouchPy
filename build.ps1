# Build script for creating TouchPy.exe
# Run this script to build the Windows executable

Write-Host "=== TouchPy Build Script ===" -ForegroundColor Green
Write-Host ""

# Check if pyinstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
        pip install -r requirements-build.txt
    } else {
        Write-Host "PyInstaller is already installed." -ForegroundColor Green
    }
} catch {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install -r requirements-build.txt
}

Write-Host ""
Write-Host "Building TouchPy.exe..." -ForegroundColor Yellow
Write-Host ""

# Run PyInstaller
pyinstaller --clean --noconfirm TouchPy.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Build Complete! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your executable is located at:" -ForegroundColor Cyan
    Write-Host "  dist\TouchPy\TouchPy.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "To run the app:" -ForegroundColor Yellow
    Write-Host "  cd dist\TouchPy" -ForegroundColor White
    Write-Host "  .\TouchPy.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "You can distribute the entire 'dist\TouchPy' folder." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "Build failed! Check the error messages above." -ForegroundColor Red
}
