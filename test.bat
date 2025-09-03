@echo off
echo Testing Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python is not in your PATH or not installed.
    pause
    exit /b 1
)

echo.
echo Testing Python script execution...
python -c "print('Python is working!')"

if %errorlevel% neq 0 (
    echo Failed to run Python script.
    pause
    exit /b 1
)

echo.
echo Testing complete!
pause
