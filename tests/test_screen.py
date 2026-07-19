def test_tap_sort(screen_page):
    screen_page.wait_until_loaded()
    screen_page.tap_sort()
    screen_page.tap_sort_by_price()
    screen_page.scroll_to_fourth_product()
    assert screen_page.is_product_visible()


def test_w3c_sort_and_scroll(screen_page):
    screen_page.wait_until_loaded()
    screen_page.tap_sort_w3c()
    screen_page.tap_sort_by_price_w3c()
    screen_page.scroll_to_fourth_product()
    assert screen_page.is_product_visible()
