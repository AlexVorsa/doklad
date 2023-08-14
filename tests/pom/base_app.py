"""
POM base page
"""
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TMLocators:
    """
    Class for locators
    """
    # top menu item
    TM_CATALOG = (By.CSS_SELECTOR, '#page [class*="menu-item-11001"]')
    TM_FAQ = (By.CSS_SELECTOR, '#page [class*="menu-item-11088"]')
    TM_BLOG = (By.CSS_SELECTOR, '#page [class*="menu-item-11002"]')
    TM_ABOUT = (By.CSS_SELECTOR, '#page [class*="menu-item-11003"]')
    TM_CONTACTS = (By.CSS_SELECTOR, '#page [class*="menu-item-11005"]')

    # basic locator for top menu
    TM = (By.CSS_SELECTOR, '[id="menu-top"] li a')


class BasePage:
    """
    Base page
    """
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://testqastudio.me"

    def find_element(self, locator, time=10):
        """
        Find element with waiting
        """
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                    message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        """
        Find elements with waiting
        """
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                    message=f"Can't find elements by locator {locator}")

    def go_to_site(self):
        """
        Get base URL
        """
        return self.driver.get(self.base_url)

    def go_to_catalog(self):
        """
        Go to catalog
        """
        self.find_element(locator=TMLocators.TM_CATALOG).click()

    def go_to_faq(self):
        """
        Go to FAQ
        """
        logger.info('Find element')
        self.find_element(locator=TMLocators.TM_FAQ).click()
        logger.info('Wait for page')
        WebDriverWait(self.driver, timeout=5, poll_frequency=1).until(EC.url_to_be(f"{self.base_url}/faq/"))

    def get_current_url(self):
        """
        Get current url
        """
        return self.driver.current_url

    def get_top_menu(self) -> list:
        """
        Get top menu item
        """
        elements = self.find_elements(locator=TMLocators.TM)

        result_list = []
        for element in elements:
            result_list.append(element.text)

        return result_list
