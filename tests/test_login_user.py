import os
import sys
sys.path.append(os.getcwd())

import allure
import requests

from data import Data


@allure.epic("Login")
class TestLoginUser:

    @allure.title("Successful login")
    def test_successful_login(self, new_user):
        payload = {
            "email": new_user["email"],
            "password": new_user["password"],
        }
        response = requests.post(Data.LOGIN_URL, data=payload)

        assert response.status_code == 200
        assert len(response.json()["accessToken"]) > 10
        assert "Bearer" in response.json()["accessToken"]
        assert response.json()["user"]["email"] == new_user["email"]

    @allure.title("Failed login with wrong password")
    def test_login_with_wrong_password(self, new_user):
        payload = {
            "email": new_user["email"],
            "password": "Wrong Password",
        }
        response = requests.post(Data.LOGIN_URL, data=payload)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"

    @allure.title("Failed login with wrong email")
    def test_login_with_wrong_email(self, new_user):
        payload = {
            "email": "some_email@test1-1.com",
            "password": new_user["password"],
        }
        response = requests.post(Data.LOGIN_URL, data=payload)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
        print(response.text)