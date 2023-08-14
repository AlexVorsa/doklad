# импортируем модули и отдельные классы
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# каждый тест должен начинаться с test_
def test_zvuk():
    """
    Test case WERT-1
    """
		# Описываем опции запуска браузера
    chrome_options = Options()
    chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    # chrome_options.add_argument("--headless") # спец. режим "без браузера"

		# устанавливаем webdriver в соответствии с версией используемого браузера
    service = Service()
    # запускаем браузер с указанными выше настройками
    driver = webdriver.Chrome(service=service, options=chrome_options)
		# определяем адрес страницы для теста и переходим на неё
    url = "https://career.zvuk.com"
    driver.get(url=url)

    x_path_table = '//*[@id="rec473279205"]/div/div/div[5]/a'
    element = driver.find_element(by=By.XPATH, value=x_path_table)
    # element.click()
    driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, timeout=10, poll_frequency=1).until(
        EC.url_to_be("https://career.zvuk.com/vacancies")) # ждем загрузки страницы

    driver.execute_script("window.scrollTo(0, 300);") # скролим страницы на 300 поинтов

    backend_dev = '//*[@id="rec471265435"]/div[1]/div/div[4]/div[1]/div/div/div/a/div/div[1]'
    WebDriverWait(driver, timeout=10, poll_frequency=2).until(
        EC.visibility_of_element_located((By.XPATH, backend_dev))) # ждем когда прогрузятся плиточки с вакансиями

    element = driver.find_element(by=By.XPATH, value=backend_dev)
    driver.execute_script("arguments[0].click();", element)

    assert True, ''
