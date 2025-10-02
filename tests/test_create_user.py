import pytest
import allure
import requests
from Credentials.data_user import DataUser
from Credentials.urls import UrlsSB


@allure.feature("Создание пользователя")
class TestCreateUser:
    
    # Список для хранения токенов созданных пользователей
    created_users_tokens = []
    
    @allure.title("Тест создания пользователя")
    @allure.story("Проверка различных сценариев создания пользователя")
    @pytest.mark.parametrize('email, password, name', DataUser.emailPasswordName)
    def test_create_users(self, email, password, name):
        payload = {
            "email": email,
            "password": password, 
            "name": name
        }
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(UrlsSB.urlCreateUser, json=payload)
            response_body = response.json()
        
        with allure.step("Валидация ответа"):
            if response_body['success'] == False:
                if email == '' or password == '' or name == '':
                    with allure.step("Проверка ошибки валидации"):
                        assert response.status_code == 403
                        assert response_body["message"] == "Email, password and name are required fields"
                else:
                    with allure.step("Проверка ошибки дубликата"):
                        assert response.status_code == 403
                        assert response_body["message"] == "User already exists"
            elif response_body['success'] == True:
                with allure.step("Проверка успешного создания"):
                    assert response.status_code == 200
                    assert response_body["user"]["email"] == email
                    assert response_body["user"]["name"] == name
                    assert "accessToken" in response_body
                    assert "refreshToken" in response_body
                    
                    # Сохраняем токен для последующего удаления
                    access_token = response_body["accessToken"]
                    self.created_users_tokens.append(access_token)

    # Фикстура для очистки после всех тестов в классе
    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_tests(self):
        yield
        self.delete_created_users()
    
    def delete_created_users(self):
        with allure.step("Удаление созданных пользователей"):
            for token in self.created_users_tokens:
                headers = {"Authorization": token}
                try:
                    response = requests.delete(UrlsSB.urlDeleteUser, headers=headers)
                    if response.status_code == 202:
                        allure.attach(f"Пользователь с токеном {token[:20]}... успешно удален", 
                                    name="Удаление пользователя")
                    else:
                        allure.attach(f"Ошибка при удалении пользователя: {response.status_code}", 
                                    name="Ошибка удаления")
                except Exception as e:
                    allure.attach(f"Исключение при удалении: {str(e)}", name="Ошибка удаления")