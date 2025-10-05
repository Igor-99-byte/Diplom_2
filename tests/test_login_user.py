import allure
import requests
from Credentials.urls import UrlsSB
from Credentials.data_user import LoginPassedUser, LoginFailedUser

@allure.feature("Авторизация пользователя")
class TestLoginUser:
    
    @allure.title("Успешная авторизация пользователя")
    @allure.story("Позитивные сценарии авторизации")
    def test_login_user_success(self):
        payload = {
            "email": LoginPassedUser.email,
            "password": LoginPassedUser.password
        }       
        
        with allure.step("Отправка запроса на авторизацию пользователя"):
            response = requests.post(UrlsSB.urlLoginUser, json=payload)
            response_body = response.json()
        
        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200
            assert response_body['success'] == True
            assert 'accessToken' in response_body
            assert 'refreshToken' in response_body
            assert response_body['user']['email'] == LoginPassedUser.email
            assert response_body['user']['name'] == LoginPassedUser.name
    
    @allure.title("Неуспешная авторизация пользователя с неверными данными")
    @allure.story("Негативные сценарии авторизации")
    def test_login_user_failure(self):
        payload = {
            "email": LoginFailedUser.email,
            "password": LoginFailedUser.password
        }
        
        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = requests.post(UrlsSB.urlLoginUser, json=payload)
            response_body = response.json()
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            assert response_body['success'] == False
            assert response_body['message'] == "email or password are incorrect"