import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


@pytest.fixture
def driver():
    """Простая фикстура браузера"""
    options = Options()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.chitai-gorod.ru/")
    
    yield driver
    driver.quit()
