import pytest
import requests
import allure
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
    
    # Очистка после теста
    with allure.step("Удаление созданных пользователей"):
        for token in created_tokens:
            headers = {"Authorization": token}
            try:
                response = requests.delete(UrlsSB.urlDeleteUser, headers=headers)
                if response.status_code == 202:
                    allure.attach(f"Пользователь успешно удален", name="Удаление пользователя")
                else:
                    allure.attach(f"Ошибка при удалении пользователя: {response.status_code}", 
                                name="Ошибка удаления")
            except Exception as e:
                allure.attach(f"Исключение при удалении: {str(e)}", name="Ошибка удаления")