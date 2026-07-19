# Mobile Automation (Appium + Pytest + POM)

Android UI automation for Sauce Labs My Demo App.

---

## Prerequisites (install once)

1. **Python 3.12+**  
   https://www.python.org/downloads/  
   During install, check **Add Python to PATH**.

2. **Node.js (LTS)**  
   https://nodejs.org/  
   Needed for Appium server.

3. **Android Studio**  
   https://developer.android.com/studio  
   - Install Android SDK  
   - Create an emulator (AVD), e.g. Pixel with API 35 / Android 15  
   - Note your SDK path (usually):  
     `C:\Users\<you>\AppData\Local\Android\Sdk`

4. **Environment variables (Windows)**  
   Add to System Environment Variables:

   | Variable | Value |
   |----------|--------|
   | `ANDROID_HOME` | `C:\Users\<you>\AppData\Local\Android\Sdk` |
   | Path | `%ANDROID_HOME%\platform-tools` |
   | Path | `%ANDROID_HOME%\emulator` |

   Open a **new** PowerShell and check:

   ```powershell
   adb version
   ```

5. **Appium 2 + UiAutomator2 driver**

   ```powershell
   npm install -g appium
   appium driver install uiautomator2
   appium -v
   appium driver list
   ```

---

## Project setup (from 0)

### 1. Open project

```powershell
cd C:\Users\suren_ma\Downloads\pythonProject1
```

### 2. Create virtual environment and install packages

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Put the APK in `apps/`

Download My Demo App APK:

https://github.com/saucelabs/my-demo-app-android/releases/download/2.2.0/mda-2.2.0-25.apk

Save as:

```text
apps\mda-2.2.0-25.apk
```

### 4. Configure `config/config.yaml`

Option A — edit manually:

```yaml
app:
  path: "apps/mda-2.2.0-25.apk"
  package: "com.saucelabs.mydemoapp.android"
  activity: "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"

device:
  name: "emulator-5554"
  platform_version: "15"
```

Option B — auto-fill from APK:

```powershell
python -m utils.setup_app apps\mda-2.2.0-25.apk --device emulator-5554 --platform 15
```

Update `device.name` / `platform_version` to match your emulator (`adb devices`).

---

## Run automation

### 1. Start Android emulator

Android Studio → Device Manager → Play  
Or:

```powershell
emulator -list-avds
emulator -avd <your_avd_name>
```

Check device:

```powershell
adb devices
```

You should see something like `emulator-5554 device`.

### 2. Start Appium server (keep this terminal open)

```powershell
appium --port 4725
```

Leave it running. URL used by tests: `http://127.0.0.1:4725`

### 3. Run tests (new terminal)

```powershell
cd C:\Users\suren_ma\Downloads\pythonProject1
.\.venv\Scripts\Activate.ps1
pytest tests/ -v -s
```

### Run one test

```powershell
pytest tests/test_screen.py::test_tap_sort -v -s
pytest tests/test_screen.py::test_w3c_sort_and_scroll -v -s
```

### Run from PyCharm

1. Open the project folder  
2. Set interpreter to `.venv`  
3. Right-click `tests/test_screen.py` → **Run**  
4. Emulator + Appium must already be running

---

## What the tests do

| Test | Flow |
|------|------|
| `test_tap_sort` | Open catalog → tap Sort → sort by price → scroll to turquoise T-Shirt |
| `test_w3c_sort_and_scroll` | Same flow using W3C Actions for taps/swipe |

On failure, screenshots are saved to `reports/screenshots/`.

---

## Project structure

```text
apps/                 APK files
config/config.yaml    app / device / appium settings
core/                 driver factory, config loader
pages/
  base_page.py        waits, click, W3C tap/swipe, scroll
  screen_page.py      locators + page actions (POM)
tests/
  test_screen.py      test cases
utils/                APK setup helper, permission dialogs
reports/screenshots/  failure screenshots
```

---

## How POM works

- **Page** (`screen_page.py`) — locators + actions (`tap_sort`, `scroll_to_fourth_product`)  
- **Test** (`test_screen.py`) — steps + asserts only  
- **BasePage** — shared waits / click / W3C gestures  
- **config.yaml** — APK, package, activity, device  

Do not put locators inside test files.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `adb devices` empty | Start emulator; check USB debugging / restart `adb kill-server` then `adb start-server` |
| Session not created | Appium running on `4725`? Device name matches config? |
| APK not found | Check `apps/mda-2.2.0-25.apk` exists; path in `config.yaml` |
| Element not found | Open Appium Inspector; update locators in `pages/screen_page.py` |
| W3C actions error | Use latest `uiautomator2` driver: `appium driver update uiautomator2` |
| Permission / Skip popup | Already handled by `dialogs.skip_all` in config |

---

## Quick checklist before every run

1. Emulator is ON (`adb devices` shows device)  
2. Appium is ON (`appium --port 4725`)  
3. Venv is activated  
4. APK path in `config.yaml` is correct  
5. `pytest tests/ -v -s`
