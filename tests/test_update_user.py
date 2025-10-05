import allure
import requests
from Credentials.urls import UrlsSB


class TestRefactorUser:
    @allure.title("Обновление данных пользователя с авторизацией")
    @allure.description("Тест проверяет успешное обновление данных пользователя при наличии авторизации")
    def test_update_user(self, login_user):
        token = login_user()
        payload = {
            "name": 'qwerty_new',
            "email": 'new@mail.ru'
        }
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка PATCH запроса для обновления данных пользователя"):
            response = requests.patch(UrlsSB.urlRefactorUser, json=payload, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка успешного ответа"):
            assert response_body['success'] == True
            assert response_body['user']['name'] == 'qwerty_new'
            assert response_body['user']['email'] == 'new@mail.ru'
    
    @allure.title("Обновление данных пользователя без авторизации")
    @allure.description("Тест проверяет ошибку при попытке обновить данные пользователя без авторизации")
    def test_update_user_unauthorized(self):
        # Второй тест - без авторизации
        payload = {
            "name": 'qwerty15',
            "email": 'qwerty15@mail.ru'
        }
        
        with allure.step("Отправка PATCH запроса без авторизации"):
            response = requests.patch(UrlsSB.urlRefactorUser, json=payload)
        
        response_body = response.json()
        
        with allure.step("Проверка ответа с ошибкой авторизации"):
            assert response.status_code == 401
            assert response_body['success'] == False
            assert response_body['message'] == "You should be authorised"