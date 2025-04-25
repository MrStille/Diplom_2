import allure
import pytest
import requests
import os
import sys

from helpers.api_errors import ApiErrors
from helpers.steps import Steps

sys.path.append(os.getcwd())

from data import Data
from helpers.utils import ApiHelper


@allure.epic('Create customer')
class TestCreateUser:
    url = Data.API_URL + "auth/register"

    @allure.title("Create new user")
    def test_create_user(self):
        payload = {
            "email": ApiHelper.get_random_email(),
            "password": ApiHelper.generate_random_string(10),
            "name": "Test User"
        }
        response = Steps.create_user(payload)
        assert response.status_code == 200
        assert len(response.json()['accessToken']) > 10
        assert len(response.json()['refreshToken']) > 10
        Steps.delete_user({"access_token":response.json()['accessToken']})


    @allure.title("Cannot create user with the same email")
    def test_create_existing_user(self, new_user):
        payload = {
            "email": new_user["email"],
            "password": ApiHelper.generate_random_string(10),
            "name": ApiHelper.generate_random_string(10)
        }
        response = Steps.create_user(payload)
        assert response.status_code == 403
        assert response.json()['message'] == ApiErrors.USER_EXISTS_ERROR
        assert response.json()['success'] == False

    @allure.title("Cannot create new user without all fields filled")
    @pytest.mark.parametrize('create_user_payload', [
        {
            "email": "",
            "password": ApiHelper.generate_random_string(10),
            "name": "Test User"
        },
        {
            "email": ApiHelper.get_random_email(),
            "password": "",
            "name": "Test User"
        },
        {
            "email": ApiHelper.get_random_email(),
            "password": ApiHelper.generate_random_string(10),
            "name": ""
        }
    ])

    def test_create_without_values(self, create_user_payload):
        response = Steps.create_user(create_user_payload)
        assert response.status_code == 403
        assert response.json()['message'] == ApiErrors.USER_NO_REQUIRED_FIELDS_ERROR
        assert response.json()['success'] == False
