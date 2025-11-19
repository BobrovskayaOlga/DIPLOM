from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import allure
from typing import Optional, Tuple, List
from config.settings import settings


class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver: WebDriver):
        """
        Инициализация базовой страницы
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
        self.base_url = settings.BASE_URL
    
    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """
        Открыть указанный URL
        
        Args:
            url: URL для открытия
        """
        self.driver.get(url)
        self.wait_for_page_load()
        self.close_popups()
    
    @allure.step("Закрыть всплывающие окна")
    def close_popups(self) -> None:
        """Закрытие всплывающих окон и уведомлений"""
        popup_selectors = [
            "[data-testid='cookie-notification-close']",
            ".cookie-notification__close",
            ".js-cookie-notification-close",
            "[aria-label='Закрыть']",
            ".popup-close"
        ]
        
        for selector in popup_selectors:
            try:
                close_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                close_btn.click()
                print(f"Закрыто всплывающее окно с селектором: {selector}")
                break
            except TimeoutException:
                continue
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Найти элемент с ожиданием
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
            
        Returns:
            WebElement: Найденный элемент
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Найти кликабельный элемент {locator}")
    def find_clickable_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Найти кликабельный элемент с ожиданием
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
            
        Returns:
            WebElement: Найденный элемент
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @allure.step("Найти все элементы {locator}")
    def find_elements(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List:
        """
        Найти все элементы с ожиданием
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
            
        Returns:
            List[WebElement]: Список найденных элементов
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Кликнуть на элемент {locator}")
    def click_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        Кликнуть на элемент с обработкой StaleElement
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
        """
        for attempt in range(3):
            try:
                element = self.find_clickable_element(locator, timeout)
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def enter_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """
        Ввести текст в поле
        
        Args:
            locator: Кортеж (By, locator)
            text: Текст для ввода
            timeout: Время ожидания в секундах
        """
        element = self.find_clickable_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента {locator}")
    def get_element_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        Получить текст элемента
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
            
        Returns:
            str: Текст элемента
        """
        element = self.find_element(locator, timeout)
        return element.text.strip()
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """
        Проверить видимость элемента
        
        Args:
            locator: Кортеж (By, locator)
            timeout: Время ожидания в секундах
            
        Returns:
            bool: True если элемент видим
        """
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout: int = settings.PAGE_LOAD_TIMEOUT) -> None:
        """
        Ожидать полной загрузки страницы
        
        Args:
            timeout: Время ожидания в секундах
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @allure.step("Ожидание изменения URL")
    def wait_for_url_change(self, original_url: str, timeout: int = settings.EXPLICIT_WAIT) -> bool:
        """
        Ожидать изменения URL
        
        Args:
            original_url: Исходный URL
            timeout: Время ожидания в секундах
            
        Returns:
            bool: True если URL изменился
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            lambda driver: driver.current_url != original_url
        )
