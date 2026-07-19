from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class ScreenPage(BasePage):
    SORT_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Shows current sorting order and displays available sorting options",
    )
    SORT_PRICE_ASC = (
        AppiumBy.ACCESSIBILITY_ID,
        "Displays ascending sorting order by price",
    )
    PRODUCT_IMAGE_4 = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Test.allTheThings() T-Shirt (turquoise)")',
    )

    def wait_until_loaded(self, timeout: int = 25) -> None:
        assert self.is_displayed(*self.SORT_BUTTON, timeout=timeout), (
            "Sort button not found on catalog screen"
        )

    def tap_sort(self) -> None:
        self.click(*self.SORT_BUTTON)

    def tap_sort_w3c(self) -> None:
        self.w3c_tap(*self.SORT_BUTTON)

    def tap_sort_by_price(self) -> None:
        self.click(*self.SORT_PRICE_ASC)

    def tap_sort_by_price_w3c(self) -> None:
        self.w3c_tap(*self.SORT_PRICE_ASC)

    def scroll_to_fourth_product(self):
        return self.scroll_to_element(self.PRODUCT_IMAGE_4)

    def is_product_visible(self, timeout: int = 10) -> bool:
        return self.is_displayed(*self.PRODUCT_IMAGE_4, timeout=timeout)
