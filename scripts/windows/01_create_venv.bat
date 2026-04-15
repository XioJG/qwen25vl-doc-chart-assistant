@echo off
setlocal

if not exist .venv (
    python -m venv .venv
)

call .venv\Scriptsctivate

echo [OK] virtual environment created and activated.
python --version
