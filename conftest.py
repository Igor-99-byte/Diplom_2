import pytest
import requests
from Credentials.urls import UrlsSB

@pytest.fixture
def login_user():
    def _login(email='qwerty14@mail.ru', password='123456'):
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(UrlsSB.urlLoginUser, json=payload)
        response_body = response.json()
        token = response_body['accessToken']
        return token
    return _login

@pytest.fixture(scope="function")
def cleanup_users():
    """Фикстура для очистки созданных пользователей"""
    created_tokens = []
    
    yield created_tokens
    
    # Очистка после теста - линейный сценарий без обработки ошибок
    for token in created_tokens:
        headers = {"Authorization": token}
        requests.delete(UrlsSB.urlDeleteUser, headers=headers)