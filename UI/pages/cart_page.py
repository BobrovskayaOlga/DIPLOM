from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage
import allure
import os


class CartPageImproved(BasePage):
    """Улучшенная версия Page Object для корзины."""
    
    # Расширенные локаторы для корзины
    CART_SELECTORS = [
        (By.CSS_SELECTOR, "[href*='cart']"),
        (By.CSS_SELECTOR, "[href*='basket']"),
        (By.CSS_SELECTOR, "[href*='korzina']"),
        (By.CSS_SELECTOR, ".cart-btn"),
        (By.CSS_SELECTOR, ".basket-btn"),
        (By.CSS_SELECTOR, ".header-cart"),
        (By.CSS_SELECTOR, ".header-basket"),
        (By.CSS_SELECTOR, "[data-testid*='cart']"),
        (By.CSS_SELECTOR, "[data-testid*='basket']"),
        (By.CSS_SELECTOR, ".chg-cart"),
        (By.CSS_SELECTOR, ".chg-basket"),
        (By.XPATH, "//*[contains(text(), 'Корзина')]"),
        (By.XPATH, "//*[contains(text(), 'корзина')]"),
        (By.XPATH, "//*[contains(text(), 'Корзине')]"),
        (By.XPATH, "//*[contains(text(), 'Basket')]"),
        (By.XPATH, "//*[contains(text(), 'basket')]"),
        (By.XPATH, "//*[contains(@class, 'cart')]"),
        (By.XPATH, "//*[contains(@class, 'basket')]")
    ]
    
    @allure.step("Проверить видимость корзины")
    def is_cart_visible(self) -> bool:
        """
        Улучшенная проверка что корзина отображается на странице.
        
        Returns:
            bool: True если корзина видна
        """
        for selector in self.CART_SELECTORS:
            try:
                elements = self.driver.find_elements(*selector)
                for element in elements:
                    if element.is_displayed():
                        element_text = element.text.strip()
                        allure.attach(f"Найден элемент корзины: {element_text}", name="Cart Element Found")
                        return True
            except Exception:
                continue
        
        # Если не нашли стандартными способами, делаем скриншот для анализа
        self._take_debug_screenshot("cart_not_found")
        return False
    
    @allure.step("Найти все элементы корзины")
    def find_all_cart_elements(self) -> list:
        """
        Поиск всех возможных элементов корзины.
        
        Returns:
            list: Список найденных элементов
        """
        found_elements = []
        
        for selector in self.CART_SELECTORS:
            try:
                elements = self.driver.find_elements(*selector)
                for element in elements:
                    if element.is_displayed():
                        element_info = {
                            'selector': str(selector),
                            'text': element.text.strip(),
                            'tag': element.tag_name,
                            'location': element.location
                        }
                        found_elements.append(element_info)
            except Exception:
                continue
        
        return found_elements
    
    @allure.step("Открыть корзину")
    def open_cart(self) -> bool:
        """
        Улучшенное открытие корзины.
        
        Returns:
            bool: True если корзина открыта успешно
        """
        # Сначала ищем все возможные элементы корзины
        cart_elements = self.find_all_cart_elements()
        
        if not cart_elements:
            allure.attach("Элементы корзины не найдены", name="No Cart Elements")
            return self._open_cart_via_url()
        
        # Пробуем кликнуть по найденным элементам
        for element_info in cart_elements:
            try:
                selector = eval(element_info['selector'])  # Преобразуем строку обратно в кортеж
                elements = self.driver.find_elements(*selector)
                
                for element in elements:
                    if element.text.strip() == element_info['text']:
                        self.driver.execute_script("arguments[0].click();", element)
                        self.wait_for_page_loaded()
                        
                        # Проверяем успешность перехода
                        if self._is_cart_page_loaded():
                            allure.attach(f"Корзина открыта через: {element_info['text']}", name="Cart Opened")
                            return True
            except Exception as e:
                continue
        
        # Если клики не сработали, пробуем URL
        return self._open_cart_via_url()
    
    def _is_cart_page_loaded(self) -> bool:
        """Проверка что загружена страница корзины."""
        current_url = self.driver.current_url.lower()
        cart_indicators = ['cart', 'basket', 'korzina']
        
        if any(indicator in current_url for indicator in cart_indicators):
            return True
        
        # Дополнительные проверки по содержимому страницы
        page_indicators = [
            "корзина",
            "корзине", 
            "basket",
            "cart",
            "товаров в корзине",
            "ваша корзина"
        ]
        
        page_text = self.driver.page_source.lower()
        return any(indicator in page_text for indicator in page_indicators)
    
    def _open_cart_via_url(self) -> bool:
        """Открытие корзины через прямые URL."""
        cart_urls = [
            "https://www.chitai-gorod.ru/cart",
            "https://www.chitai-gorod.ru/basket", 
            "https://www.chitai-gorod.ru/korzina",
            "https://www.chitai-gorod.ru/profile/cart"
        ]
        
        for url in cart_urls:
            try:
                self.driver.get(url)
                self.wait_for_page_loaded()
                
                if self._is_cart_page_loaded():
                    allure.attach(f"Корзина открыта по URL: {url}", name="Cart URL Success")
                    return True
                    
            except Exception as e:
                continue
        
        return False
    
    @allure.step("Проверить наличие кнопок добавления в корзину")
    def are_add_to_cart_buttons_present(self) -> bool:
        """
        Проверка наличия кнопок добавления в корзину.
        
        Returns:
            bool: True если кнопки найдены
        """
        add_button_selectors = [
            (By.CSS_SELECTOR, "[onclick*='cart']"),
            (By.CSS_SELECTOR, "[data-action*='cart']"),
            (By.CSS_SELECTOR, ".add-to-cart"),
            (By.CSS_SELECTOR, ".buy-btn"),
            (By.CSS_SELECTOR, ".product-buy"),
            (By.CSS_SELECTOR, "[data-product-id]"),
            (By.CSS_SELECTOR, ".chg-buy-button"),
            (By.XPATH, "//button[contains(text(), 'Купить')]"),
            (By.XPATH, "//button[contains(text(), 'В корзину')]"),
            (By.XPATH, "//button[contains(text(), 'Добавить')]")
        ]
        
        found_buttons = []
        
        for selector in add_button_selectors:
            try:
                buttons = self.driver.find_elements(*selector)
                for button in buttons:
                    if button.is_displayed():
                        button_info = {
                            'text': button.text.strip(),
                            'selector': str(selector)
                        }
                        found_buttons.append(button_info)
            except Exception:
                continue
        
        if found_buttons:
            allure.attach(f"Найдено кнопок: {len(found_buttons)}", name="Add Buttons Count")
            for btn in found_buttons[:3]:  # Показываем первые 3
                allure.attach(f"Кнопка: '{btn['text']}'", name="Button Found")
            return True
        
        return False
    
    @allure.step("Получить состояние корзины")
    def get_cart_state(self) -> str:
        """
        Получение текущего состояния корзины.
        
        Returns:
            str: Описание состояния корзины
        """
        # Проверяем URL
        current_url = self.driver.current_url.lower()
        
        # Проверяем различные индикаторы
        empty_indicators = [
            (By.XPATH, "//*[contains(text(), 'корзина пуста')]"),
            (By.XPATH, "//*[contains(text(), 'ваша корзина пуста')]"),
            (By.XPATH, "//*[contains(text(), 'корзина пока пуста')]"),
            (By.CSS_SELECTOR, ".empty-cart"),
            (By.CSS_SELECTOR, ".basket-empty"),
            (By.CSS_SELECTOR, "[data-empty-cart]")
        ]
        
        for indicator in empty_indicators:
            if self.is_element_present(indicator, timeout=2):
                return "Пустая корзина"
        
        # Проверяем наличие товаров
        item_indicators = [
            (By.CSS_SELECTOR, ".cart-item"),
            (By.CSS_SELECTOR, ".basket-item"),
            (By.CSS_SELECTOR, "[data-cart-item]"),
            (By.CSS_SELECTOR, ".chg-cart-item")
        ]
        
        for indicator in item_indicators:
            if self.is_element_present(indicator, timeout=2):
                items = self.driver.find_elements(*indicator)
                return f"Корзина с товарами ({len(items)} шт.)"
        
        return "Состояние не определено"
    
    def _take_debug_screenshot(self, name: str) -> None:
        """Создание отладочного скриншота."""
        try:
            os.makedirs("debug_screenshots", exist_ok=True)
            path = f"debug_screenshots/{name}.png"
            self.driver.save_screenshot(path)
        except Exception as e:
            print(f"Не удалось создать скриншот: {e}")
