"""
Catalog
"""
from selenium.webdriver.common.by import By
from tests.pom.base_app import BasePage


class CatalogLocators:
    """
    Locators for catalog
    """
    FILTER = (By.CSS_SELECTOR, '[class*="toggle-filters catalog-toolbar-item"]')

class Catalog(BasePage):
    """
    Class for catalog
    """
    def filter_click(self):
        """
        Filter click
        """
        search_field = self.find_element(CatalogLocators.FILTER)
        search_field.click()
