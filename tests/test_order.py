import os
import sys
sys.path.append(os.getcwd())
import allure
from conftest import new_user
from conftest import all_ingredients

sys.path.append(os.getcwd())
from helpers.steps import Steps

@allure.epic('Customers create orders')
class TestOrder:

    @allure.title("Create order")
    def test_create_order(self, new_user, all_ingredients):
        meat = Steps.get_random_ingredient("main", all_ingredients)
        bun = Steps.get_random_ingredient("bun", all_ingredients)
        sauce = Steps.get_random_ingredient("sauce", all_ingredients)
        payload = {
            "ingredients": [bun.get("_id"), sauce.get("_id"), meat.get("_id")],
        }
        response = Steps.create_order(new_user, payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["order"]["number"] > 0
        assert len(response.json()["name"])> 5
        assert bun in response.json()["order"]["ingredients"]
        assert meat in response.json()["order"]["ingredients"]
        assert sauce in response.json()["order"]["ingredients"]

    @allure.title("None logged user create order")
    def test_none_logged_user_create_order(self, all_ingredients):
        meat = Steps.get_random_ingredient("main", all_ingredients)
        bun = Steps.get_random_ingredient("bun", all_ingredients)
        payload = {
            "ingredients": [bun.get("_id"), meat.get("_id")],
        }
        user = {"access_token":"wrong_token"}
        response = Steps.create_order(user, payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["order"]["number"] > 0
        assert len(response.json()["name"]) > 5


    @allure.title("Logged in user creates order without ingredients")
    def test_logged_in_user_create_order_no_ingredients(self, new_user):
        payload = {
            "ingredients": [],
        }
        response = Steps.create_order(new_user, payload)
        assert response.status_code == 400

    @allure.title("Unauthorized user creates order without ingredients")
    def test_none_logged_in_user_create_order_no_ingredients(self):
        payload = {
            "ingredients": [],
        }
        user = {"access_token":"wrong_token"}
        response = Steps.create_order(user, payload)
        assert response.status_code == 400

    @allure.title("Create with bad ingredients id")
    def test_create_order_with_wrong_ingredient_id(self, new_user):
        payload = {
            "ingredients": ["12","asdad", "!234$"]
        }
        response = Steps.create_order(new_user, payload)
        assert response.status_code == 500

