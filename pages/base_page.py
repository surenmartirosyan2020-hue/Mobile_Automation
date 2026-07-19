from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    def __init__(self, driver, timeout: int = 5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by, locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.presence_of_element_located((by, locator))
        )

    def find_clickable(self, by, locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.element_to_be_clickable((by, locator))
        )

    def click(self, by, locator, timeout: int | None = None):
        self.find_clickable(by, locator, timeout).click()

    def is_displayed(self, by, locator, timeout: int | None = None) -> bool:
        try:
            return self.find(by, locator, timeout).is_displayed()
        except TimeoutException:
            return False

    def w3c_tap(self, by, locator, timeout: int | None = None) -> None:
        element = self.find_clickable(by, locator, timeout)
        rect = element.rect
        x = int(rect["x"] + rect["width"] / 2)
        y = int(rect["y"] + rect["height"] / 2)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def w3c_swipe(self, start_x, start_y, end_x, end_y, duration_ms: int = 800) -> None:
        # Must reuse the same PointerInput — Appium W3C pattern
        touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)
        actions.w3c_actions.pointer_action.move_to_location(int(start_x), int(start_y))
        actions.w3c_actions.pointer_action.pointer_down()
        if duration_ms > 0:
            actions.w3c_actions = ActionBuilder(
                self.driver, mouse=touch_input, duration=duration_ms
            )
        actions.w3c_actions.pointer_action.move_to_location(int(end_x), int(end_y))
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_up(self, duration_ms: int = 800) -> None:
        size = self.driver.get_window_size()
        self.w3c_swipe(
            size["width"] * 0.5,
            size["height"] * 0.75,
            size["width"] * 0.5,
            size["height"] * 0.25,
            duration_ms,
        )

    def scroll_to_element(self, locator, max_scrolls=10):
        for _ in range(max_scrolls):
            try:
                return self.driver.find_element(*locator)
            except NoSuchElementException:
                self.swipe_up()

        raise Exception(f"Element not found after scrolling: {locator}")
