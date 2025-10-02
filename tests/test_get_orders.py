import allure
import requests
from Credentials.urls import UrlsSB


class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Тест проверяет успешное получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка GET запроса для получения заказов пользователя"):
            response = requests.get(UrlsSB.urlGetOrders, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response_body['success'] == True
            assert 'orders' in response_body
            assert 'total' in response_body
            assert 'totalToday' in response_body
            
            # Проверяем структуру заказа, если заказы есть
            if len(response_body['orders']) > 0:
                order = response_body['orders'][0]
                assert '_id' in order
                assert 'ingredients' in order
                assert 'status' in order
                assert 'number' in order
                assert 'createdAt' in order
                assert 'updatedAt' in order
                
                # Проверяем возможные статусы заказа
                assert order['status'] in ['done', 'pending', 'created', 'canceled']

    @allure.title("Получение заказов неавторизованного пользователя")
    @allure.description("Тест проверяет ошибку при попытке получить заказы без авторизации")
    def test_get_user_orders_without_auth(self):
        with allure.step("Отправка GET запроса без авторизации"):
            response = requests.get(UrlsSB.urlGetOrders)
        
        response_body = response.json()
        
        with allure.step("Проверка ответа с ошибкой авторизации"):
            assert response.status_code == 401
            assert response_body['success'] == False
            assert response_body['message'] == "You should be authorised"

    @allure.title("Получение заказов с максимальным количеством")
    @allure.description("Тест проверяет что возвращается не более 50 последних заказов")
    def test_get_user_orders_max_count(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка GET запроса для получения заказов"):
            response = requests.get(UrlsSB.urlGetOrders, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка что количество заказов не превышает 50"):
            assert response.status_code == 200
            assert response_body['success'] == True
            assert len(response_body['orders']) <= 50

    @allure.title("Проверка сортировки заказов по времени обновления")
    @allure.description("Тест проверяет что заказы отсортированы по возрастанию времени обновления (старые первые)")
    def test_orders_sorted_by_updated_time(self, login_user):
        with allure.step("Получение токена авторизации"):
            token = login_user()
        
        headers = {
            "Authorization": token
        }
        
        with allure.step("Отправка GET запроса для получения заказов"):
            response = requests.get(UrlsSB.urlGetOrders, headers=headers)
        
        response_body = response.json()
        
        with allure.step("Проверка сортировки заказов (старые заказы должны быть первыми)"):
            if len(response_body['orders']) > 1:
                orders = response_body['orders']
                for i in range(len(orders) - 1):
                    assert orders[i]['updatedAt'] <= orders[i + 1]['updatedAt']