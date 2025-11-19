from typing import Dict, List, Any


class TestData:
    """Класс для хранения тестовых данных"""
    
    SEARCH_DATA: Dict[str, Any] = {
        "latin_search": "harry potter",
        "numeric_search": "1984",
        "special_chars_search": "C#",
        "cyrillic_search": "гарри поттер",
        "cyrillic_with_numbers": "12 стульев",
        "empty_search": "",
        "catalog_search": "алмазная мозаика"
    }
    

    CATEGORY_PATH: List[str] = ["Творчество и хобби", "Мозаика", "Алмазная мозаика"]
   
    EXPECTED_RESULTS: Dict[str, Any] = {
        "latin_expected_contains": "Гарри Поттер",
        "numeric_expected_contains": "1984",
        "cyrillic_expected_contains": "Гарри Поттер",
        "cyrillic_numbers_expected_contains": "12 стульев"
    }
    
    ERROR_MESSAGES: Dict[str, str] = {
        "empty_search_error": "Введите поисковый запрос",
        "unauthorized_error": "Unauthorized",
        "method_not_allowed": "Method Not Allowed"
    }


test_data = TestData()
