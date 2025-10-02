import allure
import requests
from Credentials.urls import UrlsSB


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Тест проверяет успешное создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        with allure.step("Получение списка ингредиентов"):
            ingredients_response = requests.get(UrlsSB.urlIngredients)
            ingredients_data = ingredients_response.json()
            valid_ingredients = [ingredient for ingredient in ingredients_data['data']][:2]
        
        payload = {
            "ingredients": valid_ingredients
        }
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка POST запроса для создания заказа"):
            response = requests.post(UrlsSB.urlCreateOrder, json=payload, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response_body['success'] == True
            assert 'name' in response_body
            assert 'order' in response_body
            assert 'number' in response_body['order']

    @allure.title("Создание заказа без авторизации с ингредиентами")
    @allure.description("Тест проверяет создание заказа без авторизации с валидными ингредиентами")
    def test_create_order_without_auth_with_ingredients(self):
        with allure.step("Получение списка ингредиентов"):
            ingredients_response = requests.get(UrlsSB.urlIngredients)
            ingredients_data = ingredients_response.json()
            valid_ingredients = [ingredient for ingredient in ingredients_data['data']][:2]
        
        payload = {
            "ingredients": valid_ingredients
        }
        
        with allure.step("Отправка POST запроса для создания заказа без авторизации"):
            response = requests.post(UrlsSB.urlCreateOrder, json=payload)
        
        response_body = response.json()
        
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response_body['success'] == True
            assert 'name' in response_body
            assert 'order' in response_body
            assert 'number' in response_body['order']

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        payload = {
            "ingredients": []
        }
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка POST запроса для создания заказа без ингредиентов"):
            response = requests.post(UrlsSB.urlCreateOrder, json=payload, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 400
            assert response_body['success'] == False
            assert response_body['message'] == "Ingredient ids must be provided"

    @allure.title("Создание заказа без авторизации без ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self):
        payload = {
            "ingredients": []
        }
        
        with allure.step("Отправка POST запроса для создания заказа без авторизации и без ингредиентов"):
            response = requests.post(UrlsSB.urlCreateOrder, json=payload)
        
        response_body = response.json()
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 400
            assert response_body['success'] == False
            assert response_body['message'] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа с невалидными хешами ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        payload = {
            "ingredients": ["invalid_hash_1", "invalid_hash_2"]
        }
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка POST запроса с невалидными хешами ингредиентов"):
            response = requests.post(UrlsSB.urlCreateOrder, json=payload, headers=headers)
        
        with allure.step("Проверка ответа с ошибкой сервера"):
            assert response.status_code == 500