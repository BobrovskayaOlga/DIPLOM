import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings


class DriverFactory:
    """
    Фабрика для создания и управления WebDriver
    
    Methods:
        create_chrome_driver(): Создает экземпляр Chrome WebDriver
        close_driver(driver): Корректно закрывает WebDriver
    """
    
    @staticmethod
    @allure.step("Создать Chrome WebDriver")
    def create_chrome_driver() -> webdriver.Chrome:
        """
        Создать экземпляр Chrome WebDriver
        
        Returns:
            webdriver.Chrome: Экземпляр Chrome драйвера
            
        Raises:
            Exception: Если не удалось создать драйвер
        """
        try:
            chrome_options = Options()
            
            if settings.HEADLESS:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument(f"--window-size={settings.WINDOW_SIZE}")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--remote-debugging-port=9222")

            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            if os.path.exists(settings.CHROME_DRIVER_PATH):
                allure.attach(
                    f"Using ChromeDriver from: {settings.CHROME_DRIVER_PATH}",
                    name="ChromeDriver Path",
                    attachment_type=allure.attachment_type.TEXT
                )
                service = Service(executable_path=settings.CHROME_DRIVER_PATH)
            else:
                allure.attach(
                    f"ChromeDriver not found at {settings.CHROME_DRIVER_PATH}. Using webdriver-manager",
                    name="ChromeDriver Fallback",
                    attachment_type=allure.attachment_type.TEXT
                )
                service = Service(ChromeDriverManager().install())
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.implicitly_wait(settings.IMPLICIT_WAIT)
            driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
            driver.set_script_timeout(30)
            
            return driver
            
        except Exception as e:
            allure.attach(
                f"Error creating ChromeDriver: {str(e)}",
                name="Driver Creation Error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise
    
    @staticmethod
    @allure.step("Закрыть WebDriver")
    def close_driver(driver: webdriver.Chrome) -> None:
        """
        Корректно закрыть WebDriver
        
        Args:
            driver: WebDriver instance для закрытия
        """
        if driver:
            try:
                driver.quit()
            except Exception as e:
                allure.attach(
                    f"Error closing driver: {str(e)}",
                    name="Driver Close Error",
                    attachment_type=allure.attachment_type.TEXT
                )
