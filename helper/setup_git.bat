@echo off
echo Setting up Git repository for a2asys...
echo.

REM Navigate to the current directory
cd /d "%~dp0"

REM Initialize git repository
echo Initializing git repository...
git init
if %errorlevel% neq 0 (
    echo Error: Failed to initialize git repository
    pause
    exit /b 1
)

REM Add remote origin
echo Adding remote origin...
git remote add origin https://github.com/SawsanAbdulbari/a2asys.git
if %errorlevel% neq 0 (
    echo Error: Failed to add remote origin
    pause
    exit /b 1
)

REM Add all files to staging
echo Adding files to staging...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files
    pause
    exit /b 1
)

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit - A2A SaaS System"
if %errorlevel% neq 0 (
    echo Error: Failed to create commit
    pause
    exit /b 1
)

REM Set main branch as default
echo Setting main branch...
git branch -M main
if %errorlevel% neq 0 (
    echo Warning: Failed to rename branch to main
)

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo Error: Failed to push to GitHub
    echo Please check your GitHub credentials and try again
    pause
    exit /b 1
)

echo.
echo ✅ Successfully connected local directory to GitHub repository!
echo Repository URL: https://github.com/SawsanAbdulbari/a2asys
echo.
pause
