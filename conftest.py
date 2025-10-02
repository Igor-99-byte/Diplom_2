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