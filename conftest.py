from __future__ import annotations

from datetime import datetime

import pytest

from core.config_loader import PROJECT_ROOT, load_config
from core.driver_factory import create_driver
from pages.screen_page import ScreenPage
from utils.permissions import skip_all_dialogs


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture
def driver(config):
    driver = create_driver(config)
    dialogs = config.get("dialogs", {})
    if dialogs.get("skip_all", True):
        skip_all_dialogs(driver, rounds=int(dialogs.get("rounds", 10)))
    yield driver
    try:
        driver.quit()
    except Exception:
        pass


@pytest.fixture
def screen_page(driver, config):
    timeout = config.get("waits", {}).get("explicit_seconds", 20)
    return ScreenPage(driver, timeout=timeout)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    screenshots = PROJECT_ROOT / "reports" / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = screenshots / f"{item.name}_{stamp}.png"
    try:
        driver.get_screenshot_as_file(str(path))
        print(f"\nScreenshot saved: {path}")
    except Exception as exc:
        print(f"\nFailed to save screenshot: {exc}")
