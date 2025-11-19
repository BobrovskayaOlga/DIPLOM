from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from typing import List
from .base_page import BasePage


class MainPage(BasePage):
    """Класс для работы с главной страницей Читай Город"""
    
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-form__input, input[name='search'], input[placeholder*='Найти']")
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button.catalog-btn")
    
    CATALOG_ALTERNATIVES = [
        (By.CSS_SELECTOR, "button.catalog-btn"),
        (By.CSS_SELECTOR, ".header-sticky__catalog button"),
        (By.CSS_SELECTOR, "[data-action='catalog']"),
        (By.CSS_SELECTOR, ".header-catalog"),
        (By.CSS_SELECTOR, ".catalog-toggle"),
        (By.XPATH, "//button[contains(@class, 'catalog-btn')]"),
        (By.XPATH, "//button[contains(., 'Каталог')]"),
        (By.XPATH, "//span[contains(., 'Каталог')]"),
        (By.CSS_SELECTOR, ".menu-toggle")
    ]
    
    CART_BUTTONS = [
        (By.CSS_SELECTOR, "[href*='cart']"),
        (By.CSS_SELECTOR, "[href*='basket']"),
        (By.CSS_SELECTOR, ".header-cart"),
        (By.CSS_SELECTOR, ".cart-icon"),
        (By.CSS_SELECTOR, ".basket-icon"),
        (By.XPATH, "//a[contains(@href, 'cart')]"),
        (By.XPATH, "//a[contains(@href, 'basket')]"),
        (By.XPATH, "//span[contains(text(), 'Корзина')]"),
        (By.XPATH, "//*[contains(text(), 'Корзина')]"),
        (By.CSS_SELECTOR, "[data-testid='cart-button']")
    ]
    
    CATALOG_MODAL_SELECTORS = [
        (By.CSS_SELECTOR, "div.ui-modal.vfm.vfm--fixed.vfm--inset"),
        (By.CSS_SELECTOR, ".catalog-modal"),
        (By.CSS_SELECTOR, ".categories-menu"),
        (By.CSS_SELECTOR, "[role='dialog']"),
        (By.CSS_SELECTOR, ".modal-content"),
        (By.CSS_SELECTOR, ".ui-modal__content--view-sideLeft")
    ]
    
    CATEGORY_SELECTORS = [
        (By.CSS_SELECTOR, ".category-item"),
        (By.CSS_SELECTOR, ".catalog-category"),
        (By.CSS_SELECTOR, ".menu-item"),
        (By.CSS_SELECTOR, "[data-category]"),
        (By.XPATH, "//a[contains(@href, 'catalog')]"),
        (By.XPATH, "//a[contains(@href, 'category')]")
    ]

    @allure.step("Выполнить поиск по запросу: {search_text}")
    def search_for(self, search_text: str) -> None:
        """
        Выполнить поиск товара
        
        Args:
            search_text: Текст для поиска
        """
        search_input = self.find_clickable_element(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(search_text)
        search_input.send_keys(Keys.RETURN)
        
        print(f"✓ Поиск выполнен: '{search_text}'")

    @allure.step("Открыть каталог")
    def open_catalog(self) -> bool:
        """
        Открыть каталог товаров
        
        Returns:
            bool: True если каталог успешно открыт
        """
        for catalog_button in self.CATALOG_ALTERNATIVES:
            try:
                element = self.find_clickable_element(catalog_button, timeout=5)
                element.click()
                print(f"✓ Кнопка каталога найдена по селектору: {catalog_button}")
                
                if self.is_catalog_opened():
                    return True
                    
            except Exception as e:
                print(f"✗ Не удалось открыть каталог по селектору {catalog_button}: {e}")
                continue
        
        print("✗ Не удалось открыть каталог ни одним из способов")
        return False

    @allure.step("Проверить открытие каталога")
    def is_catalog_opened(self) -> bool:
        """
        Проверить, открылось ли меню каталога
        
        Returns:
            bool: True если каталог открыт
        """
        for modal_selector in self.CATALOG_MODAL_SELECTORS:
            if self.is_element_visible(modal_selector, timeout=3):
                print(f"✓ Меню каталога открылось (селектор: {modal_selector})")
                return True
        
        for category_selector in self.CATEGORY_SELECTORS:
            try:
                categories = self.driver.find_elements(*category_selector)
                if categories and len(categories) > 0:
                    print(f"✓ Найдены категории каталога (селектор: {category_selector})")
                    return True
            except:
                continue
        
        current_url = self.driver.current_url.lower()
        if "catalog" in current_url or "categories" in current_url:
            print("✓ Каталог открылся как отдельная страница")
            return True
        
        print("✗ Меню каталога не открылось")
        return False

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        """
        Открыть корзину с альтернативными селекторами
        """
        for cart_button in self.CART_BUTTONS:
            try:
                element = self.find_clickable_element(cart_button, timeout=5)
                element.click()
                print(f"✓ Корзина найдена по селектору: {cart_button}")
                return
            except Exception as e:
                print(f"✗ Не удалось найти корзину по селектору {cart_button}: {e}")
                continue
        
        print("✓ Пробуем прямой переход в корзину")
        self.driver.get(f"{self.base_url}/cart")

    @allure.step("Получить текст поля поиска")
    def get_search_text(self) -> str:
        """
        Получить текст из поля поиска
        
        Returns:
            str: Текст из поля поиска
        """
        try:
            search_input = self.find_element(self.SEARCH_INPUT)
            return search_input.get_attribute("value") or ""
        except:
            return ""

    @allure.step("Выбрать категорию в каталоге по названию: {category_name}")
    def select_catalog_category(self, category_name: str) -> bool:
        """
        Выбрать категорию в открытом каталоге
        
        Args:
            category_name: Название категории
            
        Returns:
            bool: True если категория выбрана успешно
        """
        if not self.is_catalog_opened():
            print("✗ Каталог не открыт")
            return False
        
        category_xpaths = [
            f"//*[contains(text(), '{category_name}')]",
            f"//*[contains(., '{category_name}')]",
            f"//a[contains(text(), '{category_name}')]",
            f"//span[contains(text(), '{category_name}')]"
        ]
        
        for xpath in category_xpaths:
            try:
                category_elements = self.driver.find_elements(By.XPATH, xpath)
                for element in category_elements:
                    if category_name.lower() in element.text.lower():
                        try:
                            element.click()
                            print(f"✓ Категория '{category_name}' выбрана")
                            return True
                        except:
                            self.driver.execute_script("arguments[0].click();", element)
                            print(f"✓ Категория '{category_name}' выбрана (через JS)")
                            return True
            except Exception as e:
                print(f"✗ Не удалось выбрать категорию по XPath {xpath}: {e}")
                continue
        
        print(f"✗ Не удалось найти категорию '{category_name}'")
        return False

    @allure.step("Закрыть каталог")
    def close_catalog(self) -> bool:
        """
        Закрыть открытый каталог
        
        Returns:
            bool: True если каталог закрыт успешно
        """
        close_selectors = [
            (By.CSS_SELECTOR, ".ui-modal__close"),
            (By.CSS_SELECTOR, ".modal-close"),
            (By.CSS_SELECTOR, "[aria-label='Закрыть']"),
            (By.CSS_SELECTOR, ".close-button"),
            (By.XPATH, "//button[contains(text(), 'Закрыть')]")
        ]
        
        for selector in close_selectors:
            try:
                close_btn = self.find_clickable_element(selector, timeout=3)
                close_btn.click()
                print("✓ Каталог закрыт")
                return True
            except:
                continue
        
        try:
            overlay = self.driver.find_element(By.CSS_SELECTOR, ".ui-modal.vfm.vfm--fixed.vfm--inset")
            self.driver.execute_script("arguments[0].click();", overlay)
            print("✓ Каталог закрыт (клик по оверлею)")
            return True
        except:
            pass
        
        print("✗ Не удалось закрыть каталог")
        return False

    @allure.step("Проверить наличие ключевых элементов на главной странице")
    def check_key_elements(self) -> dict:
        """
        Проверить наличие ключевых элементов на главной странице
        
        Returns:
            dict: Статус наличия элементов
        """
        elements_status = {}
        
        key_elements = {
            "search_input": self.SEARCH_INPUT,
            "catalog_button": self.CATALOG_BUTTON,
        }
        
        for element_name, locator in key_elements.items():
            try:
                is_present = self.is_element_visible(locator, timeout=5)
                elements_status[element_name] = is_present
                print(f"✓ Элемент {element_name}: {'присутствует' if is_present else 'отсутствует'}")
            except:
                elements_status[element_name] = False
                print(f"✗ Элемент {element_name}: отсутствует")
        
        return elements_status

    @allure.step("Выполнить поиск и вернуться на главную")
    def search_and_return(self, search_text: str) -> None:
        """
        Выполнить поиск и вернуться на главную страницу
        
        Args:
            search_text: Текст для поиска
        """
        original_url = self.driver.current_url
        
        self.search_for(search_text)
        
        self.wait_for_page_load()

        self.driver.get(original_url)
        self.wait_for_page_load()
        
        print(f"✓ Поиск '{search_text}' выполнен и возврат на главную")

    @allure.step("Обновить страницу")
    def refresh_page(self) -> None:
        """Обновить текущую страницу"""
        self.driver.refresh()
        self.wait_for_page_load()
        print("✓ Страница обновлена")

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """
        Получить текущий URL
        
        Returns:
            str: Текущий URL
        """
        return self.driver.current_url

    @allure.step("Получить заголовок страницы")
    def get_page_title(self) -> str:
        """
        Получить заголовок страницы
        
        Returns:
            str: Заголовок страницы
        """
        return self.driver.title
