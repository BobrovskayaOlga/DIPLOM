from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from typing import List, Dict, Any
from .base_page import BasePage


class SearchPage(BasePage):
    """Класс для работы со страницей поиска Читай Город"""
    
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-card, .book-card, [class*='product']")
    PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='/product/']")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-card__title, .book-title, .title")
    
    NO_RESULTS_SELECTORS = [
        (By.XPATH, "//*[contains(text(), 'ничего не найдено')]"),
        (By.XPATH, "//*[contains(text(), 'не найдено')]"),
        (By.XPATH, "//*[contains(text(), 'ничего не нашлось')]"),
        (By.XPATH, "//*[contains(text(), 'товаров не найдено')]"),
        (By.CSS_SELECTOR, ".search-empty, .no-results, .empty-results")
    ]
    
    SEARCH_TITLE = (By.CSS_SELECTOR, ".search-title__head")
    
    ADD_TO_CART_SELECTORS = [
        (By.XPATH, "//div[contains(@class, 'chg-app-button__content') and contains(text(), 'Купить')]"),
        (By.XPATH, "//button[.//div[contains(text(), 'Купить')]]"),
        (By.XPATH, "//*[contains(text(), 'Купить') and contains(@class, 'button')]"),
        (By.CSS_SELECTOR, ".chg-app-button__content"),
        (By.CSS_SELECTOR, "button .chg-app-button__content"),
        (By.CSS_SELECTOR, "[class*='chg-app-button']"),
    ]
    
    SUCCESS_SELECTORS = [
        (By.XPATH, "//*[contains(text(), 'Добавлено')]"),
        (By.XPATH, "//*[contains(text(), 'добавлен')]"),
        (By.XPATH, "//*[contains(text(), 'В корзине')]"),
        (By.XPATH, "//*[contains(text(), 'корзину')]"),
        (By.CSS_SELECTOR, "[class*='success']"),
        (By.CSS_SELECTOR, "[class*='added']")
    ]
    
    @allure.step("Ожидать загрузки результатов поиска")
    def wait_for_search_results(self, timeout: int = 20) -> bool:
        """
        Ожидать загрузки результатов поиска
        
        Args:
            timeout: Время ожидания в секундах
            
        Returns:
            bool: True если результаты загружены
        """
        try:
            self.wait.until(
                lambda driver: len(driver.find_elements(*self.SEARCH_RESULTS)) > 0 or
                              len(driver.find_elements(*self.PRODUCT_LINKS)) > 0 or
                              "search" in driver.current_url.lower() or
                              "query" in driver.current_url.lower() or
                              self._has_no_results_message()
            )
            return True
        except:
            return False
    
    @allure.step("Проверить статус поиска")
    def get_search_status(self) -> Dict[str, Any]:
        """
        Получить детальный статус поиска (как в рабочей версии)
        
        Returns:
            Dict: Статус поиска с деталями
        """
        status = {
            "has_results": False,
            "has_no_results_message": False,
            "is_search_page": False,
            "results_count": 0,
            "product_links_count": 0,
            "current_url": self.driver.current_url
        }
        
        try:
            products = self.driver.find_elements(*self.SEARCH_RESULTS)
            status["results_count"] = len(products)
            status["has_results"] = len(products) > 0
        except:
            pass
        
        try:
            product_links = self.driver.find_elements(*self.PRODUCT_LINKS)
            status["product_links_count"] = len(product_links)
            if not status["has_results"]:
                status["has_results"] = len(product_links) > 0
        except:
            pass
        
        status["has_no_results_message"] = self._has_no_results_message()
        
        current_url = self.driver.current_url.lower()
        url_indicators = ["search", "query", "q="]
        status["is_search_page"] = any(indicator in current_url for indicator in url_indicators)
        
        return status
    
    def _has_no_results_message(self) -> bool:
        """Внутренный метод проверки сообщения об отсутствии результатов"""
        for selector in self.NO_RESULTS_SELECTORS:
            try:
                if self.is_element_visible(selector, timeout=2):
                    return True
            except:
                continue
        return False
    
    @allure.step("Получить список результатов поиска")
    def get_search_results(self) -> List[str]:
        """
        Получить список названий товаров из результатов поиска
        
        Returns:
            List[str]: Список названий товаров
        """
        results = []
        try:
            product_elements = self.driver.find_elements(*self.PRODUCT_LINKS)
            
            for product in product_elements:
                try:
                    title_text = product.text.strip()
                    if title_text and len(title_text) > 0:
                        results.append(title_text)
                except:
                    continue
                    
            if not results:
                product_cards = self.driver.find_elements(*self.SEARCH_RESULTS)
                
                for product in product_cards:
                    try:
                        title_element = product.find_element(By.CSS_SELECTOR, ".title, h3, a, .product-card__title")
                        title_text = title_element.text.strip()
                        if title_text:
                            results.append(title_text)
                    except:
                        continue
        except:
            pass
        
        return results
    
    @allure.step("Добавить товар в корзину по индексу {index}")
    def add_to_cart_by_index(self, index: int = 0) -> str:
        """
        Добавить товар в корзину по индексу (с улучшенной отладкой)
        
        Args:
            index: Индекс товара в списке результатов
            
        Returns:
            str: Название добавленного товара
        """
        print(f"Поиск товара с индексом {index}...")
        
        product_links = self.driver.find_elements(*self.PRODUCT_LINKS)
        print(f"Найдено ссылок на товары: {len(product_links)}")
        
        if index < len(product_links):
            product_link = product_links[index]
            
            product_title = product_link.text.strip() or f"Товар {index + 1}"
            print(f"Выбираем товар: '{product_title}'")
            print(f"Ссылка товара: {product_link.get_attribute('href')}")
            print("Переход на страницу товара...")
            product_link.click()
            self.wait_for_page_load()
            
            print("Ожидание загрузки страницы товара...")
            WebDriverWait(self.driver, 15).until(
                lambda driver: "/product/" in driver.current_url
            )
            print(f"Страница товара загружена: {self.driver.current_url}")
            

            self.take_screenshot("product_page")
            
            return self._add_to_cart_from_product_page(product_title)
        
        raise IndexError(f"Товар с индексом {index} не найден. Всего товаров: {len(product_links)}")
    
    def _add_to_cart_from_product_page(self, product_title: str) -> str:
        """
        Добавить товар в корзину со страницы товара (точная логика рабочего теста)
        
        Args:
            product_title: Название товара
            
        Returns:
            str: Название добавленного товара
        """
        print("Поиск кнопки 'Купить' на странице товара...")
        

        for selector in self.ADD_TO_CART_SELECTORS:
            try:
                print(f"Попытка найти кнопку по селектору: {selector}")
                add_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(selector)
                )
                
                button_text = add_button.text.strip()
                print(f"Найден элемент с текстом: '{button_text}'")
                
                if "Купить" in button_text:
                    print(f"✓ Найдена кнопка 'Купить' с селектором: {selector}")
                    
                    add_button.click()
                    print(f"✓ Товар '{product_title}' добавлен в корзину")
                    

                    self._wait_for_cart_success_message()
                    return product_title
                    
            except Exception as e:
                print(f"Не удалось найти/кликнуть по селектору {selector}: {e}")
                continue
        
        return self._try_alternative_add_to_cart(product_title)
    
    def _try_alternative_add_to_cart(self, product_title: str) -> str:
        """
        Альтернативный способ добавления в корзину
        """
        print("Пробуем альтернативный способ добавления в корзину...")
        
        buy_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Купить')]")
        print(f"Найдено элементов с текстом 'Купить': {len(buy_elements)}")
        
        for i, element in enumerate(buy_elements):
            try:
                element_text = element.text.strip()
                print(f"Элемент {i+1}: '{element_text}'")
                
                if "Купить" in element_text:
                    print(f"✓ Кликаем на элемент с текстом 'Купить'")
                    element.click()
                    
                    self._wait_for_cart_success_message()
                    return product_title
                    
            except Exception as e:
                print(f"Ошибка при клике на элемент {i+1}: {e}")
                continue
        
        raise Exception("Не удалось найти и кликнуть кнопку 'Купить' на странице товара")
    
    def _wait_for_cart_success_message(self):
        """
        Ожидание сообщения об успешном добавлении (как в рабочем тесте)
        """
        print("Ожидаем сообщение об успешном добавлении...")
        
        success_phrases = [
            "Добавлено",
            "добавлен", 
            "В корзине",
            "корзину"
        ]
        
        for phrase in success_phrases:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//*[contains(text(), '{phrase}')]")
                    )
                )
                print(f"✓ Успех: {element.text}")
                return
            except:
                continue
        
        print("⚠ Сообщение об успешном добавлении не найдено, продолжаем...")
    
    def _wait_for_cart_update(self):
        """Ожидание обновления состояния корзины после добавления товара"""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: any(
                    self._is_element_present(selector) 
                    for selector in self.SUCCESS_SELECTORS
                )
            )
            print("✓ Состояние корзины обновлено")
        except:

            try:
                WebDriverWait(self.driver, 3).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                print("✓ Страница готова после добавления в корзину")
            except:
                print("⚠ Сообщение об успешном добавлении не появилось, продолжаем...")
    
    def _is_element_present(self, locator):
        """Проверить наличие элемента без ожидания"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    def _verify_add_to_cart_success(self):
        """Проверить успешное добавление в корзину"""
        print("Проверка успешного добавления в корзину")
        
        for selector in self.SUCCESS_SELECTORS:
            try:
                success_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(selector)
                )
                print(f"Успех: {success_element.text}")
                return
            except:
                continue
                    
        print("Сообщение об успешном добавлении не найдено, продолжаем...")
    
    @allure.step("Проверить наличие сообщения 'нет результатов'")
    def has_no_results_message(self) -> bool:
        """
        Проверить наличие сообщения об отсутствии результатов
        
        Returns:
            bool: True если сообщение присутствует
        """
        return self._has_no_results_message()
    
    @allure.step("Получить заголовок поиска")
    def get_search_title(self) -> str:
        """
        Получить заголовок страницы поиска
        
        Returns:
            str: Текст заголовка
        """
        try:
            return self.get_element_text(self.SEARCH_TITLE)
        except:
            return ""
    
    @allure.step("Проверить наличие результатов")
    def has_results(self) -> bool:
        """
        Проверить наличие результатов поиска
        
        Returns:
            bool: True если есть результаты
        """
        return len(self.get_search_results()) > 0
    
    @allure.step("Проверить, что находимся на странице поиска")
    def is_search_page(self) -> bool:
        """
        Проверить, что текущая страница - страница поиска
        
        Returns:
            bool: True если это страница поиска
        """
        current_url = self.driver.current_url.lower()
        url_indicators = ["search", "query", "q="]
        return any(indicator in current_url for indicator in url_indicators)
