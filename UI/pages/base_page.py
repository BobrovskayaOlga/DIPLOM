from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, selector):
        """Найти элемент по CSS селектору"""
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def click(self, selector):
        """Кликнуть по элементу"""
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        element.click()

    def type(self, selector, text):
        """Ввести текст"""
        element = self.find(selector)
        element.clear()
        element.send_keys(text)

    def is_visible(self, selector):
        """Проверить видимость элемента"""
        try:
            element = self.find(selector)
            return element.is_displayed()
        except:
            return False


class MainPage(BasePage):
    
    def accept_cookies(self):
        """Принять куки если есть"""
        try:
            self.click(".cookie-notice__accept")
            time.sleep(1)  # Даем время закрыться
        except:
            pass

    def search(self, query):
        """Выполнить поиск"""
        # Пробуем разные селекторы поиска
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='поиск']",
            ".search-form input",
            "input[name='q']"
        ]
        
        for selector in search_selectors:
            try:
                self.type(selector, query)
                # Пробуем найти кнопку поиска
                button_selectors = [
                    "button[type='submit']",
                    ".search-form button", 
                    ".search-btn",
                    "input[type='submit']"
                ]
                for btn_selector in button_selectors:
                    try:
                        self.click(btn_selector)
                        time.sleep(2)  # Ждем загрузки результатов
                        return
                    except:
                        continue
            except:
                continue
        
        # Если не нашли через формы, пробуем Enter
        try:
            search_input = self.driver.switch_to.active_element
            search_input.send_keys(query)
            search_input.submit()
            time.sleep(2)
        except:
            pass

    def get_search_results(self):
        """Получить результаты поиска"""
        result_selectors = [
            ".product-card",
            ".book-item",
            ".search-result",
            ".goods-item"
        ]
        
        for selector in result_selectors:
            try:
                return self.driver.find_elements(By.CSS_SELECTOR, selector)
            except:
                continue
        return []

    def get_cart_elements(self):
        """Найти элементы корзины"""
        cart_selectors = [
            "[href*='cart']",
            "[href*='basket']",
            ".header-cart",
            ".basket-icon",
            ".cart-icon"
        ]
        
        elements = []
        for selector in cart_selectors:
            try:
                found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                elements.extend(found)
            except:
                continue
        return elements
