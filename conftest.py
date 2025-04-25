import os
import sys
sys.path.append(os.getcwd())
import pytest
import requests
from helpers.steps import Steps

from data import Data
from helpers.utils import ApiHelper


@pytest.fixture(scope='function')
def new_user():
    payload = {
        "email": ApiHelper.get_random_email(),
        "password": ApiHelper.generate_random_string(10),
        "name": "Test User"
    }
    response = requests.post(Data.REGISTER_URL, data=payload)
    assert response.status_code == 200
    user = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "access_token": response.json()["accessToken"],
        "refresh_token": response.json()["refreshToken"]
    }
    yield user
    response = Steps.delete_user(user)
    print(response.json())


@pytest.fixture(scope='class')
def all_ingredients():
    all_ingredients = {}
    ingredients = Steps.get_ingredients().json()["data"]
    for ingredient in ingredients:
        if len(all_ingredients) <= 3:
            all_ingredients.setdefault(ingredient.get("type"), list())
        all_ingredients[ingredient.get("type")].append(ingredient)
    return all_ingredients


def pytest_make_parametrize_id(config, val):
    return repr(val)
