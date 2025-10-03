import allure
import pytest
import requests
from Credentials.urls import UrlsSB
from Credentials.data_user import test_users_data

@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.title("Тест авторизации пользователя")
    @allure.story("Проверка различных сценариев авторизации пользователя")
    @pytest.mark.parametrize('email, password', test_users_data)
    
    def test_login_user(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        
        with allure.step("Отправка запроса на авторизацию пользователя"):
            response = requests.post(UrlsSB.urlLoginUser, json=payload)
            response_body = response.json()
        
        with allure.step("Валидация ответа"):
            if response.status_code == 200:
                with allure.step("Проверка успешной авторизации"):
                    assert response_body['success'] == True
                    assert 'accessToken' in response_body
                    assert 'refreshToken' in response_body
                    assert response_body['user']['email'] == email
                    assert response_body['user']['name'] == 'qwerty13'
            else:
                with allure.step("Проверка ошибки авторизации"):
                    assert response.status_code == 401
                    assert response_body['success'] == False
                    assert response_body['message'] == 'email or password are incorrect'