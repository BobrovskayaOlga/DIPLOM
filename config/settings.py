import os
from typing import Dict, Any


class Settings:
    """Класс для хранения настроек проекта"""
    
    BASE_URL: str = "https://www.chitai-gorod.ru"
    
    API_SEARCH_URL: str = f"{BASE_URL}/search"
    
   
    IMPLICIT_WAIT: int = 5
    EXPLICIT_WAIT: int = 15
    PAGE_LOAD_TIMEOUT: int = 30
    
    BROWSER: str = "chrome"
    HEADLESS: bool = False
    WINDOW_SIZE: str = "1920x1080"
    
    CHROME_DRIVER_PATH: str = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
    
    TEST_DATA_DIR: str = os.path.join(os.path.dirname(__file__), "..", "test_data")
    
    @classmethod
    def get_api_headers(cls) -> Dict[str, str]:
        """Получить заголовки для API запросов"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Referer": f"{cls.BASE_URL}/"
        }


settings = Settings()
