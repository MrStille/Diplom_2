import allure
import pytest
import requests
import os
import sys
sys.path.append(os.getcwd())

from helpers.steps import Steps

@allure.epic('Customer change their account info')
class TestUserUpdate:

    @allure.title("User update test his account")
    @pytest.mark.parametrize('patch_user',[
        {"email":"new_email@t1.rau"},
        {"name": "New Name"},
        {"password": "Password!"},

    ])
    def test_user_update(self, new_user, patch_user):
        for key, value in patch_user.items():
            if key in new_user.keys():
                new_user[key] = value

        payload = {
            "email": new_user["email"],
            "password": new_user["password"],
            "name": new_user["name"]
        }
        update_response = Steps.patch_user(new_user, payload)
        assert update_response.status_code == 200
        user_info = Steps.get_user_info(new_user)
        assert user_info.json()["user"]["email"] == new_user["email"]
        assert user_info.json()["user"]["name"] == new_user["name"]
        login_response = Steps.login_user(new_user)
        assert login_response.status_code == 200


    @allure.title("None logged user cannot update his account")
    @pytest.mark.parametrize('patch_user',[
        {"email":"new_email@t1.rau"},
        {"name": "New Name"},
        {"password": "Password!"},

    ])
    def test_not_logged_user_update(self, new_user, patch_user):
        for key, value in patch_user.items():
            if key in new_user.keys():
                new_user[key] = value

        payload = {
            "email": new_user["email"],
            "password": new_user["password"],
            "name": new_user["name"]
        }
        bad_token = {"access_token": "wrong token"}
        update_response = Steps.patch_user(bad_token, payload)
        assert update_response.status_code == 403
        assert update_response.json()["message"] == 'jwt malformed'
