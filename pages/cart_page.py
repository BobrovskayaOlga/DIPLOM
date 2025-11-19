from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from typing import List
from .base_page import BasePage


class CartPage(BasePage):
    """Класс для работы со страницей корзины Читай Город"""
    
    CART_ITEMS = [
        (By.CSS_SELECTOR, ".cart-item"),
        (By.CSS_SELECTOR, ".basket-item"),
        (By.CSS_SELECTOR, ".cart-product"),
        (By.CSS_SELECTOR, ".basket__item"),
        (By.CSS_SELECTOR, ".cart__item"),
        (By.CSS_SELECTOR, "[data-testid='cart-item']")
    ]
    
    ITEM_TITLE = (By.CSS_SELECTOR, ".product-title, .item-title, [data-testid='product-title']")
    
    EMPTY_CART_SELECTORS = [
        (By.XPATH, "//*[contains(text(), 'корзина пуста')]"),
        (By.XPATH, "//*[contains(text(), 'пустая корзина')]"),
        (By.XPATH, "//*[contains(text(), 'корзина пустая')]"),
        (By.CSS_SELECTOR, ".cart-empty, .empty-cart, .basket-empty")
    ]
    
    @allure.step("Получить список товаров в корзине")
    def get_cart_items(self) -> List[str]:
        """
        Получить список названий товаров в корзине
        
        Returns:
            List[str]: Список названий товаров
        """
        items = []
        for cart_selector in self.CART_ITEMS:
            try:
                cart_elements = self.driver.find_elements(*cart_selector)
                
                for item in cart_elements:
                    try:
                        title_selectors = [
                            ".product-title",
                            ".item-title", 
                            ".cart-item__title",
                            ".basket-item__name",
                            "h3",
                            "a"
                        ]
                        
                        for title_selector in title_selectors:
                            try:
                                title_element = item.find_element(By.CSS_SELECTOR, title_selector)
                                title_text = title_element.text.strip()
                                if title_text:
                                    items.append(title_text)
                                    break
                            except:
                                continue
                                
                    except:
                        continue
                        
                if items:
                    break
                    
            except:
                continue
        
        return items
    
    @allure.step("Проверить пуста ли корзина")
    def is_cart_empty(self) -> bool:
        """
        Проверить пуста ли корзина
        
        Returns:
            bool: True если корзина пуста
        """
        for selector in self.EMPTY_CART_SELECTORS:
            try:
                if self.is_element_visible(selector, timeout=3):
                    return True
            except:
                continue
        
        return len(self.get_cart_items()) == 0
    
    @allure.step("Проверить наличие товара {product_name} в корзине")
    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Проверить наличие товара в корзине 
        
        Args:
            product_name: Название товара для проверки
            
        Returns:
            bool: True если товар присутствует в корзине
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-item, .basket-item, .cart-product, .cart__item"))
            )
        except:
            print("Элементы корзины не найдены, продолжаем проверку...")
        cart_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        product_in_text = product_name.lower() in cart_text
        
        cart_items = self.get_cart_items()
        product_in_items = any(product_name.lower() in item.lower() for item in cart_items)
        
        print(f"Проверка товара в корзине: '{product_name}'")
        print(f"В тексте страницы: {product_in_text}")
        print(f"В элементах корзины: {product_in_items}")
        print(f"Товары в корзине: {cart_items}")
        
        return product_in_text or product_in_items
    
    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """
        Получить количество товаров в корзине
        
        Returns:
            int: Количество товаров
        """
        try:
            for cart_selector in self.CART_ITEMS:
                cart_items = self.driver.find_elements(*cart_selector)
                if cart_items:
                    return len(cart_items)
        except:
            pass
        return 0
    
    @allure.step("Проверить, что находимся на странице корзины")
    def is_cart_page(self) -> bool:
        """
        Проверить, что текущая страница - корзина
        
        Returns:
            bool: True если это страница корзины
        """
        current_url = self.driver.current_url.lower()
        cart_indicators = ["cart", "basket", "korzin", "корзин"]
        is_cart_url = any(indicator in current_url for indicator in cart_indicators)
        
        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        cart_text_indicators = ["корзина", "оформление заказа", "итого", "сумма"]
        has_cart_content = any(indicator in page_text for indicator in cart_text_indicators)
        
        return is_cart_url or has_cart_content
