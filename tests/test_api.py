import pytest
import allure
from utils.helpers import APIHelper
from config.settings import settings
from config.test_data import test_data


class TestAPI:
    """Класс для API тестов"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка перед каждым тестом"""
        self.api_helper = APIHelper()
    
    @allure.feature("API Тесты")
    @allure.story("Проверка доступности сайта")
    def test_site_availability(self):
        """Тест доступности сайта"""
        with allure.step("Проверить доступность сайта"):
            result = self.api_helper.check_site_availability()
        
        with allure.step("Убедиться, что сайт доступен"):
            assert result['available'], f"Сайт недоступен: {result.get('error', 'Unknown error')}"
    
    @allure.feature("API Тесты")
    @allure.story("Поиск по названию по кириллице")
    def test_search_cyrillic(self):
        """Тест поиска по кириллице через API"""
        with allure.step(f"Выполнить API поиск по запросу: {test_data.SEARCH_DATA['cyrillic_search']}"):
            response = self.api_helper.search_products(test_data.SEARCH_DATA['cyrillic_search'])
        
        with allure.step("Проверить статус код ответа"):
            assert response['status_code'] in [200, 301, 302], f"Неверный статус код: {response['status_code']}"
    
    @allure.feature("API Тесты")
    @allure.story("Поиск названия содержащего цифры")
    def test_search_cyrillic_with_numbers(self):
        """Тест поиска названия содержащего цифры через API"""
        with allure.step(f"Выполнить API поиск по запросу: {test_data.SEARCH_DATA['cyrillic_with_numbers']}"):
            response = self.api_helper.search_products(test_data.SEARCH_DATA['cyrillic_with_numbers'])
        
        with allure.step("Проверить статус код ответа"):
            assert response['status_code'] in [200, 301, 302], f"Неверный статус код: {response['status_code']}"
    
    @allure.feature("API Тесты")
    @allure.story("Пустой поиск")
    def test_empty_search(self):
        """Тест пустого поиска через API"""
        with allure.step("Выполнить API поиск с пустым запросом"):
            response = self.api_helper.search_products(test_data.SEARCH_DATA['empty_search'])
        
        with allure.step("Проверить статус код ответа"):
            assert response['status_code'] in [200, 301, 302, 400, 422], f"Неожиданный статус код: {response['status_code']}"
    
    @allure.feature("API Тесты")
    @allure.story("Поиск без токена")
    def test_search_without_token(self):
        """Тест поиска без авторизационного токена"""
        with allure.step("Подготовить заголовки без авторизации"):
            headers = settings.get_api_headers()
            if 'Authorization' in headers:
                del headers['Authorization']
        
        with allure.step(f"Выполнить API поиск без токена по запросу: {test_data.SEARCH_DATA['cyrillic_search']}"):
            response = self.api_helper.search_products(
                test_data.SEARCH_DATA['cyrillic_search'],
                headers=headers
            )
        
        with allure.step("Проверить ответ API"):
            assert response['status_code'] in [200, 301, 302], f"Неожиданный статус код: {response['status_code']}"
    
    @allure.feature("API Тесты")
    @allure.story("Поиск другим методом")
    def test_search_wrong_method(self):
        """Тест поиска с использованием неправильного HTTP метода"""
        with allure.step("Выполнить API запрос методом POST вместо GET"):
            response = self.api_helper.make_api_request(
                method="POST",
                url=f"{settings.BASE_URL}/search",
                params={"q": test_data.SEARCH_DATA['cyrillic_search']},
                headers=settings.get_api_headers()
            )
        
        with allure.step("Проверить ответ на неправильный метод"):
            assert response['status_code'] is not None, "Не получен ответ от сервера"
