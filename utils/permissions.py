from __future__ import annotations

import time

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

GRANT_SELECTORS = [
    (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
    (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button"),
    (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
    (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
]

SKIP_SELECTORS = [
    (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button"),
    (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button"),
    (AppiumBy.ACCESSIBILITY_ID, "Close"),
    (AppiumBy.ACCESSIBILITY_ID, "Navigate up"),
    (AppiumBy.XPATH, "//*[@content-desc='Close' or @content-desc='close']"),
    (
        AppiumBy.XPATH,
        "//*["
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'skip') or "
        "contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'skip') or "
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'not now') or "
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'no thanks') or "
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'maybe later') or "
        "(@text='Allow' or @content-desc='Allow') or "
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'while using') or "
        "contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'only this time')]"
    ),
]


def _click_first(driver: WebDriver, selectors: list, timeout: float) -> bool:
    for by, locator in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            return True
        except Exception:
            continue
    return False


def skip_all_dialogs(driver: WebDriver, rounds: int = 10, timeout: float = 1.2) -> None:
    for _ in range(rounds):
        clicked = _click_first(driver, GRANT_SELECTORS, timeout)
        if not clicked:
            clicked = _click_first(driver, SKIP_SELECTORS, timeout)
        if not clicked:
            break
        time.sleep(0.25)
