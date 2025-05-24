@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  A2A SaaS System - Git Repository Setup
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

REM Navigate to script directory
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Initialize git repository
echo 📁 Initializing git repository...
git init
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize git repository
    pause
    exit /b 1
)
echo ✅ Git repository initialized
echo.

REM Set default branch to main
echo 🌿 Setting default branch to main...
git branch -M main
echo ✅ Default branch set to main
echo.

REM Add remote origin
echo 🔗 Adding remote origin...
git remote add origin https://github.com/SawsanAbdulbari/a2asys.git
if %errorlevel% neq 0 (
    echo ❌ Failed to add remote origin
    echo This might be because the remote already exists
    echo Trying to set the URL instead...
    git remote set-url origin https://github.com/SawsanAbdulbari/a2asys.git
    if !errorlevel! neq 0 (
        echo ❌ Failed to set remote URL
        pause
        exit /b 1
    )
)
echo ✅ Remote origin configured
echo.

REM Show current status
echo 📊 Current git status:
echo.
git status
echo.

REM Add all files to staging
echo 📋 Adding files to staging area...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files to staging
    pause
    exit /b 1
)
echo ✅ Files added to staging
echo.

REM Show what will be committed
echo 📄 Files to be committed:
git status --short
echo.

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "Initial commit: Reddit Scout Agent - A2A SaaS System

- Added Reddit scout agent implementation
- Configured Python virtual environment
- Added comprehensive documentation
- Set up environment variables structure
- Included VS Code development setup"

if %errorlevel% neq 0 (
    echo ❌ Failed to create commit
    echo This might be because:
    echo 1. No changes to commit
    echo 2. Git user name/email not configured
    echo.
    echo Checking git configuration...
    git config user.name
    git config user.email
    echo.
    echo If empty, please configure:
    echo git config --global user.name "Your Name"
    echo git config --global user.email "your.email@example.com"
    pause
    exit /b 1
)
echo ✅ Initial commit created
echo.

REM Show commit information
echo 📝 Commit details:
git log --oneline -1
echo.

REM Push to GitHub
echo 🚀 Pushing to GitHub...
echo This may require authentication...
echo.
git push -u origin main
if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub
    echo.
    echo This could be due to:
    echo 1. Authentication required (GitHub username/password or token)
    echo 2. Network connectivity issues
    echo 3. Repository permissions
    echo.
    echo Please try pushing manually:
    echo git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ SUCCESS! Repository setup complete!
echo ========================================
echo.
echo 🌐 Repository URL: https://github.com/SawsanAbdulbari/a2asys
echo 📁 Local directory: %CD%
echo 🌿 Branch: main
echo.
echo Next steps:
echo 1. Your code is now on GitHub
echo 2. You can make changes and commit with:
echo    git add .
echo    git commit -m "Your commit message"
echo    git push
echo.
echo 3. Clone elsewhere with:
echo    git clone https://github.com/SawsanAbdulbari/a2asys.git
echo.
pause
