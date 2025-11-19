import pytest
import allure
from datetime import datetime
import os


def pytest_addoption(parser):
    """Добавление кастомных опций для pytest"""
    parser.addoption("--ui", action="store_true", help="Запустить только UI тесты")
    parser.addoption("--api", action="store_true", help="Запустить только API тесты")
    parser.addoption("--all", action="store_true", help="Запустить все тесты")


def pytest_collection_modifyitems(config, items):
    """Модификация коллекции тестов на основе опций"""
    if config.getoption("--ui"):
        skip_marker = pytest.mark.skip(reason="Запущены только UI тесты")
        for item in items:
            if "test_api" in item.nodeid:
                item.add_marker(skip_marker)
    
    elif config.getoption("--api"):
        skip_marker = pytest.mark.skip(reason="Запущены только API тесты")
        for item in items:
            if "test_ui" in item.nodeid:
                item.add_marker(skip_marker)
    
    elif config.getoption("--all"):
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении UI тестов"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if "test_ui" in item.nodeid:
            try:
                from tests.test_ui import TestUI
                if hasattr(TestUI, 'driver'):
                    allure.attach(
                        TestUI.driver.get_screenshot_as_png(),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
            except:
                pass


@pytest.fixture(autouse=True)
def allure_environment(request, pytestconfig):
    """Добавление информации об окружении в Allure отчет"""
    if hasattr(request.config, '_metadata'):
        request.config._metadata['Test Suite'] = 'Chitai-Gorod Tests'
        request.config._metadata['Python Version'] = '3.8+'
        request.config._metadata['Timestamp'] = datetime.now().isoformat()
