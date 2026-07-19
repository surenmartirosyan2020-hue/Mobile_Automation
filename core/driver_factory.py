from __future__ import annotations

from typing import Any

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver


def create_driver(config: dict[str, Any]) -> WebDriver:
    app = config["app"]
    device = config["device"]
    appium_cfg = config["appium"]

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = device["name"]
    options.platform_version = str(device["platform_version"])
    options.app = app["path"]
    options.app_package = app["package"]
    options.app_activity = app["activity"]
    options.auto_grant_permissions = bool(
        appium_cfg.get("auto_grant_permissions", True)
    )
    options.set_capability(
        "appium:newCommandTimeout",
        appium_cfg.get("new_command_timeout", 300),
    )
    options.set_capability(
        "appium:uiautomator2ServerLaunchTimeout",
        appium_cfg.get("uiautomator2_server_launch_timeout", 120000),
    )
    options.set_capability(
        "appium:uiautomator2ServerInstallTimeout",
        appium_cfg.get("uiautomator2_server_install_timeout", 120000),
    )
    options.set_capability(
        "appium:adbExecTimeout",
        appium_cfg.get("adb_exec_timeout", 120000),
    )

    return webdriver.Remote(
        command_executor=appium_cfg.get("url", "http://127.0.0.1:4725"),
        options=options,
    )
