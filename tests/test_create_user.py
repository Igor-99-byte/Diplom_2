import pytest
import allure
import requests
from Credentials.data_user import DataUser
from Credentials.urls import UrlsSB


@allure.feature("Создание пользователя")
class TestCreateUser:
    dataUser = DataUser()
    @allure.title("Успешное создание пользователя")
    @allure.story("Создание пользователя с валидными данными")
    @pytest.mark.parametrize('email, password, name', [
        (dataUser.create_email(), dataUser.create_password(), dataUser.create_name()),
        (dataUser.create_email(), dataUser.create_password(), dataUser.create_name())
    ])
    def test_create_user_success(self, email, password, name, cleanup_users):
        payload = {
            "email": email,
            "password": password, 
            "name": name
        }
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(UrlsSB.urlCreateUser, json=payload)
            response_body = response.json()
        
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            assert response_body["success"] == True
            assert response_body["user"]["email"] == email
            assert response_body["user"]["name"] == name
            assert "accessToken" in response_body
            assert "refreshToken" in response_body
            
            # Сохраняем токен для последующего удаления
            access_token = response_body["accessToken"]
            cleanup_users.append(access_token)

    @allure.title("Создание пользователя без обязательных полей")
    @allure.story("Попытка создания пользователя с пустыми полями")
    @pytest.mark.parametrize('email, password, name', [
        ("", "password123", "Test User"),
        ("test@example.com", "", "Test User"),
        ("test@example.com", "password123", "")
    ])
    def test_create_user_missing_required_fields(self, email, password, name):
        payload = {
            "email": email,
            "password": password, 
            "name": name
        }
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(UrlsSB.urlCreateUser, json=payload)
            response_body = response.json()
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403
            assert response_body["success"] == False
            assert response_body["message"] == "Email, password and name are required fields"

    @allure.title("Создание дубликата пользователя")
    @allure.story("Попытка создания пользователя с существующим email")
    def test_create_user_duplicate(self, cleanup_users):
        payload = {
            "email": "qwerty13@mail.ru",
            "password": "password123", 
            "name": "Duplicate User"
        }
        
        with allure.step("Создание первого пользователя"):
            response1 = requests.post(UrlsSB.urlCreateUser, json=payload)
            if response1.status_code == 200:
                access_token = response1.json()["accessToken"]
                cleanup_users.append(access_token)
        
        with allure.step("Попытка создания дубликата"):
            response2 = requests.post(UrlsSB.urlCreateUser, json=payload)
            response_body = response2.json()
        
        with allure.step("Проверка ошибки дубликата"):
            assert response2.status_code == 403
            assert response_body["success"] == False
            assert response_body["message"] == "User already exists"