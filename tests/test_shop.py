"""
Test shop
"""
import pytest

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pom.catalog import Catalog
from tests.helper.common import InputHelper


URL = 'https://test-shop.qa.studio/'

@pytest.mark.slow
class TestSmoke:
    """
    Basic tests
    """

    @pytest.mark.xfail(reason="Wait for fix bug №45678")
    def test_header_menu(self, browser):
        """
        Test case 23:
        [SHOP][MAIN] Проверка меню
        """
        expected_list = ['Каталог', 'Часто задаваемые вопросы', 'Блог', 'О компании', 'Контакты']

        logger.info("Start test")
        main_page = Catalog(browser)
        main_page.go_to_site()
        items = main_page.get_top_menu()

        assert items == expected_list, 'Unexpected menu list'

        browser.get(URL)
        elements = browser.find_elements(by=By.CSS_SELECTOR, value="[id='menu-top'] li a")

        result_list = []
        for element in elements:
            result_list.append(element.text)

        assert expected_list == result_list, 'Unexpected menu list'

    def test_click_top_menu(self, browser, clear_report):
        """
        Click all item in top menu
        """
        logger.info("Start test")
        main_page = Catalog(browser)
        main_page.go_to_site()

        logger.warning("Go to FAQ page")
        main_page.go_to_faq()
        assert main_page.get_current_url() == 'https://test-shop.qa.studio//faq/'


    def test_count_of_all_products(self, browser):
        """
        WRT-2 Count of all product
        """
        browser.get(URL)

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "current-post"), "17"))

        elements = browser.find_elements(by=By.CSS_SELECTOR, value="[id='rz-shop-content'] ul li")

        assert len(elements) == 17, "Unexpected count of products"

    def test_right_way(self, browser):
        """
        Right way
        """
        browser.get(URL)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "current-post"), "17"))

        product = browser.find_element(by=By.CSS_SELECTOR, value="[data-product_sku='4XAVRC35']")
        product.click()

        WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located(
            (By.ID, "cart-modal")))

        cart_is_visible = browser.find_element(By.XPATH, value="//div[@id='cart-modal']").value_of_css_property("display")
        assert cart_is_visible == "block", "Unexpected state of cart"

        browser.find_element(by=By.CSS_SELECTOR, value="a.button.checkout").click()
        WebDriverWait(browser, timeout=5, poll_frequency=1).until(
            EC.url_to_be("https://testqastudio.me/checkout/"))

        input_field = browser.find_element(By.ID, value="billing_first_name")
        input_field.click()
        input_field.send_keys("Andrey")


        input_helper = InputHelper(browser)
        input_helper.enter_input(input_id="billing_first_name", data="Andrey")
        input_helper.enter_input(input_id="billing_last_name", data="Ivanov")
        input_helper.enter_input(input_id="billing_address_1", data="2-26, Sadovaya street")
        input_helper.enter_input(input_id="billing_city", data="Moscow")
        input_helper.enter_input(input_id="billing_state", data="Moscow")
        input_helper.enter_input(input_id="billing_postcode", data="122457")
        input_helper.enter_input(input_id="billing_phone", data="+79995784256")
        input_helper.enter_input(input_id="billing_email", data="andrey.i@mail.ru")

        WebDriverWait(browser, timeout=5, poll_frequency=1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="payment"] [contains(@style, "position: static; zoom: 1;")]')))
        browser.find_element(by=By.ID, value="place_order").click()

        WebDriverWait(browser, timeout=5, poll_frequency=1).until(
            EC.url_contains("https://test-shop.qa.studio/checkout/order-received/"))

        result = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "p.woocommerce-thankyou-order-received"), "Ваш заказ принят. Благодарим вас."))

        assert result, 'Unexpected notification text'
