# Mobile Automation (Appium + Pytest)

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Config

Edit `config/config.yaml` (APK path, package, activity, device).

```powershell
python -m utils.setup_app apps/mda-2.2.0-25.apk --device emulator-5554 --platform 15
```

## Run

```powershell
appium --port 4725
pytest tests/ -v -s
```

## Structure

```text
config/     config.yaml
core/       driver + config loader
pages/      page objects
tests/      pytest cases
utils/      apk helpers, dialogs
apps/       apk files
```
