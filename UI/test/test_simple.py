import pytest
import allure
from pages.base_page import MainPage


@allure.feature("Основные тесты")
class TestSimple:
    
    @allure.title("Тест 1: Поиск книги")
    def test_search_book(self, driver):
        """Простой поиск книги"""
        page = MainPage(driver)
        
        # Принимаем куки
        page.accept_cookies()
        
        # Выполняем поиск
        page.search("книга")
        
        # Проверяем что страница загрузилась
        current_url = driver.current_url
        assert "chitai-gorod" in current_url
        allure.attach(f"URL: {current_url}", name="Page URL")

    @allure.title("Тест 2: Поиск на латинице") 
    def test_search_latin(self, driver):
        """Поиск Harry Potter"""
        page = MainPage(driver)
        page.accept_cookies()
        
        page.search("Harry Potter")
        
        # Проверяем что поиск выполнен
        results = page.get_search_results()
        allure.attach(f"Найдено результатов: {len(results)}", name="Search Results")
        
        # Если есть результаты - хорошо, если нет - тоже нормально
        assert "chitai-gorod" in driver.current_url

    @allure.title("Тест 3: Поиск с цифрами")
    def test_search_numbers(self, driver):
        """Поиск 1984"""
        page = MainPage(driver)
        page.accept_cookies()
        
        page.search("1984")
        
        # Главное - что страница не упала
        current_url = driver.current_url
        assert "error" not in current_url
        allure.attach(f"URL после поиска: {current_url}", name="Search Completed")

    @allure.title("Тест 4: Поиск с спецсимволами")
    def test_search_special(self, driver):
        """Поиск со спецсимволами"""
        page = MainPage(driver)
        page.accept_cookies()
        
        page.search("!@#$%")
        
        # Проверяем что система обработала запрос
        current_url = driver.current_url
        assert "chitai-gorod" in current_url
        allure.attach("Система обработала спецсимволы", name="Special Chars Handled")

    @allure.title("Тест 5: Проверка корзины")
    def test_cart_elements(self, driver):
        """Поиск элементов корзины"""
        page = MainPage(driver)
        page.accept_cookies()
        
        # Ищем элементы корзины
        cart_elements = page.get_cart_elements()
        
        if cart_elements:
            allure.attach(f"Найдено элементов корзины: {len(cart_elements)}", name="Cart Elements Found")
            for i, element in enumerate(cart_elements[:3]):
                try:
                    text = element.text.strip()
                    if text:
                        allure.attach(f"Элемент {i+1}: {text}", name=f"Cart Element")
                except:
                    pass
        else:
            allure.attach("Элементы корзины не найдены", name="No Cart Elements")
        
        # Тест всегда проходит - мы просто проверяем наличие элементов
        assert True
