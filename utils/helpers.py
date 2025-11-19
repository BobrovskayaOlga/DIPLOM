import requests
import allure
from typing import Dict, Any, Optional
from config.settings import settings
from config.test_data import test_data


class APIHelper:
    """Класс-помощник для API тестов"""
    
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.headers = settings.get_api_headers()
    
    @allure.step("Выполнить API поиск по запросу: {query}")
    def search_products(self, query: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Выполнить поиск товаров через API
        
        Args:
            query: Поисковый запрос
            headers: Заголовки запроса (опционально)
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        if headers is None:
            headers = self.headers
            
        search_url = f"{self.base_url}/search"
        params = {"q": query}
        
        try:
            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.text,
                "url": response.url
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": None
            }
    
    @allure.step("Выполнить API запрос методом {method}")
    def make_api_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить произвольный API запрос
        
        Args:
            method: HTTP метод
            url: URL для запроса
            **kwargs: Дополнительные параметры
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        try:
            response = requests.request(method.upper(), url, **kwargs)
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.text,
                "url": response.url
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": None
            }
    
    @allure.step("Проверить доступность сайта")
    def check_site_availability(self) -> Dict[str, Any]:
        """
        Проверить доступность главной страницы
        
        Returns:
            Dict[str, Any]: Результат проверки
        """
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                timeout=10
            )
            
            return {
                "status_code": response.status_code,
                "available": response.status_code == 200,
                "url": response.url
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "available": False,
                "status_code": None
            }
